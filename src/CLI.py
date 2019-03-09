from TrendsAPI import TrendsBrowser
from justforfun import fun
import sys

# init the Browser Driver

fun()

print("\n \n Set Browser Language for Request \n \n")


while True: 
    language = input('Press (1) for DE or (2) for EN : ')
    if language == '1':
        language = 'de'
        break
    elif language == '2':
        language = 'en'
        break
    else: 
        print('Invalid')
    
    if language == '#exit':
        sys.exit()


print("Language is set to " + language + "\n\n")

Browser = TrendsBrowser(language)

while True:
    try:
        keyword = input('Keyword:')
        Browser.exitout(keyword)

        lang = input('Langcode:')
        Browser.exitout(lang)

        Browser.startProcess(keyword,lang)
    except:
        print('### Shutdown Service ### Please Restart ###')
        break

Browser.close()
