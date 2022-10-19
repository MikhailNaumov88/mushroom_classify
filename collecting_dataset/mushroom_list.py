import requests
from bs4 import BeautifulSoup
import os
from config import RU_CLASSES_URLS, HEADERS

FILES = ['edible.html', 'inedible.html']
URLS = RU_CLASSES_URLS


def load_url_contents_cached(urls, local_files):
    contents = []
    for url, local_file, i in zip(urls, local_files, range(len(local_files))):
        # if exist read local file
        if os.path.exists(local_file):
            with open(local_file, 'r', encoding="utf-8") as f:
                contents.append(f.read())
        else:
            # if not exist download
            contents.append(requests.get(url).text)

            # save in file
            with open(local_file, 'w', encoding="utf-8") as f:
                f.write(contents[i])
    return contents


def get_title(contents):
    list_classes = []
    for content in contents:
        classes = []

        soup = BeautifulSoup(content, 'lxml')
        ru_classes = soup.find(id="mw-pages").find_all('li')
        next_link = 'https://ru.wikipedia.org' + soup.find('a', text='Следующая страница').get('href')

        for item in ru_classes:
            classes.append(item.text)

        soup = BeautifulSoup(requests.get(next_link, headers=HEADERS).text, 'lxml')
        ru_classes1 = soup.find(id="mw-pages").find_all('li')

        for item in ru_classes1:
            classes.append(item.text)

        list_classes.append(classes)

    list_classes[0] = list_classes[0][2:]

    return list_classes


def get_wiki_species():
    content = load_url_contents_cached(URLS, FILES)
    list_classes = get_title(content)
    # classes = classes
    print('number of edible classes:', len(list_classes[0]))
    print('number of inedible classes:', len(list_classes[1]))
    print('number of total classes:', len([*list_classes[0], *list_classes[1]]))

    with open('edible.txt', 'w', encoding="utf-8") as f:
        for mushroom in list_classes[0]:
            f.write(mushroom + '\n')

    with open('inedible.txt', 'w', encoding="utf-8") as f:
        for mushroom in list_classes[1]:
            f.write(mushroom + '\n')

    with open('classes.txt', 'w', encoding="utf-8") as f:
        for mushroom in [*list_classes[0], *list_classes[1]]:
            f.write(mushroom + '\n')


get_wiki_species()
