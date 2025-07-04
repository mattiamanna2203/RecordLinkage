import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Funzioni utilizzate dal bot selenium.
def click_cookie_button(driver):
    """
    Questa funzione accetta i cookies quando si accede ad agoda.
    In input prende un selenium driver.
    Sono proposti 3 metodi per accettare i cookie in modo da avere meno possibilità di errore.
    Quando i cookie sono accettati con un metodo qualsiasi la funzione si interrompe.
    
    I metodi per accettare i cookie sono incapsulati tra dei TRY & EXCEPT in modo da evitare l'interruzione della funzione in caso di errore per un metodo, così da continuare con il metodo successivo.
    """
    try:
        # Metodo di accettazione 1
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='OK']"))).click()
        print("Cookie accettati metodo 1")
        return 
    except:
        pass
    
    try:
        # Metodo di  accettazione 2
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button.BtnPair__RejectBtn"))).click()
        print("Cookie accettati con metodo 2")
        return 
    except:
        pass
    
    try:
        # Metodo di accettazione 3
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Dismiss']"))).click()
        print("Cookie accettati con metodo 3")
        return 
    except:
        pass
    


# Funzioni utilizzate dal bot selenium.
def click_avanti_button(driver):
    """
    Questa funzione si occupa di andare alla pagina successiva cliccando sul pulsante apposito.
    In input prende un selenium driver.
    
    Sono proposti 3 metodi per andare alla pagina successiva in modo da avere meno possibilità di errore.
    Quando si riesce ad andare alla pagina seguente la funzione si interrompe.
    
    I metodi per avanzare di pagina sono incapsulati tra dei TRY & EXCEPT in modo da evitare l'interruzione della funzione in caso di errore per un metodo, così da continuare con il metodo successivo.
    """    
    try:
        # Metodo di  accettazione 1
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button#paginationNext"))).click()
        print("Avanti cliccato con metodo 1")
        return 
    except:
        pass
    
    try:
        # Metodo di accettazione 2
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']"))).click()
        print("Avanti cliccato con metodo 2")
        return 
    except:
        pass
    
    try:
        # Metodo di accettazione 3
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Successiva']"))).click()
        print("Avanti cliccato con metodo 3")
        return 
    except:
        pass
    