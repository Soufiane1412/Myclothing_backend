from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup

driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

driver.get('https://eu.bape.com/collections/shark-country-pack-clothing')

page_source = driver.page_source

soup = BeautifulSoup(page_source, 'html.parser')

titles = soup.find_all('img')

for title in titles:
    print(title.get('src'))