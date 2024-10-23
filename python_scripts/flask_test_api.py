import pytest 
from flask import Flask
from selenium_script import app


def client():
    app.config('TESTING') == True 
    with app.test_client() as client:
        yield client

def test_scrape_endpoint():
    response = client.get('/scrape')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    