import requests
from bs4 import BeautifulSoup
import os
from config import RU_CLASSES_URL

FILE = 'Категория_Грибы по алфавиту — Википедия.html'
URL = RU_CLASSES_URL


def load_url_contents_cached(url, local_file):
    # if exist read local file
    if os.path.exists(local_file):
        with open(local_file, 'r', encoding="utf-8") as f:
            contents = f.read()
    else:
        # if not exist download
        contents = requests.get(url).text

        # save in file
        with open(local_file, 'w', encoding="utf-8") as f:
            f.write(contents)
    return contents


def get_title(contents):
    soup = BeautifulSoup(contents, 'lxml')
    titles = soup.find(id="mw-pages").find_all('li')
    ru_titles = []

    for i in range(len(titles)):
        ru_titles.append(titles[i].text)

    return ru_titles


def get_wiki_species():
    content = load_url_contents_cached(URL, FILE)
    classes = get_title(content)
    classes = classes
    print('number of classes:', len(classes))

    with open('classes.txt', 'w', encoding="utf-8") as f:
        for mushroom in classes:
            f.write(mushroom + '\n')


get_wiki_species()