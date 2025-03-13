import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_school_info(url):
    service = Service()
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)    
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
            school_url = card.find_element(By.CLASS_NAME, "name").get_attribute("href")
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
    output_file = 'url.csv'
    for i in range(1,30):
        url = f"https://www.greatschools.org/best-high-schools/new-york/new-york?distance=60&gradeLevels%5B%5D=h&lat=40.6906&locationType=city&lon=-73.9488&page={i}"
        print(f"Scraping data for {url}...")
        schools = scrape_school_info(url)        
        # Step 4: Save school information
        save_school_info(schools, output_file)    
    print("Scraping completed and data saved to url.csv")

if __name__ == "__main__":
    main()