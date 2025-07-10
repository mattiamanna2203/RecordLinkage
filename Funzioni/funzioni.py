import pandas as pd 
import recordlinkage
from recordlinkage.preprocessing import clean


def record_linkage_title(dataframe_1 : pd.DataFrame(),
                        dataframe_2 : pd.DataFrame(),
                        soglia : float ) -> pd.DataFrame():
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

   # Pulizia titoli
   dataframe_2['titolo_booking'] = clean(dataframe_2['titolo']).str.lower().str.strip()
   dataframe_1['titolo_agoda'] = clean(dataframe_1['titolo']).str.lower().str.strip()

   # Blocking sulla prima lettera
   dataframe_2['first_letter'] = dataframe_2['titolo_booking'].str[0]
   dataframe_1['first_letter'] = dataframe_1['titolo_agoda'].str[0]

   indexer = recordlinkage.Index()
   indexer.block('first_letter')
   candidate_links = indexer.index(dataframe_2, dataframe_1)
   print(f"Coppie candidate: {len(candidate_links)}")

   # Similarità con Jaro-Winkler
   compare = recordlinkage.Compare()
   compare.string('titolo_booking', 'titolo_agoda', method='jarowinkler', label='name_similarity')
   features = compare.compute(candidate_links, dataframe_2, dataframe_1)
   print(features['name_similarity'].describe())

   # Tentativo con ECMClassifier
   try:
      fs = recordlinkage.ECMClassifier()
      fs.fit(features)  # errore atteso se non hai y
      matches = fs.predict(features)
      matches_df_1 = pd.DataFrame(list(matches), columns=['index_booking', 'index_agoda'])

      metodo = 'Fellegi-Sunter'
   except Exception as e:
      print('Errore ECMClassifier:', e)
      print(f'Fallback: soglia fissa > {soglia}')

      match_candidates = features[features['name_similarity'] > soglia].reset_index()
      matches_df_1 = match_candidates.rename(columns={'level_0': 'index_booking', 'level_1': 'index_agoda'})
      metodo = f'Soglia fissa > {soglia}'

   # Recupero ID e info
   matches_df_1['id_booking'] = dataframe_2.loc[matches_df_1['index_booking'], 'id_booking'].values
   matches_df_1['id_agoda'] = dataframe_1.loc[matches_df_1['index_agoda'], 'id_agoda'].values
   matches_df_1['titolo_booking'] = dataframe_2.loc[matches_df_1['index_booking'], 'titolo_booking'].values
   matches_df_1['titolo_agoda'] = dataframe_1.loc[matches_df_1['index_agoda'], 'titolo_agoda'].values
   matches_df_1['similarity'] = features.loc[list(zip(matches_df_1['index_booking'], matches_df_1['index_agoda'])), 'name_similarity'].values
   matches_df_1['pair'] = matches_df_1['id_booking'].astype(str) + '#' + matches_df_1['id_agoda'].astype(str)
   #aggiunta indirizzo
   matches_df_1['città_booking'] = dataframe_2.loc[matches_df_1['index_booking'], 'città'].values
   matches_df_1['città_agoda'] = dataframe_1.loc[matches_df_1['index_agoda'], 'città'].values
   # Aggiunta prezzi
   matches_df_1['prezzo_booking'] = dataframe_2.loc[matches_df_1['index_booking'], 'prezzo'].values
   matches_df_1['prezzo_agoda'] = dataframe_1.loc[matches_df_1['index_agoda'], 'prezzo'].values

   matches_df_1.drop(columns=["index_booking","index_agoda","name_similarity"],inplace=True)

   return matches_df_1

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
