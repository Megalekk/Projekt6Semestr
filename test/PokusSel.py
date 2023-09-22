import time
import json
from selenium import webdriver

# Funkce pro extrakci dat z karty predmetu
def extract_subject_info(subject_url):
    driver.get(subject_url)
    time.sleep(3)  # Počkejme chvilku, než se načtou data
    subject_id = subject_url.split("/")[-1]

    subject_info = {
        "ID karty": subject_id,
        "ID programu": extract_id_from_link(driver.find_element_by_xpath("//a[@class='btn btn-outline-primary btn-sm' and contains(text(), 'Program')]")),
        "ID garanta": extract_id_from_link(driver.find_element_by_xpath("//a[@class='btn btn-outline-info btn-sm' and contains(text(), 'Garant')]")),
        "ID předmětu v akreditaci": extract_id_from_link(driver.find_element_by_xpath("//a[@class='btn btn-outline-secondary btn-sm' and contains(text(), 'Link na akreditaci')]")),
        "Položky": extract_items(),
    }
    return subject_info

# Funkce pro extrakci ID z odkazu
def extract_id_from_link(element):
    link = element.get_attribute("href")
    return link.split("/")[-1]

# Funkce pro extrakci seznamu témat
def extract_items():
    items = []
    elements = driver.find_elements_by_xpath("//div[@class='card-body']/div/ul/li")
    for element in elements:
        item = element.text.strip()
        items.append(item)
    return items

# Hlavní funkce pro provedení analýzy všech stránek
def analyze_pages(urls):
    results = []
    for url in urls:
        driver.get(url)
        time.sleep(3)  # Počkejme chvilku, než se načtou data
        department_elements = driver.find_elements_by_xpath("//a[@class='btn btn-outline-primary btn-sm' and contains(text(), 'Katedra')]")
        for department_element in department_elements:
            department_link = department_element.get_attribute("href")
            people_url = department_link.replace("/MojeAP/Katedra", "/MojeAP/Lide")
            driver.get(people_url)
            time.sleep(3)  # Počkejme chvilku, než se načtou data
            person_elements = driver.find_elements_by_xpath("//a[@class='btn btn-outline-primary btn-sm' and contains(text(), 'Osoba')]")
            for person_element in person_elements:
                person_link = person_element.get_attribute("href")
                subjects_url = person_link.replace("/MojeAP/Osoba", "/MojeAP/Predmet")
                driver.get(subjects_url)
                time.sleep(3)  # Počkejme chvilku, než se načtou data
                subject_elements = driver.find_elements_by_xpath("//a[@class='btn btn-outline-primary btn-sm' and contains(text(), 'Předmět')]")
                for subject_element in subject_elements:
                    subject_link = subject_element.get_attribute("href")
                    subject_info = extract_subject_info(subject_link)
                    results.append(subject_info)
    return results

if __name__ == "__main__":
    # Zde zadáme výchozí URL pro analýzu
    starting_urls = [
        "https://apl.unob.cz/MojeAP/Fakulta/369",
        "https://apl.unob.cz/MojeAP/Fakulta/633",
        "https://apl.unob.cz/MojeAP/Fakulta/647"
    ]

    # Spustíme prohlížeč
    driver = webdriver.Chrome()

    # Provedeme analýzu stránek a získáme výsledky
    results = analyze_pages(starting_urls)

    # Ukončíme prohlížeč
    driver.quit()

    # Uložíme výsledky do JSON souboru
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("Extrakce dat dokončena. Výsledky byly uloženy do souboru 'results.json'.")
