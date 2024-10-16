import requests
from bs4 import BeautifulSoup


url='http://books.toscrape.com/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

titles = soup.find_all('h3')

for title in titles:
    a_tag = title.find('a')
    if a_tag:
        bookText = a_tag.get('title')
        url = a_tag.get('href')
        print(f"bookText: {title}, url:{url}")