Questo progetto ha come obiettivo...


è diviso in tre fasi:
  - La prima fase di scraping (ottentimento dati)
  - La seconda nella quale si puliscono i dati 
  - Terza si effettua il record linkage
  - La quarta di analisi dei risultati del record linkage.



Web scraping..




Se si vuole riutilizzare lo script i percorsi file vanno specificati nel file **config**, mentre i pacchetti python necessari possono essere trovati nella cartella **Conda Environment**. 

Nel dettaglio:
- ***"path_selenium_driver"*** percorso file del selenium driver

-  ***"path_html_agoda"*** percorso file della cartella nella quale salvare gli html 
   risultato del webscraping al sito web agoda; 

-  ***"path_funzioni_agoda"*** percorso file della cartella contenente le funzioni per il 
   bot selenium per lo scraping del sito web agoda;

-  ***"path_html_booking"*** percorso file della cartella nella quale salvare gli html 
   risultato del webscraping al sito web booking; 

-  ***"path_funzioni_booking"*** percorso file della cartella contenente le funzioni per il 
   bot selenium per lo scraping del sito web booking;

-  ***"path_data_lake"*** percorso file della cartella nella quale sono i dati grezzi;

-  ***"path_data_product"*** percorso file della cartella nella quale sono i dati  
    preprocessati e gli script per preprocessarli;

-  ***"path_results"*** percorso file della cartella nella quale i risultati vengono salvati;

-  ***"path_funzioni"*** percorso file della cartella contenente le funzioni.


