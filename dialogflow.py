from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException,ElementNotVisibleException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chrome_driver = "chromedriver.exe"
driver = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)
print(driver.title)

url_dialogflow = "https://console.dialogflow.com/api-client/"
timeout = 5

saisies = ["bonjour","Lundi","14h","Monsieur"]
limite = 0

def goToDialogflow():
    driver.get(url_dialogflow)

def sendText(txt):
    try:
        element_present = EC.presence_of_element_located((By.ID, 'test-client-query-input'))
        WebDriverWait(driver, timeout).until(element_present)
        
        champ_texte = driver.find_element_by_id("test-client-query-input")
        champ_texte.send_keys(txt, Keys.RETURN)
    except TimeoutException:
        print("Timed out waiting for page to load")
        
def getUserSays():
    says = ""
    try:
        xpath_user_says = '//*[@id="test-console"]/div[2]/div[4]/div[2]/div[2]/span'
        element_present = EC.presence_of_element_located((By.XPATH, xpath_user_says))
        WebDriverWait(driver, timeout).until(element_present)
        
        says = driver.find_element_by_xpath(xpath_user_says)
        if says != None:
            says = says.text
    except TimeoutException:
        print("Timed out waiting for page to load")
    finally:
        #print("Saying : "+says)
        return says

def speakForMe():
    cpt = 1
    for s in saisies:
        if (limite < 1 or cpt <= limite):
            #print("To say : "+s)
            sendText(s)
            says = getUserSays()
            while (says != s):
                time.sleep(1)
                says = getUserSays()
        cpt += 1

def resetContext():
    try:
        element_present = EC.presence_of_element_located((By.ID, 'test-client-query-input'))
        WebDriverWait(driver, timeout).until(element_present)
        
        btn_reset_ctx = driver.find_element_by_id("reset-contexts")
        if (btn_reset_ctx != None):
            btn_reset_ctx.click()
    except TimeoutException:
        print("Timed out waiting for page to load")
    except ElementNotVisibleException:
        print("Reset button is hidden")

resetContext()
speakForMe()