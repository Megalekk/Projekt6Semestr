import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from gg.login import *
from gg.openPage import *

def get_subject_data(subject_url):
    driver = webdriver.Chrome()
    openPage(driver)
    #driver.get(subject_url)
    login(driver)
    wait = WebDriverWait(driver, 10)
    subject_data = {}

    subject_data['ID karty'] = int(subject_url.split("/")[-1])

    program_link = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/main/div[1]/div[1]/div[2]/div/div[1]/div']"))).get_attribute("href")
    subject_data['ID programu'] = int(program_link.split("/")[-1])

    garant_link = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@title='Vyucujici']"))).get_attribute("href")
    subject_data['ID garanta'] = int(garant_link.split("/")[-1])

    akreditace_link = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@title='Akreditace2017']"))).get_attribute("href")
    subject_data['ID předmětu v akreditaci'] = int(akreditace_link.split("/")[-1])

    topics = [item.text.strip() for item in wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='karta-text']")))]
    subject_data['Položky'] = topics

    driver.quit()
    return subject_data

def main():
    base_urls = [
        'https://apl.unob.cz/MojeAP/Fakulta/369',
        'https://apl.unob.cz/MojeAP/Fakulta/633',
        'https://apl.unob.cz/MojeAP/Fakulta/647'
    ]

    subjects_data = []

    for base_url in base_urls:
        driver = webdriver.Chrome()  # Nastavte správnou cestu ke svému webovému prohlížeči
        #driver.get(base_url)
        openPage(driver)
        login(driver)
        wait = WebDriverWait(driver, 10)
        subject_links = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[@title='Predmet']")))

        for subject_link in subject_links:
            subject_url = subject_link.get_attribute("href")
            subject_data = get_subject_data(subject_url)
            subjects_data.append(subject_data)

        driver.quit()

    with open('subjects_data.json', 'w') as json_file:
        json.dump(subjects_data, json_file, indent=2)

if __name__ == "__main__":
    main()
