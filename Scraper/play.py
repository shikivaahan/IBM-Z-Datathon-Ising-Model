from playwright.sync_api import sync_playwright

def get_html(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        # Wait for the page to fully load JavaScript
        page.wait_for_timeout(5000)  # Adjust timeout as necessary
        html = page.content()  # Get the page content
        browser.close()
        return html

# Usage example
url = 'https://www.reddit.com/r/soccer/comments/1g75iu2/erik_ten_hag_we_have_won_trophies_remember_6/'
html = get_html(url)

# Parse the HTML with BeautifulSoup
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Extract comments
comments = soup.find_all('p')
for comment in comments:
    print(comment.get_text())