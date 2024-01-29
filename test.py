import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://dora.dev/devops-capabilities/"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")


def find_links_in_page(capability_element):
    found_links = []
    for cap_element in capability_element:
        anchor_elements = cap_element.find_all('a')
        for a_elem in anchor_elements:
            href=a_elem.get('href')
            if href not in ['/research/']:
                found_links.append(href)
    return found_links

links_set = find_links_in_page(soup.find_all("section", class_="capabilitiesGrid"))
links_set=set(links_set)


def remove_tags(html):
    soup = BeautifulSoup(html, "html.parser") 
    for data in soup(['style', 'script']):
        data.decompose()
    return ' '.join(soup.stripped_strings)


def get_article_from_link(links_set):
    records = []
    for link in links_set:
        record = {}
        page_link="https://dora.dev{0}".format(link)
        page = requests.get(page_link)
        soup = BeautifulSoup(page.content, "html.parser")
        article = soup.find('article')
        article = remove_tags(str(article.contents))
        record = {link, str(article)}
        records.append(record)
    return records

records1 = pd.DataFrame.from_records(get_article_from_link(links_set))

records1.to_csv("records1.csv")
