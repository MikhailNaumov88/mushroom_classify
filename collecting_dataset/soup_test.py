from bs4 import BeautifulSoup

with open('Категория_Грибы по алфавиту — Википедия.html') as file:
    src = file.read()

soup = BeautifulSoup(src, 'lxml')

ru_classes = soup.find(id="mw-pages").find_all('li')

for item in ru_classes:
    print(item.text)
