DATASET_PATH = '/home/mikhail/Documents/GitHub/mushroom_classify/mushroom_dataset'

url_edible = 'https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%A1%D1%8A%D0%B5%D0%B4%D0%BE%D0%B1%D0%BD%D1%8B%D0%B5_%D0%B3%D1%80%D0%B8%D0%B1%D1%8B'
url_inedible = 'https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9D%D0%B5%D1%81%D1%8A%D0%B5%D0%B4%D0%BE%D0%B1%D0%BD%D1%8B%D0%B5_%D0%B3%D1%80%D0%B8%D0%B1%D1%8B'
RU_CLASSES_URLS = [url_edible, url_inedible]

HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 '
                  'Safari/537.36 '
}

DRIVER_PATH = "/usr/bin/chromedriver"  # chromedriver location
