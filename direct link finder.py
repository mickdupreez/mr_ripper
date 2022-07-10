import re
from webbrowser import get
import requests
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession



def get_source(url):
    """Return the source code for the provided URL. 

    Args: 
        url (string): URL of the page to scrape.

    Returns:
        response (object): HTTP response object from requests_html. 
    """

    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)


def scrape_google(query):

    query = urllib.parse.quote_plus(query)
    responses = get_source("https://www.google.com/search?q="+query)
    print(responses)
    links = list(responses.html.absolute_links)
    
    google_domains = ('https://www.google.', 
                      'https://google.', 
                      'https://webcache.googleusercontent.', 
                      'http://webcache.googleusercontent.', 
                      'https://policies.google.',
                      'https://support.google.',
                      'https://maps.google.')

    for url in links[:]:
        if url.startswith(google_domains):
            links.remove(url)
    for url in links[:]:
        if not url.endswith("/"):
            links.remove(url)
    return links

print(scrape_google("Suicide Squad movie imdb"))