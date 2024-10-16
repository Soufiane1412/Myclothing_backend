import requests
from bs4 import BeautifulSoup


url='https://www.zalando.fr/chaussures-femme/?camp=fr_mss_premiumdesigner_fs_aw24/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

images = soup.find_all('img')

for image in images:
    img = image.get('src')
    print(f"Image:{img}")
