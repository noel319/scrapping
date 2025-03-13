import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Step 1: Read the uscities.csv file and process the city names
def process_city_names(input_file):
    cities = []
    with open(input_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            city = row['city'].lower().replace(' ', '-')
            cities.append(city)
    return cities

# Step 2: Generate URLs and save them to url.csv
def generate_urls(cities, output_file):
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['city', 'url'])
        for city in cities:
            url = f"https://www.greatschools.org/best-high-schools/{city}/{city}?distance=60&gradeLevels%5B%5D=h&lat=40.6906&locationType=city&lon=-73.9488"
            writer.writerow([city, url])

# Step 3: Scrape the school information using Selenium
def scrape_school_info(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    service = Service(executable_path='/path/to/chromedriver')  # Update with your chromedriver path
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    driver.get(url)
    
    # Wait until the school cards are loaded
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "school-card"))
    )
    schools = []
    school_cards = driver.find_elements(By.CLASS_NAME, "school-card")
    for card in school_cards:
        try:
            name = card.find_element(By.CLASS_NAME, "name").text
            address = card.find_element(By.CLASS_NAME, "address").text
            school_url = "https://www.greatschools.org" + card.find_element(By.CLASS_NAME, "name").get_attribute("href")
            schools.append((name, school_url, address))
        except Exception as e:
            print(f"Error extracting school info: {e}")
    
    driver.quit()
    return schools

# Step 4: Save the extracted data to url.csv
def save_school_info(schools, output_file):
    with open(output_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for school in schools:
            writer.writerow(school)

# Main function
def main():
    input_file = 'uscities.csv'
    output_file = 'url.csv'
    
    # Step 1: Process city names
    cities = process_city_names(input_file)
    
    # Step 2: Generate URLs
    generate_urls(cities, output_file)
    
    # Step 3: Scrape school information
    with open(output_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            city = row['city']
            url = row['url']
            print(f"Scraping data for {city}...")
            schools = scrape_school_info(url)
            
            # Step 4: Save school information
            save_school_info(schools, output_file)
    
    print("Scraping completed and data saved to url.csv")

if __name__ == "__main__":
    main()