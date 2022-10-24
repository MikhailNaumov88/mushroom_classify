import json
from bs4 import BeautifulSoup
import os
import requests
import time

page = 'https://ru.wikipedia.org/wiki/'  # Wikipedia page

with open('classes.txt', 'r', encoding='utf-8') as f:
    classes = f.read()
    classes = classes.split('\n')


def clear_classes(list_to_clear):
    '''
    :param list_to_clear: Take the list with russian classes
    :return: cleared list of classes
    removing incorrect elements by index defined manually
    '''
    ind_remove = [75, 76, 116, 129, 170, 231, 235, 237,
                  347, 355, 368, 405, 392, 609, 610, 613,
                  614, 615, 617, 620]
    cleared_list = [i for j, i in enumerate(list_to_clear) if j not in ind_remove]
    return cleared_list


def get_lat_ru_dict(classes):
    classes = clear_classes(classes)

    ru_lat_dict = {}
    count = 0

    if os.path.exists('ru_lat_dict.json'):
        with open('ru_lat_dict.json') as f:
            ru_lat_dict = json.load(f)
    else:
        ru_lat_dict = {}
        count = 0

        for mush in classes:
            src = requests.get(page + mush.replace(' ', '_')).text
            soup = BeautifulSoup(src, 'lxml')
            # print(soup)

            try:
                lat_name = soup.find_all("td", class_='plainlist')
                lat_name = lat_name[1].find('i').text
            except:
                try:
                    lat_name = soup.find(class_='infobox').find_all('span')[1].text
                except:
                    lat_name = 'Undefined'

            if lat_name == '':
                try:
                    lat_name = soup.find_all(class_="wikidata-snak wikidata-main-snak")[1].text
                except:
                    lat_name = 'Undefined'

            if lat_name.isnumeric():
                try:
                    lat_name = soup.find(class_='infobox').find_all('span')[2].text
                except:
                    lat_name = 'Undefined'

            print(lat_name, count)
            count += 1
            ru_lat_dict[lat_name] = mush
            time.sleep(1)
        ru_lat_dict.pop('Undefined')

        with open('ru_lat_dict.json', 'w') as f:
            json.dump(ru_lat_dict, f, indent=4, ensure_ascii=False)
    try:
        ru_lat_dict.pop('Undefined')
        print('Dictionary is ready')
    except KeyError:
        print('Dictionary is ready')

    return ru_lat_dict


if __name__ == "__main__":

    ru_lat_dict = get_lat_ru_dict(classes)
