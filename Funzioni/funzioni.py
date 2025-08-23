import pandas as pd 
import recordlinkage
from recordlinkage.preprocessing import clean


def record_linkage_title(copia_agoda : pd.DataFrame(),
                         copia_booking : pd.DataFrame(),
                         soglia : float ) -> pd.DataFrame():
   """Funzione per praticare il record linkage tra due dataframe, selezione tramite threshold. 
      Non si tratta di una vera e propria funzione in quanto i parametri sono molti e non tutti selezionabili, è solo un modo per risparmiare codice e rendere tutto più chiaro e semplice.
      Input:
         - Dataframe1;
         - Dataframe2;
         - Soglia (threshold).
         
      Output:
         - Restituisce un dataframe con i risultati.
   """


   # Aggiungere le colonne ID: 
   copia_booking['id_booking'] = copia_booking.index
   copia_agoda['id_agoda'] = copia_agoda.index
   

   copia_booking = copia_booking.rename(columns={"titolo_processed":"titolo_booking"})
   copia_agoda = copia_agoda.rename(columns={"titolo_processed":"titolo_agoda"})

   # Blocking sulla prima lettera (Il blocking sulla prima lettera è una tecnica di record linkage usata per ridurre il numero di confronti tra record che devono essere effettuati.)
   #  Nel record linkage, si confrontano record da due (o più) set di dati per trovare duplicati o corrispondenze. Confrontare ogni record con tutti gli altri è computazionalmente costoso, soprattutto con set grandi complessità. 
   # Il blocking serve a limitare i confronti a gruppi più piccoli di record che condividono una certa caratteristica.
   # Il blocking sulla prima lettera: significa che i record vengono suddivisi in blocchi in base alla prima lettera di un campo di testo, per esempio un cognome, un nome o un indirizzo. Solo i record che iniziano con la stessa lettera vengono poi confrontati tra loro.
   copia_booking['first_letter'] = copia_booking['titolo_booking'].str[0]
   copia_agoda['first_letter'] = copia_agoda['titolo_agoda'].str[0]

   # STEP 1
   # Creare un oggetto di tipo Index e  definire una strategia di "blocking" basata sul valore della colonna 'first_letter'.
   indexer = recordlinkage.Index() # Creare index
   indexer.block('first_letter') # Definire il blocking sulla prima colonna

   # STEP 2
   #  Generare i candidate pairs (coppie da confrontare) tra due dataset (copia_booking e copia_agoda), 
   # secondo le regole di blocking definite prima con indexer.block() (step 1).
   candidate_links = indexer.index(copia_booking, copia_agoda) # Trovare le coppie da confrontare 
   #print(f"Coppie candidate: {len(candidate_links)}")        # Mostrare a schermo il numero di coppie candidate

   # STEP 3
   # Configurare il confronto tra due colonne di testo, usando il metodo di similarità Jaro-Winkler.
   # Il metodo Jaro-Winkler è particolarmente efficace per confrontare stringhe brevi e con piccole variazioni o errori di battitura (es. "Hotel Roma" vs "Hotel Roma Center").
   compare = recordlinkage.Compare()
   compare.string('titolo_booking',         # variabile 1 da confrontare
                  'titolo_agoda',           # variabile 2 da confrontare
                  method='jarowinkler',    # Metodo per il confronto
                  label='name_similarity'  # Nome della variabile risultante contenente la simililarità, compresa tra 0 e 1 (0 stringhe completamente diverse, 1 stringhe identiche)
                  )

   # STEP 4
   # Eseguire effettivamente il confronto tra le coppie di record (i candidate links) generate in precedenza (STEP 2).
   # Usa le regole di similarità definite con compare
   features = compare.compute(candidate_links, copia_booking, copia_agoda) # Restituisce un pandas dataframe con la similarity per ogni coppia
   #print(features['name_similarity'].describe()) # Overview sulle similarities calcolate.

   # STEP 5
   # Trovare i match. Le coppie con un valore di similarità superiore a una soglia stabilita sono considerate match.
   # Il metodo fellegi sunter non può essere usato su una sola variabile quindi si fa direttamente la selezione tramite soglia.
   scores_df = features[features['name_similarity'] > soglia] # Estrazione coppie match
   # Ordinare il dataset dei risultati. Aggiungere ai match le informazioni di agoda e booking
   scores_df.reset_index(inplace=True)  # Fare il reset degli indici. In questo modo si avranno come variabili gli indici delle location. 
                                    # Avere gli indici come variabili faciliterà poi  le prossime operazioni.                                  
   scores_df = scores_df.rename(columns={'level_0': 'index_booking', 'level_1': 'index_agoda'}) # Rinominare le variabili indice
   scores_df['pair'] = scores_df['index_booking'].astype(str) + '#' + scores_df['index_agoda'].astype(str)

   # Negli step successivi:
   # A. Eliminati tutti gli index che hanno più di un match
   # B. Selezionato solo l'index booking duplicato con score maggiore, a parità presi entrambi
   # C. Selezionato solo l'index agoda duplicato con score maggiore, a parità presi entrambi
   # D. Inserire nuovamente i match migliori.
   # In questo modo se una location ha più di un match si prende quella con la probabilità di match migliore
   # è infatti inutile avere due match diversi dato che uno sarà sicuramente sbagliato dato che la corrispondenza deve
   # essere 1:1
   match = scores_df.copy()


   # A. Prendere solo il match migliore per ogni location, non ha senso prendere la seconda opzione.
   match = scores_df.drop_duplicates(subset='index_booking', keep=False)
   match = match.drop_duplicates(subset='index_agoda', keep=False)

   # B.
   # Filtra solo i duplicati su index_booking
   dups = scores_df[scores_df.duplicated(subset='index_booking', keep=False)]
   # Raggruppa per index_booking e seleziona il massimo score
   booking_best_match = dups.groupby('index_booking', group_keys=False).apply(
      lambda row: row[row['name_similarity'] == row['name_similarity'].max()]
   )

   # C.
   # Filtra solo i duplicati su index_agoda
   dups = scores_df[scores_df.duplicated(subset='index_agoda', keep=False)]
   # Raggruppa per index_booking e seleziona il massimo score
   agoda_best_match = dups.groupby('index_agoda', group_keys=False).apply(
      lambda row: row[row['name_similarity'] == row['name_similarity'].max()]
   )

   # D.
   agoda_best_match["pair"] = agoda_best_match['index_booking'].astype(str) + '#' + agoda_best_match['index_agoda'].astype(str)
   booking_best_match["pair"] = booking_best_match['index_booking'].astype(str) + '#' + booking_best_match['index_agoda'].astype(str)
   match = pd.concat([match,booking_best_match])
   match = pd.concat([match,agoda_best_match])


   # STEP 6
   # Ordinare il dataset dei risultati. Aggiungere ai match le informazioni di agoda e booking

   match.reset_index(inplace=True) # Fare il reset degli indici. In questo modo si avranno come variabili gli indici delle location. 
                                    # Avere gli indici come variabili faciliterà poi  le prossime operazioni.                                  
   match = match.rename(columns={'level_0': 'index_booking', 'level_1': 'index_agoda'}) # Rinominare le variabili indice

   match['pair'] = match['index_booking'].astype(str) + '#' + match['index_agoda'].astype(str)

   # Lista delle variabili da inserire nel dataset finale dei match. 
   # Evito di inserie numero di notti e persone perchè è lo stesso per entrambi i dataset. E quindi si prende direttamente dall'ultimo dataset
   variabili_comuni = ["titolo", "zona","città","distanza_centro","prezzo", 
                     'recensione_voto_numerico', 'recensione_voto_parola', 'numero_recensioni'] 

   # Unire il dataframe dei match con il dataframe booking. Prendere solo le informazioni delle accomodation in comune.
   match = pd.merge(match, # Dataframe left
                  copia_booking[variabili_comuni], # Dataframe right
                  left_on="index_booking", # Il dataframe left (match) ha come indice per il merge la variabile 'index_booking'
                  right_index=True # Il dataframe right (booking) ha come indice per il merge l'index.
                  ) 

   variabili_comuni.extend(['numero_notti', 'numero_persone', 'inizio_permanenza', 'fine_permanenza']) # Ora posso aggiungere le variabili comuni.
   match =  pd.merge(match, # Dataframe left
                  copia_agoda[variabili_comuni], # Dataframe right
                  left_on="index_agoda", # Il dataframe left (match) ha come indice per il merge la variabile 'index_booking'
                  right_index=True, # Il dataframe right (booking) ha come indice per il merge l'index.
                  suffixes=("_booking","_agoda") # Le variabili che avranno nome uguali in left e right avranno suffisso 'booking' in left e suffisso 'agoda' in right
                  ) 

                                                                        
   # Ordinare le colonne per una visualizzazione dei dati migliore.
   match = match[[ 'pair','name_similarity',
                  'titolo_booking', 'titolo_agoda',
                  'zona_booking','zona_agoda',
                  'città_booking', 'città_agoda',
                  'prezzo_booking', 'prezzo_agoda', 
                  'index_booking', 'index_agoda',
                  'distanza_centro_booking', 'distanza_centro_agoda',
                  'recensione_voto_numerico_booking', 'recensione_voto_numerico_agoda',
                  'recensione_voto_parola_booking',    'recensione_voto_parola_agoda',
                  'numero_recensioni_booking','numero_recensioni_agoda',
                  'numero_notti', 'numero_persone', 'inizio_permanenza', 'fine_permanenza', 
               ]]
   match.drop_duplicates(inplace=True) # Rimuovere righe duplicate
   return match

def record_linkage_city_title(dataframe_booking : pd.DataFrame(),
                              dataframe_agoda : pd.DataFrame(),
                              soglia_titolo : float,
                              soglia_città : float
                              ) -> pd.DataFrame():
   """Funzione per praticare il record linkage tra due dataframe. 
      Utilizza il metodo: 'Fellegi-Sunter'.
      Input:
         - Dataframe1;
         - Dataframe2;
         - Soglia (threshold).
         
      Output:
         - Restituisce un dataframe con i risultati.
   """
   copia_booking = dataframe_booking.copy()
   copia_agoda = dataframe_agoda.copy()

   # Aggiungere le colonne ID: 
   copia_booking['id_booking'] = copia_booking.index
   copia_agoda['id_agoda'] = copia_agoda.index

   copia_booking = copia_booking.rename(columns={"titolo_processed":"titolo_booking"})
   copia_agoda = copia_agoda.rename(columns={"titolo_processed":"titolo_agoda"})

   # Blocking sulla prima lettera (Il blocking sulla prima lettera è una tecnica di record linkage usata per ridurre il numero di confronti tra record che devono essere effettuati.)
   #  Nel record linkage, si confrontano record da due (o più) set di dati per trovare duplicati o corrispondenze. Confrontare ogni record con tutti gli altri è computazionalmente costoso, soprattutto con set grandi complessità. 
   # Il blocking serve a limitare i confronti a gruppi più piccoli di record che condividono una certa caratteristica.
   # Il blocking sulla prima lettera: significa che i record vengono suddivisi in blocchi in base alla prima lettera di un campo di testo, per esempio un cognome, un nome o un indirizzo. Solo i record che iniziano con la stessa lettera vengono poi confrontati tra loro.
   copia_booking['first_letter'] = copia_booking['titolo_booking'].str[0]
   copia_agoda['first_letter'] = copia_agoda['titolo_agoda'].str[0]
   copia_agoda.head(1)

   # STEP 0, impostare i threshold/soglie
   soglia_titolo = 0.95
   soglia_città = 0.9

   # STEP 1, strategia di blocking
   indexer = recordlinkage.Index()
   indexer.block('first_letter')


   # STEP 2, candidate pairs
   candidate_links = indexer.index(copia_booking, copia_agoda)


   # STEP 3, configurare metodo per il calcolo delle similarità
   compare = recordlinkage.Compare()
   compare.string('titolo_booking', 'titolo_agoda', method='jarowinkler', label='name_similarity')
   compare.string('città', 'città', method='jarowinkler', label='città_similarity')

   # STEP 4, calcolo similarità
   features = compare.compute(candidate_links, copia_booking, copia_agoda)


   # STEP 5 
   # Binarizzazione per Fellegi-Sunter (lascia più margine)
   # Il modello si basa su variabili binarie che indicano se un certo campo matcha (coincide) o meno — o almeno supera una certa soglia di somiglianza.
   # Il modello Fellegi-Sunter lavora meglio (o richiede) variabili binarie:
   # Invece di usare direttamente la similarità continua (es. 0.96, 0.87...), si trasforma in vero/falso in base a una soglia ritenuta significativa.
   # Questo semplifica il calcolo delle probabilità di match e non-match, che nel modello sono basate su matrici di confusione binarie (es. probabilità che name_similarity=True dato che è un match vs. non match).
   features_bin = features.copy()
   features_bin["name_similarity"] = features_bin["name_similarity"] > soglia_titolo
   features_bin["città_similarity"] = features_bin["città_similarity"] > soglia_città

   # STEP 6 Classificare tramite  ECMClassifier (Fellegi-Sunter) e trovare match.
   fs = recordlinkage.ECMClassifier() # Definire il classificatore
   fs.fit(features_bin)               # Train classificatore
   matches = fs.predict(features_bin) # Ottenere i match

   # calcola punteggio medio come proxy (media delle similarità)
   scores = features.loc[list(matches)].mean(axis=1)

   # Creare un dataframe con gli scores e rinominare le variabili
   scores_df = scores.reset_index()
   scores_df.columns = ['index_booking', 'index_agoda', 'score'] # Siccome l'ordine di confronto era booking e poi agoda, il primo indice è quello di booking, segue l'index di agoda e lo score


   # Negli step successivi:
   # A. Eliminati tutti gli index che hanno più di un match
   # B. Selezionato solo l'index booking duplicato con score maggiore, a parità presi entrambi
   # C. Selezionato solo l'index agoda duplicato con score maggiore, a parità presi entrambi
   # Ha senso siccome si sta facendo selezione con jarowinkler????
   match = scores_df.copy()

   # A. Prendere solo il match migliore per ogni location, non ha senso prendere la seconda opzione.
   match = scores_df.drop_duplicates(subset='index_booking', keep=False)
   match = match.drop_duplicates(subset='index_agoda', keep=False)

   # B.
   # Filtra solo i duplicati su index_booking
   dups = scores_df[scores_df.duplicated(subset='index_booking', keep=False)]

   # Raggruppa per index_booking e seleziona il massimo score
   booking_best_match = dups.groupby('index_booking', group_keys=False).apply(
      lambda row: row[row['score'] == row['score'].max()]
   )

   # C.
   # Filtra solo i duplicati su index_agoda
   dups = scores_df[scores_df.duplicated(subset='index_agoda', keep=False)]
   # Raggruppa per index_booking e seleziona il massimo score
   agoda_best_match = dups.groupby('index_agoda', group_keys=False).apply(
      lambda row: row[row['score'] == row['score'].max()]
   )

   # D.
   agoda_best_match["pair"] = agoda_best_match['index_booking'].astype(str) + '#' + agoda_best_match['index_agoda'].astype(str)
   booking_best_match["pair"] = booking_best_match['index_booking'].astype(str) + '#' + booking_best_match['index_agoda'].astype(str)
   match = pd.concat([match,booking_best_match])
   match = pd.concat([match,agoda_best_match])



   # STEP 7, aggiungere informazioni utili ai risultati
   match['pair'] = match['index_booking'].astype(str) + '#' + match['index_agoda'].astype(str)

   # Lista delle variabili da inserire nel dataset finale dei match. 
   # Evito di inserie numero di notti e persone perchè è lo stesso per entrambi i dataset. E quindi si prende direttamente dall'ultimo dataset
   variabili_comuni = ["titolo","zona","città","distanza_centro","prezzo", 
                     'recensione_voto_numerico','recensione_voto_parola','numero_recensioni'] 

   # Unire il dataframe dei match con il dataframe booking. Prendere solo le informazioni delle accomodation in comune.
   match = pd.merge(match, # Dataframe left
                  dataframe_booking[variabili_comuni], # Dataframe right
                  left_on="index_booking",   # Il dataframe left (match) ha come indice per il merge la variabile 'index_booking'
                  right_index=True # Il dataframe right (booking) ha come indice per il merge l'index.
                  ) 

   variabili_comuni.extend(['numero_notti', 'numero_persone', 'inizio_permanenza', 'fine_permanenza']) # Ora posso aggiungere le variabili comuni.
   match =  pd.merge(match, # Dataframe left
                  dataframe_agoda[variabili_comuni], # Dataframe right
                  left_on="index_agoda", # Il dataframe left (match) ha come indice per il merge la variabile 'index_booking'
                  right_index=True, # Il dataframe right (booking) ha come indice per il merge l'index.
                  suffixes=("_booking","_agoda") # Le variabili che avranno nome uguali in left e right avranno suffisso 'booking' in left e suffisso 'agoda' in right
                  ) 

   # Estrarre gli score della città e del titolo per poi aggiungerli al dataset finale
   single_scores = features.reset_index()
   single_scores["pair"] = single_scores["level_0"].astype(str) + '#' + single_scores["level_1"].astype(str)
   match = pd.merge(match,single_scores,on="pair")

                                                                        
   # Ordinare le colonne per una visualizzazione dei dati migliore.
   match = match[[ 'pair','score','name_similarity','città_similarity',
                  'titolo_booking', 'titolo_agoda',
                  'zona_booking','zona_agoda',
                  'città_booking', 'città_agoda',
                  'prezzo_booking', 'prezzo_agoda', 
                  'index_booking', 'index_agoda',
                  'distanza_centro_booking', 'distanza_centro_agoda',
                  'recensione_voto_numerico_booking', 'recensione_voto_numerico_agoda',
                  'recensione_voto_parola_booking',    'recensione_voto_parola_agoda',
                  'numero_recensioni_booking','numero_recensioni_agoda',
                  'numero_notti', 'numero_persone', 'inizio_permanenza', 'fine_permanenza', 
               ]]

   match.drop_duplicates(inplace=True) # Rimuovere righe duplicate
   return match