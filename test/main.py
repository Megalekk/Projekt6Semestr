from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
#driver.get("http://intranet.unob.cz")
pageurl = ""
driver.get(pageurl)
#assert "Python" in driver.title

source = driver.page_source
print(source)

elem = driver.find_element(By.NAME, "q")
elem.clear()
elem.send_keys("")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
driver.close()
