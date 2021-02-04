import requests
from bs4 import BeautifulSoup
import json
from glob import glob
from os.path import join
from urllib.parse import urljoin


def get_all_cuisne(url):
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, 'html.parser')
    save_temp = []
    for item in soup.find_all("ul", class_="c-category-flex__nav-listing"):
        for a in item.find_all('a', {'href': True}):
            save_temp.append(a['href'])
    return(save_temp)


def get_the_link_cuisine(url):
    linklist = []
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, 'html.parser')
    pageURL = url + "?page="
    with requests.Session() as session:
        page_number = 1
        # url = 'https://www.seriouseats.com/recipes/topics/cuisine/american?page='
        while True:
            next_l = None
            # print("Processing page: #{page_number}; url: {url}".format(page_number=page_number, url=pageURL))
            linklist.append(pageURL)
            response = session.get(pageURL)
            soup = BeautifulSoup(response.content, 'html.parser')
            # print(soup)
            # check if there is next page, break if not
            # <link href="https://www.seriouseats.com/recipes/topics/cuisine/american?page=2" rel="next"/>
            for item in soup.find_all('link', rel='next'):
                next_l = item['href']
            if next_l is None:
                break
            pageURL = urljoin(url, next_l)
            page_number += 1
    return linklist


# baseurl = "https://www.seriouseats.com/recipes/topics/cuisine/"
# cusineurl = baseurl + "American"
# print(cusineurl)
# print(get_the_link_cuisine(cusineurl))
main_cuisne_menu = 'https://www.seriouseats.com/recipes/topics/cuisine'
cusineurl_list = get_all_cuisne(main_cuisne_menu)
# print(cusineurl_list)
main_list = []
for cusine_name in cusineurl_list:
    main_list.append(get_the_link_cuisine(cusine_name))


def getWebData(url):
    pageData = {}
    print(url)
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    pageData['recipeLink'] = url
    pageData['recipeTitle'] = soup.find(
        'h1', class_='title recipe-title c-post__h1').text
    if soup.find('aside', class_='callout callout-bottom callout-bottom-recipe recipe-equipment') != None:
        specialEquipment = soup.find(
            'aside', class_='callout callout-bottom callout-bottom-recipe recipe-equipment')
        if specialEquipment.find('span', class_='info') != None:
            pageData['specialEquipment'] = specialEquipment.find(
                'span', class_='info').text
        else:
            pageData['specialEquipment'] = 'None'
    else:
        pageData['specialEquipment'] = 'None'

    if soup.find('aside', class_='callout callout-bottom callout-bottom-recipe recipe-notes') != None:
        notes = soup.find(
            'aside', class_='callout callout-bottom callout-bottom-recipe recipe-notes')
        pageData['notes'] = notes.find('span', class_='info').text
    else:
        pageData['notes'] = 'None'
    if soup.find('ul', class_='recipe-about') != None:
        recipeAbout = soup.find('ul', class_='recipe-about')
        timeInfo = recipeAbout.find_all('span', class_='info')
        if len(timeInfo) > 0:
            pageData['activeTime'] = timeInfo[len(timeInfo) - 2].text
            pageData['totalTime'] = timeInfo[len(timeInfo) - 1].text
        else:
            pageData['activeTime'] = 'None'
            pageData['totalTime'] = 'None'
    else:
        pageData['totalTime'] = 'None'
        pageData['activeTime'] = 'None'
    directions = soup.find('div', class_='recipe-procedures show-large-images')
    if directions != None:
        directionText = directions.find_all(
            'div', class_='recipe-procedure-text')
        if directionText != None:
            totalDirection = ''
            for i in directionText:
                singleLine = i.text
                totalDirection += singleLine
            pageData['direction'] = totalDirection.replace("\n", "")
        else:
            pageData['direction'] = "No directions found"
    else:
        pageData['direction'] = "No directions found"

    totalIngredients = ''
    ingredients = soup.find('div', class_='recipe-ingredients')
    if ingredients != None:

        for i in ingredients.find_all('li', class_='ingredient'):
            singleLine = i.text
            totalIngredients += singleLine
        pageData['ingredients'] = totalIngredients
    else:
        pageData['ingredients'] = "No ingredients found"
    return pageData


arrayofPageData = []
for i in main_list:
    for j in i:
        url = j
        print(url)
        html_content = requests.get(url).text
        soup = BeautifulSoup(html_content, 'html.parser')
        s = soup.find_all("script", type="application/ld+json")
        js = json.loads(s[len(s) - 1].text)
        recipeUrls = [i["url"] for i in js["itemListElement"]]
        while len(recipeUrls) > 0:
            url = recipeUrls.pop(0)
            arrayofPageData.append(getWebData(url))
print(len(arrayofPageData))
with open('data.json', 'w') as outfile:
    json.dump(arrayofPageData, outfile)
