# Descrizione del progetto

## Obiettivo
Questo progetto ha come obiettivo l'applicazione del record linkage su dati reali.  
I dati reali sono stati ottenuti tramite tecniche di **web scraping**.   

## Pipeline del progetto
Il progetto è diviso in quattro fasi:
  1. Fase di scraping (ottentimento dati);
  2. Pulizia i dati;
  3. Record linkage;
  4. Analisi dei risultati ottenuti e delle differenze tra booking e agoda.

### 1. Fase di scraping (ottentimento dati);

Dalle piattaforme  ***agoda*** e ***booking*** tramite scraping sono stati estratti dati relativi a location di diverso tipo:
- hotel
- B&B
- affitti a breve termine

Questi dati sono stati raccolti per location di Terni e di Roma.  

### 2,3 Fase di pulizia dati e record linkage
Successivamente tramite tecniche di **record linkage** supportate da un corretto **preprocessing** dei dati sono stati identificate e matchate le stesse location presenti sia in booking che in agoda.

### 4. Analisi dei risultati

Infine sono stati analizzati i dati per le location presenti in entrambi i dataset così da 
capire quale piattaforma presenta offerte migliori.   



# Descrizione delle cartelle e dei file

```
├── AnalisiRisultati.ipynb  # 
├── Conda Environment
├── Data Lake
├── Data Product
├── Funzionamento_jarowinkler_jellyfish.ipynb
├── Funzioni
├── OriginaleLinkage.ipynb
├── Presentazione
├── README.md
├── RecordLinkage.ipynb
├── Results
├── Web Scraping
└── config.json
```


Più nel dettaglio:

```
.
├── .DS_Store
├── .gitattributes
├── .gitignore
├── AnalisiRisultati.ipynb
├── Conda Environment
│   ├── create_env.sh
│   ├── download_selenium_driver.md
│   └── setup-env.yml
├── Data Lake
│   ├── agoda_Roma.csv
│   ├── agoda_Terni.csv
│   ├── booking_Roma.csv
│   └── booking_Terni.csv
├── Data Product
│   ├── Cleaning_pipeline.ipynb
│   ├── agoda.csv
│   ├── booking.csv
│   └── funzioni.py
├── Funzionamento_jarowinkler_jellyfish.ipynb
├── Funzioni
│   ├── .DS_Store
│   └── funzioni.py
├── OriginaleLinkage.ipynb
├── Presentazione
│   ├── Record linkage.ppt
│   └── Slide.ppt
├── README.md
├── RecordLinkage.ipynb
├── Results
│   ├── matches_titolo_095.csv
│   └── matches_titolo_095_città_08.csv
├── Web Scraping
│   ├── .DS_Store
│   ├── Scraping-from-Agoda
│   │   ├── .DS_Store
│   │   ├── 01)_Get_HTML.ipynb
│   │   ├── 02)_Get_Info.ipynb
│   │   ├── funzioni
│   │   │   └── funzioni_selenium_bot_agoda.py
│   │   └── html
│   │       ├── .DS_Store
│   │       ├── html_final_pagina1.txt
│   │       └── html_final_pagina2.txt
│   └── Scraping-from-booking
│       ├── .DS_Store
│       ├── 01)_Get_HTML.ipynb
│       ├── 02)_Get_Info.ipynb
│       ├── funzioni
│       │   └── funzioni_selenium_bot_booking.py
│       └── html
│           └── html_final.txt
└── config.json
```





# Riutilizzare il codice

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




