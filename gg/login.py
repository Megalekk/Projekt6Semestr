import base64
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def login(driver):
    try:
        f = open("..\login.txt", "r")
        username = f.readline()
        password = f.readline()
        password = base64.b64decode(password.encode('ascii')).decode('ascii')
        f.close()
    except:
        print("File not found.")

    elem = driver.find_element(By.NAME, "Username")
    elem.clear()
    elem.send_keys(username)
    elem = driver.find_element(By.NAME, "Password")
    elem.clear()
    elem.send_keys(password)
    elem.send_keys(Keys.RETURN)