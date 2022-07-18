import time
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

print('if an error comes up - rerun and it should work')

#globals
USERNAME = input('input your username without the u/ > ')
PASSWORD = input('input your password > ')

#install chrome driver
chromedriver_autoinstaller.install()
driver = webdriver.Chrome()


def redditLogin():
    #open URL
    driver.get('https://old.reddit.com/login')
    driver.set_window_size(1024, 600)
    driver.maximize_window()
    
    #find elements
    userInput = driver.find_element(By.XPATH, '//*[@id="user_login"]')
    passInput = driver.find_element(By.XPATH, '//*[@id="passwd_login"]')
    
    #enter text and submit
    userInput.send_keys(USERNAME)
    passInput.send_keys(PASSWORD, Keys.ENTER)
    
    #wait until login
    waitForLogin = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="header-bottom-right"]/span[1]/a')))
    print('Logged In')

def findComments():
    driver.get('https://old.reddit.com/user/{}/comments/'.format(USERNAME))
    
    wiatForPerma = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "permalink")]')))
    permalinks = driver.find_elements(By.XPATH, '//*[contains(text(), "permalink")]')
    for i in permalinks:
        link = i.get_attribute('href')
        commentId = link[-8] + link[-7] + link[-6] + link[-5] + link[-4] + link[-3] + link[-2]
        
        delete = driver.find_element(By.XPATH, '//*[@id="thing_t1_{}"]/div[2]/ul/li[7]/form/span[1]/a'.format(commentId))
        delete.click()
        
        waitForConfirm = waitForLogin = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="thing_t1_{}"]/div[2]/ul/li[7]/form/span[2]/a[1]'.format(commentId))))
        confirm = driver.find_element(By.XPATH, '//*[@id="thing_t1_{}"]/div[2]/ul/li[7]/form/span[2]/a[1]'.format(commentId))
        confirm.click()
        
        time.sleep(0.2)

redditLogin()
for i in range(100):
    findComments()

driver.close()