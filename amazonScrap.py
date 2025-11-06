from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd


driver = webdriver.Chrome('C:\webDrivers\chromedriver')

df = pd.read_excel('Amazon Scraping.xlsx')

URL = 'https://www.amazon.{c}/dp/{a}'

asin = df['Asin'].tolist()
coun = df['country'].tolist()

#To get URL
def upC(i):
    return URL.format(c=coun[i],a=asin[i])

def getTitle(x:str) -> list:
    url = str(x)
    driver.get(url)
    ptitle = driver.find_elements_by_xpath('//h1[@id="productTitle"]')
    if ptitle == None:
       ptitle = driver.find_elements_by_xpath('//h1[@class="a-size-base a-color-price a-color-price"]')
    title_list = []
    for p in range(len(ptitle)):
        title_list.append(ptitle[p].text)
    if len(title_list) == 0:
        title_list.append('URL not available')
    s = ''
    for i in title_list:
        s = s + i
    return s

def getImage(x:str) -> list:
    url = str(x)
    driver.get(url)
    pimage = driver.find_elements_by_xpath("//img[@id = 'landingImage']")
    if pimage==None:
        pimage = driver.find_elements_by_xpath('//img[@id="imgBlkFront"]')
    image_list = []
    for p in range(len(pimage)):
        image_list.append(pimage[p].get_attribute('src'))
    if len(image_list) == 0:
        image_list.append('URL not available')
    return image_list

def getPrice(x:str) -> list:
    url = str(x)
    driver.get(url)
    pprice = driver.find_elements_by_xpath('//span[@class="a-price aok-align-center reinventPricePriceToPayMargin priceToPay"]')
    price_list = []
    for p in range(len(pprice)):
        price_list.append(pprice[p].text)
    if len(price_list) == 0:
        price_list.append('URL not available')
    s = ''
    for i in price_list:
        s = s + i
    return s

def getDesc(x:str) -> list:
    url = str(x)
    driver.get(url)
    pdesc = driver.find_elements_by_xpath('//span[@class="a-list-item"]')
    desc_list = []
    for p in range(len(pdesc)):
        desc_list.append(pdesc[p].text)
    if len(desc_list) == 0:
        desc_list.append('URL not available')
    s = ''
    for i in desc_list:
        s = s + i
    return s

cURL = [upC(i) for i in range(len(coun))]
df['URL'] = cURL

title_list = [getTitle(i) for i in df['URL']]
df["TITLE"] = title_list
image_list = [getImage(i) for i in df['URL']]
df["IMAGE"] = image_list
price_list = [getPrice(i) for i in df['URL']]
df["PRICE"] = price_list
desc_list = [getDesc(i) for i in df['URL']]
df["DESC"] = desc_list

df= df.drop('country',axis=1)
df= df.drop('Asin',axis=1)
df= df.drop('id',axis=1)

df.to_excel("Output.xlsx")

df.to_json('file.json', orient = 'split', compression = 'infer', index = 'true')
df = pd.read_json('outputFile.json', orient ='split', compression = 'infer')