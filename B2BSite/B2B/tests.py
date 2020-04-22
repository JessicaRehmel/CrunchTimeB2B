#from django.test import TestCase

import requests

if __name__ == "__main__":
    requests.post('http://localhost:8000/B2B/search_books/', data={'username':'admin', 'password':'password', 'queries':"[{\"author\": \"\", \"title\": \"Cows\", \"isbn\": \"\"}]"})
