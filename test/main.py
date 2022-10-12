
import requests
import urllib
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
    response = get_source("https://www.google.co.uk/search?q=" + query)

    links = list(response.html.absolute_links)
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

    return links


def parse_results(response):
    css_identifier_result = ".tF2Cxc"
    css_identifier_title = "h3"
    css_identifier_link = ".yuRUbf a"
    css_identifier_text = ".VwiC3b"

    results = response.html.find(css_identifier_result)

    output = []

    for result in results:
        item = {
            'title': result.find(css_identifier_title, first=True).text,
            'link': result.find(css_identifier_link, first=True).attrs['href'],
        }

        output.append(item)

    return output


def get_results(query,n):

    if n>0:
        query = urllib.parse.quote_plus(query+"&start="+str(n))
        response = get_source("https://www.google.com/search?q=" + query + "&start="+str(n))
        # print("https://www.google.com/search?q=" + query+"&start="+str(n))
    else:
        query = urllib.parse.quote_plus(query)
        response = get_source("https://www.google.com/search?q=" + query)
        # print("https://www.google.com/search?q=" + query)

    return response

def google_search(query,n):
    response = get_results(query,n)
    return parse_results(response)


f = open("data.txt","w")

com = 0
for m in range(5):
    results = google_search("cybersecurity news",10*m)
    for i in results:
        for j,k in i.items():
            f.write(j+" : "+k+"\n")
        f.write("\n\n")
        com+=1
print(com)

for m in range(5):
    results = google_search("cybersecurite info",10*m)
    for i in results:
        for j,k in i.items():
            f.write(j+" : "+k+"\n")
        f.write("\n\n")
        com+=1
print(com)
