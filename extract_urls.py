from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd

# Instantiate the WebDriver
driver = webdriver.Chrome()
driver.get('https://www.goodschoolsguide.co.uk/school-search/')

# Accept cookies
driver.execute_script("window.scrollBy(0, 500);")
time.sleep(2)
button = driver.find_element("xpath", '//button[@type="button" and contains(@class, "btn-primary") and contains(@class, "btn-sm") and contains(@class, "acceptcookies")]')
button.click()

# Set age 11 to 18 (the numbers seem to be offset by -3)
driver.execute_script('document.getElementById("child_age_slider").setAttribute("data-from", "8");')
driver.execute_script('document.getElementById("child_age_slider").setAttribute("data-to", "15");')

# Set mixed and girls
checkbox = driver.find_element("xpath", '//input[@type="checkbox" and @name="sixth_form_gender[]" and @value="M"]')
if not checkbox.is_selected():
    checkbox.click()
checkbox = driver.find_element("xpath", '//input[@type="checkbox" and @name="sixth_form_gender[]" and @value="G"]')
if not checkbox.is_selected():
    checkbox.click()

# Open advanced search
link = driver.find_element("xpath", '//a[@href="#collapseThreeAdvanced"]')
link.click()

# Open SEN
#time.sleep(4)
wait = WebDriverWait(driver, 10)
link = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="#collapse_sen"]')))
link.click()
time.sleep(2)

# Attention Deficit Hyperactivity Disorders
checkbox = driver.find_element("xpath", '//input[@type="checkbox" and @name="sen_condition[]" and @value="3"]')
if not checkbox.is_selected():
    checkbox.click()
#time.sleep(2)
# CReSTeD registered for Dyslexia
checkbox = driver.find_element("xpath", '//input[@type="checkbox" and @name="sen_condition[]" and @value="17"]')
if not checkbox.is_selected():
    checkbox.click()
#time.sleep(2)
# Dyscalculia
checkbox = driver.find_element("xpath", '//input[@type="checkbox" and @name="sen_condition[]" and @value="5"]')
if not checkbox.is_selected():
    checkbox.click()
#time.sleep(2)
# Dysgraphia
checkbox = driver.find_element("xpath", '//input[@type="checkbox" and @name="sen_condition[]" and @value="6"]')
if not checkbox.is_selected():
    checkbox.click()
#time.sleep(2)
# Dyslexia
checkbox = driver.find_element("xpath", '//input[@type="checkbox" and @name="sen_condition[]" and @value="7"]')
if not checkbox.is_selected():
    checkbox.click()
#time.sleep(2)
# Dyspraxia
checkbox = driver.find_element("xpath", '//input[@type="checkbox" and @name="sen_condition[]" and @value="8"]')
if not checkbox.is_selected():
    checkbox.click()
#time.sleep(2)
# SpLD - Specific Learning Difficulty
checkbox = driver.find_element("xpath", '//input[@type="checkbox" and @name="sen_condition[]" and @value="27"]')
if not checkbox.is_selected():
    checkbox.click()
#time.sleep(2)

# Click Search
button = driver.find_element("xpath", '//button[@type="submit" and contains(@class, "btn-default") and contains(@class, "btn-lg") and contains(@class, "btn-block")]')
button.click()

# Get the links for each school on each page
link_texts = []
current_url = driver.current_url
while True:
    try:
        links = driver.find_elements("xpath", '//div[@id="list"]//a[contains(@class, "link-primary")]')
        link_texts.extend([link.get_attribute('href') for link in links])
        link = driver.find_element("xpath", '//ul[contains(@class, "pagination")]//li[last()]//a')
        link.click()
        time.sleep(2)
        new_url = driver.current_url
        if new_url == current_url:
            break  # exit the loop if the URL hasn't changed
        
        
        current_url = new_url
    except NoSuchElementException:
        break  # exit the loop if the link is not found


print(link_texts)

df = pd.DataFrame(link_texts, columns=['URL'])
df.to_excel('school_urls.xlsx', header=False, index=False)

driver.quit()