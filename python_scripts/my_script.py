import requests
from bs4 import BeautifulSoup


url='https://books.toscrape.com'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

titles = soup.find_all('h3', 'a')
for title in titles:
    print(title.text)