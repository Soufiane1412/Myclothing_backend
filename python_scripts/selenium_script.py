from flask import Flask, jsonify
from selenium import webdriver
from bs4 import BeautifulSoup

app = Flask(__name__)
@app.route('/scrape')
def scrape_images():
    driver = webdriver.Firefox()
    driver.get('https://www.gucci.com/us/en/ca/men/shoes-for-men/loafers-for-men-c-men-shoes-moccasins-and-loafers')
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    images = [img.get('src') for img in soup.find_all('img')]
    driver.quit()
    return jsonify(images)

if __name__== '__main__':
    app.run(debug=True)
