# if you want to scrape a website:
# 1. use the API
# 2. HTML web scarapping using some tools like bs4   
# 

# step.1
# pip install requests
# pip install bs4
# pip install html5lib




from typing import TYPE_CHECKING, Type
import requests
from bs4 import BeautifulSoup
url = "http://farmingaws.pythonanywhere.com"

# step1:  get the HTML
r = requests.get(url)
htmlcontent = r.content
#print(htmlcontent)

# step2: parse the html
soup = BeautifulSoup(htmlcontent,'html.parser')
#print(soup.prettify)

# step3. HTML tree traversal
#
# commonly used types of objects:
# print(type(title)) # 1.Tag
# print(type(title.string)) # 2. Navigablestring
# print(Type(soup))  # 3. Beautifulsoup

#  step comments
markup = "<p><!---This is my name and comment --></p>"
soup2 = BeautifulSoup(markup)
print(soup2.p)
print(type(soup2.p.string))
#exit()
title = soup.title

# get all the pargraphs from the HTML

paras = soup.find_all('p')
#print(paras)

# get all the anchor tage from web page
anchors = soup.find_all('a')
#print(anchors)


#  get first element in the HTML page
print(soup.find('p'))

#  get class of any element in the html page
#print(soup.find('p')['class'])

#  find all the element with class lead
print(soup.find_all("p", class_="lead"))


# get the text from the tags/soup
print(soup.find('p').get_text())
print(soup.get_text())

#  get all the anchor tags from the page
anchors = soup.find_all('a')
all_links = set()
for link in anchors:
    if(link.get('href') != '#'):
        linkText = "http://farmingaws.pythonanywhere.com" +link.get('href')
        all_links.add(link)
        print(linkText)


elem = soup.select('.modal-footer')
print(elem)        