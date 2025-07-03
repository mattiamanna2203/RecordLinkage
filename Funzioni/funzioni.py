import re
import string

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
   x = x.lower()

   # Rimuovere caratteri speciali, punteggiatura & ecc...,
   # https://stackoverflow.com/questions/23996118/replace-special-characters-in-a-string-in-python
   chars = re.escape(string.punctuation)
   x = re.sub(f'[{chars}]', '', x)

   # Suddividere in parole
   parole = x.split()

   # Ordinare
   parole_ordinate = sorted(parole)

   # Ricomporre
   stringa = ' '.join(parole_ordinate).strip()

   return stringa