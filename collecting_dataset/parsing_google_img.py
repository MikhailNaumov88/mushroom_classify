import logging
import os
import random
import time
import urllib.error
import urllib.request
from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from user_agent import generate_user_agent

from config import DRIVER_PATH, DATASET_PATH


def make_dataset_dir(link_path):
    link_file_path = link_path + 'links/'
    download_dir = link_path + 'dataset/'
    if not os.path.exists(link_file_path):
        os.makedirs(link_file_path)

    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    return link_file_path, download_dir


def get_image_links(query, link_file_path, num_requested=100):
    query = query
    google_query = '+'.join(query.split())
    page = "https://www.google.co.in/search?q=" + '"' + google_query + '"' + "&source=lnms&tbm=isch"
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(executable_path=DRIVER_PATH, chrome_options=options)
    driver.get(page)
    img_urls = set()

    # scroll google images gallery
    number_of_scrolls = int(num_requested / 400) + 1
    for _ in range(number_of_scrolls):
        for __ in range(10):
            # multiple scrolls needed to show all 400 images
            driver.execute_script("window.scrollBy(0, 1000000)")
            time.sleep(2)
        # to load next 400 images
        time.sleep(1)
        try:
            driver.find_element(By.CLASS_NAME, "mye4qd").click()
        except Exception as e:
            print("Process-{0} reach the end of page or get the maximum number of requested images".format(query))
            break

    # find all img url

    # thumbs = driver.find_element(By.XPATH, '//a[@class="wXeWr islib nfEiy mM5pbd"]')
    thumbs = driver.find_element(By.CSS_SELECTOR, 'img.Q4LuWd')
    # thumbs.size

    # print(len(thumbs))
    for thumb in thumbs:
        try:
            thumb.click()
            time.sleep(random.randint(1, 6))
        except Exception as e:
            print("Error clicking one thumbnail")

        url_elements = driver.find_element(By.XPATH, '//img[@class="n3VNCb"]')
        for url_element in url_elements:
            try:
                url = url_element.get_attribute('src')
            except e:
                print("Error getting one url")
            if url.startswith('http') and not url.startswith('https://encrypted-tbn0.gstatic.com'):
                img_urls.add(url)
                print("Found image url: " + url)

    driver.quit()
    link_path = link_file_path + '_'.join(query.split()) + '_links.txt'
    with open(link_path, 'w') as wf:
        for url in img_urls:
            wf.write(url + '\n')
    print('Store all the links in file {0}'.format(link_path))

    len(img_urls)
    return link_path


def img_downloading(query, link_file, download_dir, prefix):
    count = 0
    headers = {}

    img_dir = download_dir + '_'.join(query.split()) + '/'
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)

    # start to download images
    with open(link_file, 'r') as rf:
        for link in rf:
            try:
                o = urlparse(link)
                ref = o.scheme + '://' + o.hostname
                ua = generate_user_agent()
                headers['User-Agent'] = ua
                headers['referer'] = ref
                print('\n{0}\n{1}\n{2}'.format(link.strip(), ref, ua))
                req = urllib.request.Request(link.strip(), headers=headers)
                response = urllib.request.urlopen(req)
                data = response.read()
                file_path = img_dir + '{0}_{1}.jpg'.format(prefix, count)
                with open(file_path, 'wb') as wf:
                    wf.write(data)

                count += 1
                if count % 10 == 0:
                    print('Process-{0} is sleeping'.format(query))
                    time.sleep(random.randint(4, 10))

            except urllib.error.HTTPError as e:
                print('HTTPError')
                logging.error(
                    'HTTPError while downloading image {0}http code {1}, reason:{2}'.format(link, e.code, e.reason))
                continue
            except urllib.error.URLError as e:
                print('URLError')
                logging.error('URLError while downloading image {0}reason:{1}'.format(link, e.reason))
                continue
            except Exception as e:
                print('Unexpected Error')
                logging.error(
                    'Unexpeted error while downloading image {0}error type:{1}, args:{2}'.format(link, type(e), e.args))
                continue


if __name__ == "__main__":

    dataset_dir = DATASET_PATH
    # Russian bird specias dataset for classification
    classes = []
    ru_classes = 'classes.txt'  # file with russian mushroom names
    with open(ru_classes, 'r') as f:
        for mushroom in f:
            classes.append(mushroom)

    # print(len(species))
    link_file_path, download_dir = make_dataset_dir(dataset_dir)

    have_mushroom = [' '.join(x.split('_')) for x in os.listdir(download_dir)]

    for mushroom in classes[1:]:
        if mushroom[:-1] not in have_mushroom:
            link_file = get_image_links(mushroom, link_file_path, num_requested=401)
            img_downloading(mushroom, link_file, download_dir, '0_')




