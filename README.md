Questo progetto ha come obiettivo l'applicazione del record linkage su dati reali.  
I dati reali sono stati ottenuti tramite tecniche di **web scraping**.   

Il progetto è diviso in quattro fasi:
  1. Fase di scraping (ottentimento dati);
  2. Pulizia i dati;
  3. Record linkage;
  4. Analisi dei risultati ottenuti e delle differenze tra booking e agoda.


Dalle piattaforme  ***agoda*** e ***booking*** tramite scraping sono stati estratti dati relativi a location di diverso tipo:
- hotel
- B&B
- affitti a breve termine

Questi dati sono stati raccolti per location di Terni e di Roma.  
Successivamente tramite tecniche di **record linkage** supportate da un corretto **preprocessing** dei dati sono stati identificate e matchate le stesse location presenti sia in booking che in agoda.

Infine sono stati analizzati i dati per le location presenti in entrambi i dataset così da 
capire quale piattaforma presenta offerte migliori.   


Se si vuole riutilizzare lo script i percorsi file vanno specificati nel file **config**, mentre i pacchetti python necessari possono essere trovati nella cartella **Conda Environment**. 

Vanno modificati solo i percorsi file seguenti:

-  ***"path_selenium_driver"*** percorso file del selenium driver;

-  ***"path_progetto"*** percorso file della directory che contiene il progetto;

Invece questi percorsi file se non si rinominano o spostano cartelle/file non necessitano di 
essere modificati:

-  ***"path_scraper_agoda"*** percorso file scraper agoda;

-  ***"path_funzioni_agoda"*** percorso file della cartella contenente le funzioni per il 
   bot selenium per lo scraping del sito web agoda;

-  ***"path_scraper_booking"*** percorso file scraper booking;

-  ***"path_funzioni_booking"*** percorso file della cartella contenente le funzioni per il 
   bot selenium per lo scraping del sito web booking;

-  ***"path_data_lake"*** percorso file della cartella nella quale sono i dati grezzi;

-  ***"path_data_product"*** percorso file della cartella nella quale sono i dati  
    preprocessati e gli script per preprocessarli;

-  ***"path_results"*** percorso file della cartella nella quale i risultati vengono salvati;

-  ***"path_funzioni"*** percorso file della cartella contenente le funzioni.


