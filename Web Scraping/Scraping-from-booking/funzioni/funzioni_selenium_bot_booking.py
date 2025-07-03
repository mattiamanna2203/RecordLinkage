import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Funzioni utilizzate dal bot selenium.
def click_cookie_button(driver):
    """
    Questa funzione si occupa di accettare i cookies quando si accede su booking
    """
    try:
        # Metodo di accettazione 1
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Accetto']"))).click()
        print("Cookie accettati metodo 1")
        return 
    except:
        pass
    
    try:
        # Metodo di  accettazione 2
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button#onetrust-accept-btn-handler"))).click()
        print("Cookie accettati metodo 2")
        return 
    except:
        pass




# Funzioni utilizzate dal bot selenium.
def click_caricaaltri_button(driver):
    """
    Questa funzione si occupa di accettare i cookies quando si accede su booking
    """
    try:
        # Metodo di accettazione 1
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Carica più risultati']"))).click()
        print("Carica altri risultati metodo 1")
        return 
    except:
        pass
    
    try:
        # Metodo di  accettazione 2
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button.de576f5064 b46cd7aad7 d0a01e3d83 dda427e6b5 bbf83acb81 a0ddd706cc"))).click()
        print("Carica altri risultati metodo 2")
        return 
    except:
        pass

    try:
        # Metodo di  accettazione 3
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Carica più risultati']"))).click()
        print("Carica altri risultati metodo 3")
        return 
    except:
        pass






