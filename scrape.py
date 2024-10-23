### Contains a function that takes a websites URL and returns
###all of the content from that website

import selenium.webdriver as webdriver
# Selenium allows the user to control their web browser
# Such as interacting with widgets, clicking buttons etc.
from selenium.webdriver.chrome.service import Service 
from bs4 import BeautifulSoup
import time

#This function will allow to user to grab open-sourced content from a site
def scrape_website(website):
    print("Launching chrome browser")

    chrome_driver_path = "./chromedriver.exe"
    #Options are included so the user can specify how the driver should work
    options = webdriver.ChromeOptions()
    #Set Up the driver
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    try:
        #The web driver is being used to go to the website and grab content
        driver.get(website)
        print("page loaded!")
        # Grabbing the page source
        html = driver.page_source
        time.sleep(10)

        return html
    finally:
        driver.quit()
    
def extract_bodyContent(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_bodyContent(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()
    
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
        )

    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
        ]
