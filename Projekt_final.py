import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from gg.login import *
from gg.openPage import *

fakulty = [
    {'cislo': 1, 'url': 'https://apl.unob.cz/MojeAP/Fakulta/369', 'nazev': 'FVT'},
    {'cislo': 2, 'url': 'https://apl.unob.cz/MojeAP/Fakulta/633', 'nazev': 'FVL'},
    {'cislo': 3, 'url': 'https://apl.unob.cz/MojeAP/Fakulta/647', 'nazev': 'FVZ'}
]

#vypsani fakulty
print("Vyberte fakultu:")
for fakulta in fakulty:
    print(f"{fakulta['cislo']}. {fakulta['nazev']}")

#vstup od uzivatele
selected_fakulta_cislo = int(input("Zadejte číslo fakulty: "))

#platnost vyberu fakulty
selected_fakulta = None
for k in fakulty:
    if k['cislo'] == selected_fakulta_cislo:
        selected_fakulta = k
        break

if selected_fakulta:
    selected_base_url = selected_fakulta['url']

    # Pokračujte s procházením vybrané katedry
    chrome_driver_path = "C:\chromedriver.exe"
    driver = webdriver.Chrome(executable_path=chrome_driver_path)

    openPage(driver, selected_base_url)
    login(driver)
    wait = WebDriverWait(driver, 10)

    #//*[@id="KatedraList"]/div[1]/div[1]/a

    def odkazy_kateder():
        katedra_tabulka = driver.find_element(By.XPATH, '//*[@id="KatedraList"]')
        katedra_elementy = katedra_tabulka.find_elements(By.XPATH, '//a[@class="text-underline-hover text-black"]')
        #katedra_elementy = driver.find_elements(By.XPATH, '//*[@id="KatedraList"]/div[1]/div[1]/a')
        #katedra_odkazy = [katedra_elem.get_attribute("href") for katedra_elem in katedra_elementy]
        katedra_odkazy = (katedra_elem.get_attribute("href") for katedra_elem in katedra_elementy)
        katedra_odkazy = list(filter(lambda item:'Katedra' in item, katedra_odkazy))
        return katedra_odkazy

    def odkazy_vyucujici(katedra_odkazy):
        vyucujici_odkazy = []
        for katedra_odkaz in katedra_odkazy:
            driver.get(katedra_odkaz)
            print('.', end='')
            vyucujici_tabulky = driver.find_elements(By.XPATH, '//*[@id="KatedraVyucujici"]')
            for vyucujici_tabulka in vyucujici_tabulky:
                vyucujici_elementy = vyucujici_tabulka.find_elements(By.XPATH, '//a[@class="text-underline-hover text-black"]')
                vyucujici_adresy = (vyucujici_elem.get_attribute("href") for vyucujici_elem in vyucujici_elementy)
                vyucujici_adresy = list(filter(lambda item:'Vyucujici' in item, vyucujici_adresy))
                vyucujici_odkazy.extend(vyucujici_adresy)
                #vyucujici_odkazy = list(filter(lambda item:'Vyucujici' in item, vyucujici_odkazy))

        return vyucujici_odkazy
else:
    print("Neplatný výběr katedry.")

#//*[@id="frm_Nau_358"]/div[1]/div[1]/a
"""
def odkazy_predmety(vyucujici_odkazy):
    predmety_odkazy = []
    for vyucujici_odkaz in vyucujici_odkazy:
        driver.get(vyucujici_odkaz)
        print('*', end='')
        predmety_tabulky = driver.find_elements(By.XPATH, '//*[@id="accordionFlushNau"]')
        #predmety_elementy = driver.find_elements(By.XPATH, )
        for predmety_tabulka in predmety_tabulky:
            predmety_elementy = predmety_tabulka.find_elements(By.XPATH, '//a[@class="text-underline-hover text-black"]')
            predmety_adresy = (predmety_elem.get_attribute("href") for predmety_elem in predmety_elementy)
            predmety_adresy = list(filter(lambda item:'Predmety' in item, predmety_adresy))
            print(len(predmety_adresy), end='')
            predmety_odkazy.extend(predmety_adresy)
            #predmety_odkazy = list(filter(lambda item:'Predmety' in item, predmety_odkazy))
    return predmety_odkazy
"""

katedra_odkazy = odkazy_kateder()

vyucujici_odkazy = odkazy_vyucujici(katedra_odkazy)

#predmety_odkazy = odkazy_predmety(vyucujici_odkazy)

#ulozeni do JSON souboru
with open("odkazy_kateder.json", "w", encoding="utf-8") as kateder_file:
    json.dump(katedra_odkazy, kateder_file)

with open("odkazy_vyucujici.json", "w", encoding="utf-8") as vyucujici_file:
    json.dump(vyucujici_odkazy, vyucujici_file)

"""
print('test_zmeny')
print(katedra_odkazy)
print("------------------------------------------------------------------------------------------------------------------------------------")
print("------------------------------------------------------------------------------------------------------------------------------------")
print("------------------------------------------------------------------------------------------------------------------------------------")
print(vyucujici_odkazy)
print("------------------------------------------------------------------------------------------------------------------------------------")
print("------------------------------------------------------------------------------------------------------------------------------------")
print("------------------------------------------------------------------------------------------------------------------------------------")
#print(predmety_odkazy)
"""