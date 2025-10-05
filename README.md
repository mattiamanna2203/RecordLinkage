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



# Descrizione delle cartelle e dei file

## Tree 



```
├── AnalisiRisultati.ipynb  # Python notebook per analizzare i risultati del record linkage
├── Conda Environment       # Cartella contenente informazioni sui pacchetti python e driver 
                              # necessari per il corretto funzionamento del progetto
├── Data Lake               # Folder contenente i dati grezzi
├── Data Product            # Folder contenente dati puliti e script che li hanno puliti
├── Funzionamento_jarowinkler_jellyfish.ipynb # Python notebook per capire il funzionamento di
                                              # jarowinkler e jellyfish (record linkage)     
├── Funzioni                # Folder contenente le funzioni necessari per il record linkage
├── README.md               # File readme che si sta leggendo in questo momento
├── RecordLinkage.ipynb     # Python notebook per applicare le tecniche di record linkage 
├── Results                 # Folder ove salvare i risultati del record linkage
├── Web Scraping            # Folder contenenti le funzioni ed i bot selenium per effettuare 
                              # il web scraping
└── config.json             # File json contenente i path necessari per il corretto    
                              # funzionamento degli script
```


### Tre più nel dettaglio

```
.
├── AnalisiRisultati.ipynb # Python notebook per analizzare i risultati del record linkage
├── Conda Environment      # Cartella contenente informazioni sui pacchetti python e driver 
                              # necessari per il corretto funzionamento del progetto
│   ├── create_env.sh      # bash script  per la creazione del conda environment necessario  
                           # per un corretto funzionamento di python
│   ├── download_selenium_driver.md # Informazioni su come effettuare il download del giusto 
                                    # selenium chrome driver 
│   └── setup-env.yml      # Lista dei pacchetti python necessari nel conda environment 
├── Data Lake              # Folder contenente i dati grezzi
│   ├── agoda_Roma.csv     # Dataframe contenente location relative a roma sulla piattaforma agoda
│   ├── agoda_Terni.csv    # Dataframe contenente location relative a terni sulla piattaforma agoda
│   ├── booking_Roma.csv   # Dataframe contenente location relative a roma sulla piattaforma booking
│   └── booking_Terni.csv  # Dataframe contenente location relative a terni sulla piattaforma booking
├── Data Product           # Folder contenente dati puliti e script che li hanno puliti
│   ├── Cleaning_pipeline.ipynb # Python notebook per preprocessare i dati 
│   ├── agoda.csv               # Dati preprocessati per la piattaforma agoda
│   ├── booking.csv             # Dati preprocessati per la piattaforma booking
│   └── funzioni.py             # Funzioni per il preprocessing dei dati
├── Funzionamento_jarowinkler_jellyfish.ipynb # Python notebook per capire il funzionamento di
                                                # jarowinkler e jellyfish (record linkage)     
├── Funzioni               # Folder contenente le funzioni necessari per il record linkage
│   └── funzioni.py        # funzioni
├── README.md              # File readme che si sta leggendo in questo momento
├── RecordLinkage.ipynb    # Python notebook per applicare le tecniche di record linkage 
├── Results                # Folder ove salvare i risultati del record linkage
│   ├── matches_titolo_095.csv          # match ottenuti utilizzando solo la variabile titolo
│   └── matches_titolo_095_città_08.csv # match ottenuti utilizzando la variabile 
                                          # titolo e città
├── Web Scraping           # Folder contenenti le funzioni ed i bot selenium per effettuare 
                              # il web scraping
│   ├── Scraping-from-Agoda # Contiente il bot per lo scraping al sito agoda
│   │   ├── 01)_Get_HTML.ipynb # Python notebook per l'ottenimento degli html tramite bot selenium
│   │   ├── 02)_Get_Info.ipynb # Python notebook per l'estrazione dati dagli html
│   │   ├── funzioni # Folder contenente le funzioni per il funzionamento del bot selenium per agoda
│   │   │   └── funzioni_selenium_bot_agoda.py 
│   │   └── html # Folder nel quale salvare gli html ottenuti tramite scraping
│   │       ├── html_final_pagina1.txt
│   │       └── html_final_pagina2.txt
│   └── Scraping-from-booking  # Contiente il bot per lo scraping al sito booking
│       ├── 01)_Get_HTML.ipynb # Python notebook per l'ottenimento degli html tramite bot selenium
│       ├── 02)_Get_Info.ipynb # Python notebook per l'estrazione dati dagli html
│       ├── funzioni # Folder contenente le funzioni per il funzionamento del bot selenium per booking
│       │   └── funzioni_selenium_bot_booking.py
│       └── html # Folder nel quale salvare gli html ottenuti tramite scraping
│           └── html_final.txt
└── config.json              # File json contenente i path necessari per il corretto    
                              # funzionamento degli script
```