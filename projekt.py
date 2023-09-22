import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from gg.login import *
from gg.openPage import *

base_urls = [
        'https://apl.unob.cz/MojeAP/Fakulta/369',
        #'https://apl.unob.cz/MojeAP/Fakulta/633',
        #'https://apl.unob.cz/MojeAP/Fakulta/647'
    ]




for base_url in base_urls:
        driver = webdriver.Chrome()  

        #driver.get(base_url)
        openPage(driver,base_url)
        login(driver)
        wait = WebDriverWait(driver, 10)

katedra_odkazy=[]
vyucujici_odkazy=[]

def odkazy_kateder():
    global katedra_odkazy
    katedra_tabulka_1 = driver.find_element(By.XPATH, '//*[@id="KatedraList"]')
    katedra_elem = katedra_tabulka_1.find_elements(By.XPATH, '//a[@class="text-underline-hover text-black"]')
    katedra_odkazy = [katedra_elem.get_attribute("href") for katedra_elem in katedra_elem]
    return katedra_odkazy


def odkazy_vyucujici():
    global vyucujici_odkazy
    vyucujici_tabulka_1 = katedra_odkazy.find_elements(By.XPATH, '//*[@id="KatedraVyucujici"]')
    vyucujici_elementy = vyucujici_tabulka_1.find_elements(By.CLASS_NAME, '//a[@class="text-underline-hover text-black"]')
    vyucujici_odkazy = [vyucujici_elem.get_attribute("href") for vyucujici_elem in vyucujici_elementy]
    vyucujici_odkazy += vyucujici_odkazy
    return vyucujici_odkazy

odkazy_kateder()
odkazy_vyucujici()
print(katedra_odkazy)
print("-----------")
print("-----------")
print(vyucujici_odkazy)