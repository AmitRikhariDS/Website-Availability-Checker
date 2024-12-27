'''
-Scrape Price, Link and address of the properties from one of the website:
-Clean the data
-Fill the entry one by by using selenium in google form
- Link Google form to spredsheet manually.
-End result:
Data in the Excel format


'''

from urllib.response import addbase
import time
from bs4 import BeautifulSoup
import requests
from cffi.cffi_opcode import CLASS_NAME
from selenium.webdriver.common.devtools.v85.target import detach_from_target
from setuptools.command.build_ext import link_shared_object
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

FORM_URL=input("Enter your Google form URl")
WEBSITE_URL=input("Enter the webpage URl which you want to scrape")

res=requests.get(WEBSITE_URL)
soup= BeautifulSoup(res.text,'html.parser')
prices=soup.find(name='span',)
print(prices)
address=[]
for i  in soup.select('.StyledPropertyCardDataArea-anchor[href]'):
    address.append((i.getText()).split('\n')[2].replace(" ",""))

links=[]
for i in soup.select('.StyledPropertyCardDataArea-anchor[href]'):
    links.append(i.get('href'))
prices=[]
for i in soup.select('.PropertyCardWrapper__StyledPriceLine'):
    prices.append((i.getText().split('+')[0].split('/')[0]))

chrome_options= webdriver.ChromeOptions()
chrome_options.add_experimental_option(name='detach',value=True)

driver=webdriver.Chrome(chrome_options)
# option1=driver.find_element(By.CLASS_NAME,value='whsOnd.zHQkBf')
# option2=driver.find_element(By.CLASS_NAME,value='aCsJod.oJeWuf')
# option3=driver.find_element(By.CLASS_NAME,value='ndJi5d.snByac')
# submit= driver.find_element(By.CLASS_NAME,value='NPEfkd.RveJvd.snByac')

for i in range(len(address)):
    driver.get(FORM_URL)
    option1=driver.find_element(By.XPATH,value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    option1.send_keys(address[i])
    time.sleep(3)
    option2=driver.find_element(By.XPATH,value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    option2.send_keys(prices[i])

    time.sleep(3)
    option3=driver.find_element(By.XPATH,value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    option3.send_keys(links[i])

    time.sleep(1)
    submit= driver.find_element(By.XPATH,value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
    submit.send_keys(Keys.ENTER)

time.sleep(5)
