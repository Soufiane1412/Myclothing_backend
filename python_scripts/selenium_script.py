from flask import Flask, jsonify
from selenium import webdriver
from bs4 import BeautifulSoup

app = Flask(__name__)
@app.route('/scrape')
def scrape_images():
    driver = webdriver.Firefox()
    driver.get('https://eu.bape.com/')
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    images = [img.get('src') for img in soup.find_all('img')]
    driver.quit()
    return jsonify(images)

if __name__== '__main__':
    app.run(debug=True)
