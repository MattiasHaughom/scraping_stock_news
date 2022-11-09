#%% Imports
import numpy as np
import pandas as pd
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import itertools
import datetime as datetime
from nltk.tokenize import treebank


directory = r"input_folder"
os.chdir(directory)
industry = pd.read_excel('OBStickers.xlsx')
allTickers = pd.read_excel('all_tickers.xlsx')
dct = pd.read_excel('norskDict.xlsx')
pos_list=list(dct['positiv'])
neg_list=list(dct['negativ'][:52])
tokenizer = treebank.TreebankWordTokenizer()

def sentiment(sent):
    senti = 0
    words = [word.lower() for word in tokenizer.tokenize(sent)]
    for word in words:
        if word in pos_list:
            senti += 1
        elif word in neg_list:
            senti -= 1
    return senti



#%% Norwegian stock news scraping

now = datetime.datetime.now()
today8am = now.replace(hour=8, minute=0, second=0, microsecond=0)
today12am = now.replace(hour=12, minute=0, second=0, microsecond=0)
today16am = now.replace(hour=16, minute=0, second=0, microsecond=0)


if now < today8am:
    nReadmores =10
elif np.logical_and(now> today8am,now<today12am):
    nReadmores =20
elif now > today12am:
    nReadmores =25
elif now > today16am:
    nReadmores =35


url = 'https://investor.dn.no/#!/Oversikt'

driver = webdriver.Chrome(r'input_cromedriver_folder')

driver.get(url)
#driver.minimize_window()
button = WebDriverWait(driver, 25).until(
    EC.element_to_be_clickable((By.LINK_TEXT,'Vis flere nyheter')))

driver.execute_script('arguments[0].click()', button)

sleep(5)

button = WebDriverWait(driver, 25).until(
    EC.element_to_be_clickable((By.LINK_TEXT,'Vis mer')))

driver.execute_script('arguments[0].click()', button)

sleep(5)

readMore =  driver.find_elements(By.CLASS_NAME,'inv-overview-readmore')

for number,element in enumerate(readMore[:nReadmores]):
    driver.execute_script('arguments[0].click()', element)
    sleep(1)

sleep(5)
articles = driver.find_elements(By.XPATH,'//*[@id="dndirekte-master-container"]/section/div')

dataFrames = []
aksjeInf = []
for post in articles:
    tekst = post.text
    tmp = list(itertools.chain.from_iterable(list(map(lambda x: x.split(';'),tekst.split("\n")))))
    postSentiment = 0
    if np.logical_and(len(tmp[0]) == 8,len([str(j) for j in allTickers['aksje'] if j in tekst])> 0):
        postSentiment += sentiment(tekst)
        aksjeInf = [str(j) for j in allTickers['aksje'] if j in tekst]
        d = {'aksje':aksjeInf, 'sentiment': postSentiment}
        df = pd.DataFrame([d])
        dataFrames.append(df)
newsSentiment = pd.concat(dataFrames)

driver.quit()

