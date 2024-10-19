from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

# Set up Selenium WebDriver (Chrome in this case)
service = Service('/path/to/chromedriver')  # Update with your actual ChromeDriver path
driver = webdriver.Chrome(service=service)

# Open the Reddit post page (or any dynamic page)
url = 'https://www.reddit.com/r/Python/comments/some_post_id'
driver.get(url)

# Wait for the page to load fully (you can tweak this time)
time.sleep(5)

# Optional: Scroll to load more comments (infinite scrolling pages)
# Scroll a few times if necessary
for i in range(3):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

# Get the page source after JavaScript content is loaded
html = driver.page_source

# Parse the page with BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Extract the Reddit comments (you might need to adjust the selectors)
comments = soup.find_all('div', {'data-testid': 'comment'})

# Print or process the comments
for comment in comments:
    print(comment.get_text())

# Close the Selenium driver
driver.quit()
