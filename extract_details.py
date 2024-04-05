import time
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def extract_element_text(driver, css_selector=None, xpath=None):
    try:
        if css_selector:
            elements = driver.find_elements(By.CSS_SELECTOR, css_selector)
        elif xpath:
            elements = driver.find_elements(By.XPATH, xpath)
        if len(elements) > 1:
            return [element.text for element in elements]
        else:
            return elements[0].text if elements else ''
    except NoSuchElementException:
        return ''

# Instantiate the WebDriver
driver = webdriver.Chrome()  # replace with the WebDriver for your preferred browser
driver.get('https://www.goodschoolsguide.co.uk/school-search/')

# Accept cookies
driver.execute_script("window.scrollBy(0, 500);")
time.sleep(2)
button = driver.find_element("xpath", '//button[@type="button" and contains(@class, "btn-primary") and contains(@class, "btn-sm") and contains(@class, "acceptcookies")]')
button.click()

# Read the Excel file
df = pd.read_excel('school_urls.xlsx')

# Get the first column
urls = df.iloc[:, 0].tolist()

# Initialize an empty list to store the new rows
new_rows = []

# Assume total_urls is the total number of URLs you are going to loop over
total_urls = len(urls)

# Visit each URL
for i, url in enumerate(urls, start=1):
    driver.get(url)
    time.sleep(2)  # Wait for the page to load
    # Extract the School Name
    name = extract_element_text(driver, css_selector="h1").replace('\n', ' ')

    # Extract the address
    address_parts = extract_element_text(driver, css_selector="span[itemprop='address'] span")
    address = ', '.join(address_parts)
    address = address.replace('\n', ' ').replace('\t', ' ')

    # Extract the number of pupils
    pupils_text = extract_element_text(driver, xpath="//li[strong='Pupils:']")
    pupils = pupils_text.split(':')[1].strip().replace(',','').replace(';','').split(' ',1)[0] if pupils_text else ''

    # Extract the fees
    fees_text = extract_element_text(driver, xpath="//li[strong='Fees:']")
    fees = fees_text.split(':')[1].strip().replace('£', '').replace(',', '').split(' ')[0] if fees_text else ''

    # Extract the type of school
    type_text = extract_element_text(driver, xpath="//li[strong='Boarding:']")
    school_type = type_text.split(':')[1].strip() if type_text else ''

    # Extract the religion
    religion_text = extract_element_text(driver, xpath="//li[strong='Religion:']")
    religion = religion_text.split(':')[1].strip() if religion_text else ''
    
    # Append the details to the list as a dictionary
    new_rows.append({'Name': name, 'Address': address, 'Number Pupils': pupils, 'Fees': fees, 'Boarding': school_type, 'Religion': religion, 'URL': url})

    # Print the row with its number out of the total number of loops
    print(f'Row {i} of {total_urls}:', new_rows[-1])

# Prepare an empty DataFrame with Headings
data = pd.DataFrame(columns=['Name', 'Address', 'Number Pupils', 'Fees', 'Boarding', 'Religion', 'URL'])  # replace with your headers

# Convert the list of new rows to a DataFrame
new_data = pd.DataFrame(new_rows)

# Concatenate the new data to the original DataFrame
data = pd.concat([data, new_data], ignore_index=True)

# Write the DataFrame to an Excel file
data.to_excel('schools.xlsx', index=False)

driver.quit()