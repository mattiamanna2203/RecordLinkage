import re
import string
import numpy as np
import dateparser

#%%% Funzioni data product 

def alfabeto(x: str) -> str:
   """ Funzione che presa una stringa in input:
      - Ordina le parole all'interno di essa;
      - Tutte le parole minuscole;
      - Rimosso ogni carattere speciali;
      - Rimossi eventuali spazi aggiuntivi.
      Infine restituisce la stringa pulita in output.
   """
   if not isinstance(x, str):
      raise TypeError("'x' deve essere una stringa.")

   # Tutto minuscolo subito
   x = x.title()

   # Rimuovere caratteri speciali, punteggiatura & ecc...,
   # https://stackoverflow.com/questions/23996118/replace-special-characters-in-a-string-in-python
   chars = re.escape(string.punctuation)
   x = re.sub(f'[{chars}]', ' ', x)

   # Suddividere in parole
   parole = x.split()

   # Ordinare
   parole_ordinate = sorted(parole)

   # Ricomporre
   stringa = ' '.join(parole_ordinate).strip()

   return stringa

def pulisci_prezzo_per_riga(prezzo : str ) -> str :
   """Questa funzione serve per pulire la variabile prezzo.
   è una funzione creata per essere applicata ad ogni riga singolarmente.
   Ad esempio tramite -> .apply(lambda row: pulisci_prezzo(row))
   Prende il prezzo e: 
   - rimuove il simbolo dell'euro;
   - rimuove i punti come separatori delle migliaia:
   - rimuove spazi non necessari ad inizio e fine della stringa;
   - trasforma la variabile da tipo 'object' a tipo 'int'.
   """
   prezzo = prezzo.replace('€', '') # rimuove il simbolo €
   prezzo = prezzo.replace('.', '')   # rimuove i punti migliaia
   prezzo = prezzo.strip()                         # rimuove spazi
   return prezzo   

def pulisci_prezzo(colonna):
    """Questa funzione serve per pulire la variabile prezzo.
       è una funzione creata per essere applicata direttamente ad una colonna.
       Prende il prezzo e: 
         - rimuove il simbolo dell'euro;
         - rimuove i punti come separatori delle migliaia:
         - rimuove spazi non necessari ad inizio e fine della stringa;
         - trasforma la variabile da tipo 'object' a tipo 'int'.
    """
    return (
        colonna
        .str.replace('€', '', regex=False)   # rimuove il simbolo €
        .str.replace('.', '', regex=False)   # rimuove i punti migliaia
        .str.strip()                         # rimuove spazi
        .astype(int)                         # converte la stringa in un numero intero 
    )

def pulisci_recensione(riga: str) -> int :
   """ Questa funzione serve per pulire la variabile recensione.
      è una funzione creata per essere applicata direttamente ad una colonna.
      Prende il numero di recensioni: 
      - rimuove la parola 'recensioni';
      - rimuove separatore migliaia;
      - Se la recensione risulta 'novità su agoda' o  'Novità su booking' assegna 0.
   """
   # Operazioni per rendere la stringa compatibile con gli if statement.
   riga = riga.strip() # Rimozione spazi ad inizio e fine della stringa
   riga = riga.lower() # Rendere tutto il testo minuscolo  
   
   if riga == 'novità su agoda':
      return 0 
   
   elif riga == 'novità su booking':
      return 0  

   else:
      riga = riga.replace('recensioni','') # Sostituire la parola 'recensioni'
      riga = riga.replace('recensione','') # Sostituire la parola 'recensioni'
      riga = riga.replace('.','') # Rimuovere separatore migliaia
      riga = riga.strip() # Rimuovere spazi finali ed iniziali non necessari
      return int(riga) # Ritornare il valore pulito in formato int

def pulisci_distanza_centro(riga : str) -> float:
   """Funzione per estrarre la distanza dal centro, distanza specificata in km.
      Prende la stringa ove è rappresentata la distanza dal centro:
         - Se risulta 'In pieno centro' vengono specificati 0 km;
         - Rimosse le parole 'A km dal centro' oppure 'A m dal centro';
         - A volte la distanza è specificata in metri a volte in km, se in metri convertire in km;
         - Rendere la variabile float.
   """
   if not isinstance(riga,str): # Se non è una stringa la distanza non è specificata.
      return np.nan   

   # Operazioni per rendere la stringa compatibile con gli if statement.
   riga = riga.strip() # Rimozione spazi ad inizio e fine della stringa
   riga = riga.lower() # Rendere tutto il testo minuscolo  

   # Pulizia della stringa 
   if riga == 'in pieno centro':
      return 0

   elif "km" in riga: # Pulire i km
      riga =  re.sub(f'[a km dal centro]', '', riga)
      riga = riga.replace(",",".") # Se c'è la virgola come separatore dei decimali convertirla in punto perchè è il formato che python accetta
      # Conversione in float
      distanza = float(riga)     
      return distanza

   else: # Pulire i metri
      riga =  re.sub(f'[a m dal centro]', '', riga)
      riga = riga.replace(",",".") # Se c'è la virgola come separatore dei decimali convertirla in punto perchè è il formato che python accetta
      
      # Conversione in float
      distanza = float(riga)   

      # Convertire la distanza in km
      distanza = distanza / 1000      

      return distanza

def trasforma_in_data(data_str : str,
                      anno : int = None,
                      format : str  = '%d-%m-%y'):
    """Funzione che presa una data la formatta.
       Prende in input una data scritta in formato italiano, es. 1 luglio, e la trasforma  in formato YY-MM-DD, es. 2025-08-01.
       Input:
        - data (str);
        - anno (opzionale), per specificare un anno, se non specificato prende quello corrente;
        - format (opzionale), formato nel quale la data viene restituita, formato italiano di default (giorno-mese-anno).
       Output:
        - data formattata.   
    """
    # Inserire l'anno nella stringa se è specificato
    if anno:
        data_str = f"{data_str} {anno}"
        
    # Formattare la stringa
    data = dateparser.parse(data_str, languages=['it'])
    

    
    # Se la data è stata generata correttamente trasformarla in formato data tramite format specificato, altrimenti restituire None.
    if data:
        return data.strftime(format)
    else:
        return None
#%%%


#%%% Funzioni record linkage



#%%%



