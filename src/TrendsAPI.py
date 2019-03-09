from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from sty import fg, bg, ef, rs, RgbFg
from bs4 import BeautifulSoup
import sys 
import os
'''
    Trends Browser Terminal Output by Felix Schürmeyer
    V. 1.0  
'''

class TrendsBrowser:
    
    def __init__(self,lang):
        self.chrome_options = Options()  
        self.chrome_options.add_argument("--headless")  
        self.chrome_options.add_argument("--lang={}".format(lang))
        self.driver = webdriver.Chrome(os.getcwd() + '/chromedriver',options=self.chrome_options)

    def startProcess(self,keyword,lang):
        if self.checkValid(keyword,lang):
            return True
        url = "https://trends.google.com/trends/explore?q=" + keyword + self.setGlobal(lang)
        print(fg.red + url + fg.rs)
        driver = self.startingDriver(url)

        if not self.errorOnRequest(driver):
            return True

        self.printing(self.getOptions(driver.page_source))


    def setGlobal(self,lang):
        if lang == 'EN':
            lang = self.setGlobal(input('Invalid Langcode set new:'))

        if lang == 'Global':
            geo = ''
        else:
            geo = "&geo=" + lang.upper()

        return geo

    def printing(self,options):
        
        print('\n \n' + options['Country'] + '\n \n')

        print(bg.blue + '### Topics ###' + bg.rs)
        for i in options["Queries"]:
            print(bg.blue + i + bg.rs)

        print()

        print(bg.green + '### Queries ###' + bg.rs)
        for i in options["Topics"]:
            print(bg.green + i + bg.rs)

        print("\n\n")


    def checkValid(self,k,l):
        if len(k) == 0 or len(l) == 0:
            print('Invalid Input ')
            return True
        else:
            return False

    def errorOnRequest(self,driver):
        if "Error 429" in driver.title:
            print(fg.yellow + 'Waiting...' + fg.rs)
            driver.refresh()
        if "Oops! There was a problem displaying this page." in driver.page_source or "Hoppla! Beim Anzeigen dieser Seite ist ein Fehler aufgetreten." in driver.page_source:
            print(fg(201) + 'Invalid Code' + fg.rs)
            return False
        return True

    def startingDriver(self,url):
        self.driver.get(url)
        return self.driver

    def getOptions(self,source):
        soup = BeautifulSoup(source, 'html.parser')
        queries = []; topics = []
        country = soup.select('#compare-pickers-wrapper div hierarchy-picker:nth-child(1) ng-include div.hierarchy-select.ng-pristine.ng-valid div span:nth-child(1)')[0].text

        for i in soup.select('.widget-template'): 
            if 'Related topics' in str(i) or 'Verwandte Themen' in str(i):
                for x in i.select('span[ng-bind="bidiText"]'):
                        topics.append(x.text)
            if 'Related queries' in str(i) or 'Ähnliche Suchanfragen' in str(i):
                for x in i.select('span[ng-bind="bidiText"]'):
                            queries.append(x.text)

        

        return {"Queries":queries,"Topics":topics,"Country":country}

    def exitout(self,i):
        if i == '#exit':
            sys.exit()


    def close(self):
        self.driver.close()
