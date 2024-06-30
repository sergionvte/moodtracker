# Login test

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
browser = webdriver.Chrome(options=options)

browser.implicitly_wait(5)
browser.get('http://127.0.0.1:5000')
link = browser.find_element(By.CLASS_NAME, 'start-button')
link.click()

user_input = browser.find_element(By.ID, "email")
pass_input = browser.find_element(By.ID, 'password')

user_input.send_keys('sergionvte11@outlook.cm')
pass_input.send_keys('Fenixx110')
pass_input.send_keys(Keys.RETURN)

profile = browser.find_element(
    By.CLASS_NAME,
    "greeting"
)

label = profile.get_attribute("innerHTML")

assert "Sergio" in label

browser.quit()