import json
import requests
from bs4 import BeautifulSoup
from dataclasses import asdict
from tqdm import tqdm

from masterdata import FeatCard


# This function extracts the necessary data from the feat's page
def scrape_feat_card_details(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    card_wrapper = soup.find('div', class_='card-wrapper')

    title_span = card_wrapper.find('span', {'data-copy': True})
    title, title_en = title_span.text.split(' [')
    title_en = title_en.strip(']')

    description_div = card_wrapper.find('div', itemprop='description')
    description = description_div.text.strip()

    requirements_li = card_wrapper.find('li', class_='size-type-alignment')
    requirements = requirements_li.text.strip() if requirements_li else None

    source_span = card_wrapper.find('span', class_='source-plaque')
    source = source_span['title'] if source_span else None

    return FeatCard(title, url, title_en, requirements, description, source)


def main():
    url = "https://dnd.su/feats/"
    resp = requests.get(url)

    soup = BeautifulSoup(resp.text, 'html.parser')
    feats_html = soup.find_all('div', class_='col list-item__spell for_filter')

    feat_cards = []
    for feat_html in tqdm(feats_html):
        url = "https://dnd.su" + feat_html.a['href']
        feat_card = scrape_feat_card_details(url)
        feat_cards.append(feat_card)

    with open('feats.json', 'w', encoding='utf-8') as f:
        json.dump([asdict(card) for card in feat_cards], f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()
