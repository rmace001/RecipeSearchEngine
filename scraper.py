import requests
from bs4 import BeautifulSoup
import json
from pandas import DataFrame as df

# extract desired info from a recipe url
def getWebData(url):
    pageData = {}
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    pageData['recipeLink'] = url
    pageData['recipeTitle'] = soup.find('h1', class_='title recipe-title c-post__h1').text
    if soup.find('aside', class_='callout callout-bottom callout-bottom-recipe recipe-equipment') != None:
        specialEquipment = soup.find('aside', class_='callout callout-bottom callout-bottom-recipe recipe-equipment')
        if specialEquipment.find('span', class_='info') != None:
            pageData['specialEquipment'] = specialEquipment.find('span', class_='info').text
    else:
        pageData['specialEquipment'] = 'None'
    
    if soup.find('aside', class_='callout callout-bottom callout-bottom-recipe recipe-notes') != None:
        notes = soup.find('aside', class_='callout callout-bottom callout-bottom-recipe recipe-notes')
        pageData['notes'] = notes.find('span', class_='info').text
    else:
        pageData['notes'] = 'None'
    if soup.find('ul', class_='recipe-about') != None:
        recipeAbout = soup.find('ul', class_='recipe-about')
        timeInfo = recipeAbout.find_all('span', class_='info')
        pageData['totalTime'] = timeInfo[1].text
        pageData['activeTime'] = timeInfo[2].text
    else:
        pageData['totalTime'] = 'None'
        pageData['activeTime'] = 'None'
    directions = soup.find('div', class_='recipe-procedures show-large-images')
    directionText = directions.find_all('div', class_='recipe-procedure-text')

    totalDirection = ''
    for i in directionText:
        singleLine = i.text
        totalDirection += singleLine
    pageData['direction'] = totalDirection.replace("\n", "")

    totalIngredients = ''
    ingredients = soup.find('div', class_='recipe-ingredients')
    for i in ingredients.find_all('li', class_='ingredient'):
        singleLine = i.text
        totalIngredients += singleLine
    pageData['ingredients'] = totalIngredients
    return pageData
# extract all recipe urls from a single cuisine url
url = "https://www.seriouseats.com/recipes/topics/cuisine/american"
html_content = requests.get(url).text
soup = BeautifulSoup(html_content, 'html.parser')
s = soup.find_all("script",type="application/ld+json")
js = json.loads(s[len(s) - 1].text)
recipeUrls = [i["url"] for i in js["itemListElement"]]


arrayofPageData = []
while len(recipeUrls) > 0:
    url = recipeUrls.pop(0)
    arrayofPageData.append(getWebData(url))
        

        
with open('data.json', 'w') as outfile:
    json.dump(arrayofPageData, outfile)



