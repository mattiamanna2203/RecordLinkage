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
   print(f"Coppie candidate: {len(candidate_links)}")        # Mostrare a schermo il numero di coppie candidate

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
   match = features[features['name_similarity'] > soglia] # Estrazione coppie match


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
   return match

def record_linkage_city_title(dataframe_1 : pd.DataFrame(),
                              dataframe_2 : pd.DataFrame(),
                              soglia_titolo : float,
                              soglia_city : float
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



   # Aggiungi ID se non esistono
   dataframe_2['id_booking'] = dataframe_2.index
   dataframe_1['id_agoda'] = dataframe_1.index

   # Pulizia titoli e indirizzi
   dataframe_2['titolo_booking'] = clean(dataframe_2['titolo']).str.lower().str.strip()
   dataframe_1['titolo_agoda'] = clean(dataframe_1['titolo']).str.lower().str.strip()
   dataframe_2['città_booking'] = clean(dataframe_2['città']).str.lower().str.strip()
   dataframe_1['città_agoda'] = clean(dataframe_1['città']).str.lower().str.strip()

   # Blocking sulla prima lettera del titolo
   dataframe_2['first_letter'] = dataframe_2['titolo_booking'].str[0]
   dataframe_1['first_letter'] = dataframe_1['titolo_agoda'].str[0]

   indexer = recordlinkage.Index()
   indexer.block('first_letter')
   candidate_links = indexer.index(dataframe_2, dataframe_1)
   print(f"Coppie candidate: {len(candidate_links)}")

   # Comparazione con Jaro-Winkler
   compare = recordlinkage.Compare()
   compare.string('titolo_booking', 'titolo_agoda', method='jarowinkler', label='name_similarity')
   compare.string('città_booking', 'città_agoda', method='jarowinkler', label='città_similarity')
   features = compare.compute(candidate_links, dataframe_2, dataframe_1)

   print(features.describe())

   # binarizzazione per Fellegi-Sunter (lascia più margine)
   features_bin = features.copy()
   features_bin["name_similarity"] = features_bin["name_similarity"] > soglia_titolo
   features_bin["città_similarity"] = features_bin["città_similarity"] > soglia_city

   # ECMClassifier (Fellegi-Sunter)
   fs = recordlinkage.ECMClassifier()
   fs.fit(features_bin)
   matches = fs.predict(features_bin)

   # calcola punteggio medio come proxy (media delle similarità)
   scores = features.loc[list(matches)].mean(axis=1)

   # dataframe con punteggio
   scores_df = scores.reset_index()
   scores_df.columns = ['index_booking', 'index_agoda', 'score']

   # ordina dal match migliore al peggiore
   scores_df = scores_df.sort_values('score', ascending=False)

   # deduplica one-to-one greedy
   scores_df = scores_df.drop_duplicates(subset='index_booking', keep='first')
   scores_df = scores_df.drop_duplicates(subset='index_agoda', keep='first')


   # risultato finale
   matches_df_2_new = scores_df[['index_booking', 'index_agoda']]



   # Recupero info
   matches_df_2_new['id_booking'] = dataframe_2.loc[matches_df_2_new['index_booking'], 'id_booking'].values
   matches_df_2_new['id_agoda'] = dataframe_1.loc[matches_df_2_new['index_agoda'], 'id_agoda'].values
   matches_df_2_new['titolo_booking'] = dataframe_2.loc[matches_df_2_new['index_booking'], 'titolo_booking'].values
   matches_df_2_new['titolo_agoda'] = dataframe_1.loc[matches_df_2_new['index_agoda'], 'titolo_agoda'].values
   matches_df_2_new['città_booking'] = dataframe_2.loc[matches_df_2_new['index_booking'], 'città_booking'].values
   matches_df_2_new['città_agoda'] = dataframe_1.loc[matches_df_2_new['index_agoda'], 'città_agoda'].values
   matches_df_2_new['zona_booking'] = dataframe_2.loc[matches_df_2_new['index_booking'], 'zona'].values
   matches_df_2_new['zona_agoda'] = dataframe_1.loc[matches_df_2_new['index_agoda'], 'zona'].values
   matches_df_2_new['name_similarity'] = features.loc[list(zip(matches_df_2_new['index_booking'], matches_df_2_new['index_agoda'])), 'name_similarity'].values
   matches_df_2_new['città_similarity'] = features.loc[list(zip(matches_df_2_new['index_booking'], matches_df_2_new['index_agoda'])), 'città_similarity'].values
   matches_df_2_new['pair'] = matches_df_2_new['id_booking'].astype(str) + '#' + matches_df_2_new['id_agoda'].astype(str)
   matches_df_2_new['prezzo_booking'] = dataframe_2.loc[matches_df_2_new['index_booking'], 'prezzo'].values
   matches_df_2_new['prezzo_agoda'] = dataframe_1.loc[matches_df_2_new['index_agoda'], 'prezzo'].values

   print(f"Match one-to-one trovati: {len(matches_df_2_new)}")
   
   matches_df_2_new.drop(columns=["index_booking","index_agoda"],inplace=True)

   return matches_df_2_new


def bozze():
   # STEP 5
# Trovare i match. Si procede con due strade diverse.
# La prima (clausola try) riguarda il tentativo con ECMClassifier
# L'ECMClassifier implementa il modello probabilistico di Fellegi-Sunter, che stima automaticamente quali coppie sono match o non-match.
# L'ECMClassifier è l'implementazione del modello di Fellegi-Sunter basato sull’algoritmo Expectation Conditional Maximization (ECM), una variante dell’algoritmo EM.
# è un modo migliore è più chiaro di trovare i match. In caso non funzioni si passa ad un criterio basato su soglia.

   try:
      fs = recordlinkage.ECMClassifier() # Crea un'istanza del classificatore probabilistico.
      fs.fit(features)  #  Allena il modello con i dati di similarità calcolati (es. name_similarity). ECMClassifier.fit() richiede che features abbia come indice le coppie di record da confrontare, ovvero un MultiIndex
      matches = fs.predict(features)  # Il risultato matches è un pandas MultiIndex con le coppie classificate come match. (non match vengono scartati).
      display(matches)
      matches_df_1 = pd.DataFrame(list(matches), columns=['index_booking', 'index_agoda'])

      metodo = 'Fellegi-Sunter'

   # Se  ECMClassifier fallisce (ad es. dataset troppo piccolo o distribuzione sbilanciata), scatta l’except.
   except:
      # Trovare i match. Le coppie con un valore di similarità superiore a una soglia stabilita sono considerate match.
      features = features[features['name_similarity'] > soglia] # Estrazione coppie match
      features.reset_index(inplace=True) # Fare il reset degli indici. In questo modo si avranno come variabili gli indici delle location. 
                                                # Avere gli indici come variabili faciliterà poi  le prossime operazioni.                                  
      features = features.rename(columns={'level_0': 'index_booking', 'level_1': 'index_agoda'}) # Rinominare le variabili indice
      metodo = f'Soglia fissa > {soglia}'
      features
   print(metodo)