import requests
from bs4 import BeautifulSoup
import json

def get_subject_data(subject_url):
    response = requests.get(subject_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    subject_data = {}
    
    subject_data['ID karty'] = int(subject_url.split("/")[-1])
    
    program_link = soup.find('a', {'title': 'Program'})['href']
    subject_data['ID programu'] = int(program_link.split("/")[-1])
    
    garant_link = soup.find('a', {'title': 'Garant'})['href']
    subject_data['ID garanta'] = int(garant_link.split("/")[-1])
    
    akreditace_link = soup.find('a', {'title': 'Link na akreditaci'})['href']
    subject_data['ID předmětu v akreditaci'] = int(akreditace_link.split("/")[-1])
    
    topics = [item.text.strip() for item in soup.find_all('div', {'class': 'karta-text'})]
    subject_data['Položky'] = topics
    
    return subject_data

def main():
    base_urls = [
        'https://apl.unob.cz/MojeAP/Fakulta/369',
        'https://apl.unob.cz/MojeAP/Fakulta/633',
        'https://apl.unob.cz/MojeAP/Fakulta/647'
    ]
    
    subjects_data = []
    
    for base_url in base_urls:
        response = requests.get(base_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        subject_links = soup.find_all('a', {'title': 'Předmět'})
        
        for subject_link in subject_links:
            subject_url = subject_link['href']
            subject_data = get_subject_data(subject_url)
            subjects_data.append(subject_data)
    
    with open('subjects_data.json', 'w') as json_file:
        json.dump(subjects_data, json_file, indent=2)

if __name__ == "__main__":
    main()
