import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from gg.login import *
from gg.openPage import *

base_urls = [
        'https://apl.unob.cz/MojeAP/Fakulta/369',
    ]


for base_url in base_urls:
        driver = webdriver.Chrome()  

        #driver.get(base_url)
        openPage(driver,base_url)
        login(driver)
        wait = WebDriverWait(driver, 10)


def odkazy_kateder():
    katedra_elementy = driver.find_elements(By.XPATH, '//*[@id="KatedraList"]/div[1]/div[1]/a')
    katedra_odkazy = [katedra_elem.get_attribute("href") for katedra_elem in katedra_elementy]
    return katedra_odkazy

def odkazy_vyucujici(katedra_odkazy):
    vyucujici_odkazy = []
    for katedra_odkaz in katedra_odkazy:
        driver.get(katedra_odkaz)
        vyucujici_tabulky = driver.find_elements(By.XPATH, '//*[@id="KatedraVyucujici"]')
        for vyucujici_tabulka in vyucujici_tabulky:
            vyucujici_elementy = vyucujici_tabulka.find_elements(By.XPATH, '//a[@class="text-underline-hover text-black"]')
            vyucujici_odkazy.extend([vyucujici_elem.get_attribute("href") for vyucujici_elem in vyucujici_elementy])

    return vyucujici_odkazy


katedra_odkazy = odkazy_kateder()

vyucujici_odkazy = odkazy_vyucujici(katedra_odkazy)

print(katedra_odkazy)
print("------------------------------------------------------------------------------------------------------------------------------------")
print("------------------------------------------------------------------------------------------------------------------------------------")
print("------------------------------------------------------------------------------------------------------------------------------------")
print(vyucujici_odkazy)





