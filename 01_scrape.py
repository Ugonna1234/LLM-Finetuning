from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os 

# Readme: This script is used to scrape a particular website and save its content to a txt.

# Input
website = "https://www.dezeen.com/2024/04/27/tuckey-design-studio-old-chapel/?li_source=LI&li_medium=rhs_block_1"
wait_time = 50
num_pages = 10

# Define the target directory for saving files
target_directory = r"C:\Users\ohakimu\OneDrive - Perkins and Will\Desktop\IAAC\Semester 3\Gen AI\LLM\LLM-Finetuning\scrape_data"

# Path to the existing Chrome profile
chrome_profile_path = r"C:\Users\ohakimu\AppData\Local\Google\Chrome\User Data"

# Chrome options to use existing profile
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"user-data-dir={chrome_profile_path}")

# Extract the paragraph elements from the webpage
def get_paragraphs(driver):
    WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.ID, "single-content")))
    text_body = driver.find_element(By.ID, "single-content")
    paragraph_elements = text_body.find_elements(By.TAG_NAME, "p")
    paragraphs = [p.text for p in paragraph_elements]
    return paragraphs

# Extract the title element for each webpage
def get_title(driver):
    WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.afd-title-big.afd-title-big--full.afd-title-big--bmargin-big.afd-relativeposition")))
    title_element = driver.find_element(By.CSS_SELECTOR, "h1.afd-title-big.afd-title-big--full.afd-title-big--bmargin-big.afd-relativeposition")
    project_name = title_element.text
    filename = f"{project_name}.txt"
    valid_filename = "".join(c for c in filename if c.isalnum() or c in (' ', '_', '-')).rstrip()
    valid_filename = valid_filename.replace(" ", "_")
    filepath = os.path.join(target_directory, valid_filename)
    if os.path.exists(filepath):
        print(f"File already exists: {filepath}. Skipping project.")
        return None
    return filepath

# Navigate to the next project
def next_project(driver):
    WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.XPATH, '//*[@id="article-nav-next"]')))
    next_button = driver.find_element(By.XPATH, '//*[@id="article-nav-next"]')
    next_url = next_button.get_attribute("href")
    driver.get(next_url)

# Clean unwanted text
def clean_paragraphs(paragraphs):
    cleaned_paragraphs = []
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        # Only add paragraphs that are not empty and have 5 or more words
        if paragraph.startswith("Text description provided by the architects."):
            paragraph = paragraph.replace("Text description provided by the architects.", "").strip()
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

# Run 
driver = webdriver.Chrome(options=chrome_options)
driver.get(website)
i = 0
while i < num_pages:
    try:
        # Get project title and check if we already scraped it
        filepath = get_title(driver)
        if filepath is None:
            next_project(driver)
            continue

        print(f"\nTitle: {os.path.basename(filepath)}")

        # Get text
        paragraphs = get_paragraphs(driver)
        paragraphs = clean_paragraphs(paragraphs)
        print(paragraphs)

        # Export to txt
        save_text(filepath, paragraphs)

        # Move to next project
        next_project(driver)
        i += 1

    except Exception as e:
        print("Error: ", e)
        break

# Close the WebDriver
driver.quit()

print("Finished scraping.")
