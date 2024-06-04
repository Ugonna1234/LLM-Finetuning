from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# Readme: This script is used to scrape a particular website and save its content to a txt.

# Input
base_url = "https://www.grubstreet.com/tags/restaurant-review/?start="
start_page = 0
num_pages = 5  # Number of index pages to scrape
wait_time = 50

# Define the target directory for saving files
target_directory = r"C:\Users\ohakimu\OneDrive - Perkins and Will\Desktop\IAAC\Semester 3\Gen AI\LLM\LLM-Finetuning\scrape_data"

# Path to the existing Chrome profile
chrome_profile_path = r"C:\Users\ohakimu\AppData\Local\Google\Chrome\User Data"

# Chrome options to use existing profile
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"user-data-dir={chrome_profile_path}")

# Extract the paragraph elements from the webpage
def get_paragraphs(driver):
    WebDriverWait(driver, wait_time).until(
        EC.presence_of_all_elements_located((By.XPATH, "//*[@class='clay-paragraph' or @class='clay-paragraph_drop-cap']"))
    )
    paragraph_elements = driver.find_elements(By.XPATH, "//*[@class='clay-paragraph' or @class='clay-paragraph_drop-cap']")
    paragraphs = [p.text for p in paragraph_elements]
    return paragraphs

# Extract the title element for each webpage
def get_title(driver):
    WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1")))
    title_element = driver.find_element(By.CSS_SELECTOR, "h1")
    project_name = title_element.text
    filename = f"{project_name}.txt"
    valid_filename = "".join(c for c in filename if c.isalnum() or c in (' ', '_', '-')).rstrip()
    valid_filename = valid_filename.replace(" ", "_")
    filepath = os.path.join(target_directory, valid_filename)
    if os.path.exists(filepath):
        print(f"File already exists: {filepath}. Skipping project.")
        return None
    return filepath

# Clean unwanted text
def clean_paragraphs(paragraphs):
    cleaned_paragraphs = []
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        # Exclude paragraphs with specific tags
        if "<strong>" in paragraph:
            continue
        # Only add paragraphs that are not empty and have 5 or more words
        if paragraph and len(paragraph.split()) >= 5:
            cleaned_paragraphs.append(paragraph)
    return cleaned_paragraphs

# Save the scraped text
def save_text(filepath, paragraphs):
    content = "\n\n".join(paragraphs)
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(content)

# Get article URLs from the index pages
def get_article_urls(driver):
    article_urls = []
    for page_num in range(start_page, start_page + num_pages):
        url = f"{base_url}{page_num * 10}"  # Assuming 10 articles per page
        driver.get(url)
        article_elements = driver.find_elements(By.CLASS_NAME, "article")
        for article in article_elements:
            link_element = article.find_element(By.CSS_SELECTOR, "a.link-text")
            article_url = link_element.get_attribute("href")
            article_urls.append(article_url)
    return article_urls

# Run
driver = webdriver.Chrome(options=chrome_options)
article_urls = get_article_urls(driver)

for url in article_urls:
    driver.get(url)
    try:
        # Get project title and check if we already scraped it
        filepath = get_title(driver)
        if filepath is None:
            continue

        print(f"\nTitle: {os.path.basename(filepath)}")

        # Get text
        paragraphs = get_paragraphs(driver)
        paragraphs = clean_paragraphs(paragraphs)
        print(paragraphs)

        # Export to txt
        save_text(filepath, paragraphs)

    except Exception as e:
        print("Error: ", e)
        continue

# Close the WebDriver
driver.quit()

print("Finished scraping.")
