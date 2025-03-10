#Notes

# What is Web Scraping? Video 1
# - the process of automating data collection from a website
#

# requests library

import requests
myPage = requests.get("https://brickset.com/sets/year-2020")

#the requests.get function retreives the website

# Starting to Scrape Video 2

#Process the page

from bs4 import BeautifulSoup
parsed = BeautifulSoup(myPage.text)

#Creates a structure of tags that we can navigate using the
#BeautifulSoup builtin methods

import requests
from bs4 import BeautifulSoup

myPage = requests.get("https://brickset.com/sets/year-2020")
parsed = BeautifulSoup(myPage.text)

#import bs4 import BeautifulSoup

#parsed = BeautifulSoup(myPage.text) organizes the html into "tags"
#html is the structure of the website, css is the styling, js provides interactivity
#json is affectively a dictionary, provides data to a website

## we have a parser that organizes the tags, now we have to look through the parsed data

parsed.title #we can use parsed.title.text to bring back just the stringg of the content, we'll use this a lot

#this brings back the title tag in the url

#we need to dig into the html of the website the structure of the website
#we'll use "inspect" on the website

parsed.find_all('article')

#this will give us a list of all the article tags

articles = parsed.find_all('article')

#this will give all the articles on the page

len(articles)

#let's check to make sure we the right number of tags by using len

import requests
from bs4 import BeautifulSoup

myPage = requests.get("https://brickset.com/sets/year-2020")
parsed = BeautifulSoup(myPage.text)

articles = parsed.find_all('article')

#we've collected all of our search results from the page

#Parsing HTML for data Video 3

#Can we collect the title and prices from the lego webiste?

#let's look for the tag that contains the title using "inspect" on the website

a = articles[0]

#a is our first article tag or lego set

a.h1

#a.h1 = bookshop, let's extract our text from the bookshop legoset

a.h1.text 

#a.h1.text = Bookshop, the title of the legoset

[a.h1.text for a in articles]

#we can now automate finding the title of every legoset on the website
## We've found the list of titles, h1.text provides the title 

#Let's try to find the price in euros of the legoset

a.dd.text

## a.dd.text gives us the number of pieces instead of the price
### we need the relationship between the recommended retail prices and the data
### the dd tag isn't always in the same spot on the list
# how do we find the price?

a.find('dt', text = 'RRP')

## find a dt tag with text rrp (recommended retail price)

a.find('dt', text = 'RRP').find_next_sibling().text

# Parent tags - usually the least indented
## Child tags - indendted under parent tags
## sibling tags - inline with child tags

#this will give us the price in euros and dollars

#let's do some cleaning and find the price in euros

import re

#let's use regex to find euros

re.search(r'\d+[.]d{2}',),a.find('dt', text = 'RRP').find_next_sibling().text

#we know the euro is always two decimal places after prices

#we need to add the euro symbol using unicode characters

import re

re.search(
r'(\d+.\d+)(\u20AC)', # \u20AC is unicode for Euro
a[0].find('dt', text="RRP").find_next_sibling().text,
re.UNICODE).groups()[0]

#Let's try this for all of the lego sets

data = [] # We will store information here
# as a list of lists
for i in a: # a is our list of article tags
row = [] # One row per result
row.append(i.h1.text) # Add the title
try: # Unless there is an error
row.append(
re.search(
r'(\d+.\d+)(\u20AC)',
i.find('dt', text="RRP").find_next_sibling().text,
re.UNICODE).groups()[0]) # Add the price
except: # If there is an error
row.append('') # Leave the entry blank
data.append(row) # Put it into the data set


#Making a Functino for our Scrape Video 4

#let's automate the data collection process

#now we have a function that takes the url, parses it and finds the articles
# 
def collectLegoSets(startURL):
# Retrieve starting URL
myPage = requests.get(startURL)
# Parse the website with Beautiful Soup
parsed = BeautifulSoup(myPage.text)

articles = parsed.find_all('article')

for a in articles:

data = []
    for a in articles:
            row = []
            # the title, let's build one row at a time
            row.append(a.h1.text)
            #we append the title and price to the list

            # the price
            row.append(float(re.search(r'(\d+.\d+)(\u20AC)',i.find('dt', text="RRP").find_next_sibling().text,re.UNICODE).groups()[0])

            #appends the title and price to the row = [] list

            data.append(row) #we'll take this list and append it to our main list


            



# Grab all sets from the page
a = [i for i in parsed.find_all('article')]
# Create and empty data set
newData = []


#Assigntment 007 

# Grab all sets from the page
    a = [i for i in parsed.find_all('article')]

    # Create and empty data set
    newData = []

    # Iterate over all sets on the page
    for i in a:
        row = []
        # Add the set name to the row of data
        row.append(i.h1.text)
        try:
            # Extract price and translate to a floating point number from string, append to row IF PRICE EXISTS
            #changed dt to dd
            row.append(float(re.search(r'(\u20AC)(\d+.\d+)', i.find('dd', text="RRP").find_next_sibling().text, re.UNICODE).groups()[0]))
        except:
            # Missing value for sets with no price, append to row IF NO PRICE EXISTS
            row.append(np.nan)
        
        # Add the row of data to the dataset
        newData.append(row)

    newData = pd.DataFrame(newData, columns = ['Set', 'Price_Euro'])
    
    # Check if there are more results on the "next" page
    try:
        nextPage = parsed.find('li', class_="next").a['href']
    except:
        nextPage = None
    
    # If there is another page of results, grab it and combine
    if nextPage:
        # Tell our program not to load new pages too fast by "sleeping" for two seconds before
        #   going to the next page
        time.sleep(2)
        # Merge current data with next page
        return pd.concat([newData, collectLegoSets(nextPage)], axis=0)
    # Otherwise return the current data
    else:
        return newData

lego2019 = collectLegoSets("https://brickset.com/sets/year-2019")

lego2019['Price_Euro'].mean()











