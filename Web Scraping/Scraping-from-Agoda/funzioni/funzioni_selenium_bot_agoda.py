import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Funzioni utilizzate dal bot selenium.
def click_cookie_button(driver):
    """
    Questa funzione si occupa di accettare i cookies quando si accede ad agoda
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
        print("Cookie accettati metodo 2")
        return 
    except:
        pass
    
    try:
        # Metodo di accettazione 1
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Dismiss']"))).click()
        print("Cookie accettati metodo 1")
        return 
    except:
        pass
    


# Funzioni utilizzate dal bot selenium.
def click_avanti_button(driver):
    """
    Questa funzione si occupa di andare alla pagina successiva
    """    
    try:
        # Metodo di  accettazione 2
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button#paginationNext"))).click()
        print("Avanti cliccato metodo 1")
        return 
    except:
        pass
    
    try:
        # Metodo di accettazione 3
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']"))).click()
        print("Avanti cliccato metodo 2")
        return 
    except:
        pass
    
    try:
        # Metodo di accettazione 3
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Successiva']"))).click()
        print("Avanti cliccato metodo 3")
        return 
    except:
        pass
    