import pytest
from flask import Flask
from selenium_script import app

def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client