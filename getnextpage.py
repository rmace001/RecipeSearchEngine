import requests
from bs4 import BeautifulSoup
from glob import glob
from os.path import join
from urllib.parse import urljoin
def get_the_link_cuisine(url):
    linklist = []
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, 'html.parser')
    pageURL = url + "?page="
    with requests.Session() as session:
        page_number = 1
        # url = 'https://securityadvisories.paloaltonetworks.com/Home/Index/?page='
        # url = 'https://www.seriouseats.com/recipes/topics/cuisine/american?page='
        while True:
            next_l = None
            #print("Processing page: #{page_number}; url: {url}".format(page_number=page_number, url=pageURL))
            linklist.append(pageURL)
            response = session.get(pageURL) 
            soup = BeautifulSoup(response.content, 'html.parser')
            # print(soup)
            # check if there is next page, break if not
            for item in soup.find_all('link', rel = 'next'):#<link href="https://www.seriouseats.com/recipes/topics/cuisine/american?page=2" rel="next"/>
                next_l = item['href']
            if next_l is None:
                break
            pageURL = urljoin(url, next_l)
            page_number += 1
    return linklist
url = "https://www.seriouseats.com/recipes/topics/cuisine/american"
print(get_the_link_cuisine(url))