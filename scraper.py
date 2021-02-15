import requests
from bs4 import BeautifulSoup
import json
from glob import glob
from os.path import join
from urllib.parse import urljoin
import os
total_memory = 0

def get_all_cuisne(url):
    global total_memory 
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, 'html.parser')
    #========================================level 1 download======
    try:
        os.makedirs('data/'+ 'level1' +"/")
    except:
        pass
    html_download = soup.prettify()
    filename = "web_1" 
    with open('data/'+ 'level1'+"/" + filename, "w") as f:
                f.write(url)
                f.write("\n")
                print(html_download,file = f)
    f.close()
    memory =  os.stat('data/'+ 'level1'+"/" + filename)
    total_memory += memory.st_size
    #========================================level 1 download======
    save_temp = []
    for item in soup.find_all("ul", class_="c-category-flex__nav-listing"):
        for a in item.find_all('a', {'href': True}):
            save_temp.append(a['href'])
    return(save_temp)


def get_the_link_cuisine(url): # read level 1 get level 2 link
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

def getWebData(url,pagenumber):
    
    # =========================download=============
    global total_memory 
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'html.parser')
    try:
        os.makedirs('data/'+ 'level3' +"/")
    except:
        pass
    html_download = soup.prettify()
    filename = "web_" +  str(pagenumber) 
    with open('data/'+ 'level3'+"/" + filename, "w") as f:
                f.write(url)
                f.write("\n")
                print(html_download,file = f)
    f.close()
    memory =  os.stat('data/'+ 'level3'+"/" + filename)
    total_memory += memory.st_size
    # =========================download=============
    pageData = {}
    # source = requests.get(url).text
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
        liTags = recipeAbout.find_all("li")
        for i in range(len(liTags)):
            if "Active time" in liTags[i].find('span').text:
                time = liTags[i].find("span", class_="info")
                pageData['activeTime'] = time.text
            elif "Total time" in liTags[i].find('span').text:
                time = liTags[i].find("span", class_="info")
                pageData['totalTime'] = time.text
        if "activeTime" not in pageData:
            pageData['activeTime'] = 'None'
        if  "totalTime" not in pageData:
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

# baseurl = "https://www.seriouseats.com/recipes/topics/cuisine/"
# cusineurl = baseurl + "American"
# print(cusineurl)
# print(get_the_link_cuisine(cusineurl))
main_cuisne_menu = 'https://www.seriouseats.com/recipes/topics/cuisine'
cusineurl_list = get_all_cuisne(main_cuisne_menu) # save level 1 html inside, get the link of level2
# print(cusineurl_list)
main_list = []
for cusine_name in cusineurl_list:
    main_list.append(get_the_link_cuisine(cusine_name)) #  all page for each cusine, all level 2 page link
# print(main_list)

arrayofPageData = []
try:
    os.makedirs('data/'+ 'level3' +"/")
except:
    pass
page3 = 1 # for all page in level 3 which the recipe web page
page2 = 0
try:
    os.makedirs('data/'+ 'level2' +"/")
except:
    pass
for i in main_list: # get the all page of cusine
    for j in i: # get the all link in each page. 
        page2 += 1
        url = j
        # print(url)
        #===============================download level 2 web page =========
        html_content = requests.get(url).text
        soup = BeautifulSoup(html_content, 'html.parser')
        html = soup.prettify()
        filename = "web_" + str(page2) # level 2 page which is 'https://www.seriouseats.com/recipes/topics/cuisine/american?page=' content
        try:
            with open('data/'+ 'level2'+"/" + filename, "w") as f:
                f.write(url)
                f.write("\n")
                print(html,file = f)
            f.close()
            memory =  os.stat('data/'+ 'level2'+"/" + filename)
            total_memory += memory.st_size
        except:
            print("error",url)
        #===============================download level 2 web page =========
        s = soup.find_all("script", type="application/ld+json")
        js = json.loads(s[len(s) - 1].text)
        recipeUrls = [i["url"] for i in js["itemListElement"]]
        while len(recipeUrls) > 0:
            url = recipeUrls.pop(0)
            arrayofPageData.append(getWebData(url,page3))
            page3 += 1 
# print(len(arrayofPageData))
print("web crawling reach memory: ", total_memory)
print("web crawling reach page: ", page2 + page3 +1 )
with open('data.json', 'w') as outfile:
    json.dump(arrayofPageData, outfile)
