import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to scrape school details
def scrape_school_details(url):
    service = Service()
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)   
    driver.get(url)
    # Wait for the contact details section to be present
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "contact"))
        )
    except:
        print(f"Timeout waiting for contact section on {url}")
        return None

    try:
        # Extract school address
        address_elements = driver.find_elements(By.CSS_SELECTOR, ".contact > .contact-row:first-of-type span")
        address = " ".join([el.text for el in address_elements]) if address_elements else "N/A"
        print(f"address-{address}")
        # Extract school leader
        leader_element = driver.find_element(By.CLASS_NAME, "school-leader")
        school_leader = leader_element.text if leader_element else "N/A"
        print(school_leader)
        # Extract phone number
        elements = driver.find_elements(By.CSS_SELECTOR, ".contact .contact-details .contact-row a")
        for element in elements:
            if element.text == "School leader email":
                email = element.get_attribute("href")
            elif element.text == "Website":
                website_url= element.get_attribute("href")
            elif element.text != "Facebook page":
                phone = element.text
        driver.quit()
        return [url, address, school_leader, phone, email, website_url]

    except Exception as e:
        print(f"Error extracting data from {url}: {e}")
        driver.quit()
        return None
    
# Function to read URLs from url.csv
def read_urls_from_csv(input_file):
    urls = []   
    with open(input_file, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            if row:  # Ensure row is not empty
                urls.append(row[1])                 
    return urls

# Function to save extracted school information to url.csv

def save_school_info(output_file, school_data):
    with open(output_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for school in school_data:
            writer.writerow(school)


# Main function
def main():
    input_file = "url.csv"
    output_file = "schools.csv"    
    # Read URLs from file
    urls = read_urls_from_csv(input_file)       
    for url in urls:
        print(f"Scraping {url}...")
        details = scrape_school_details(url)
        print(f"Details-{details}")
        if details:
            save_school_info(output_file, details)
    
    # Save extracted data back to CSV
      
    
    print("Scraping completed. Data saved to url.csv")

if __name__ == "__main__":
    main()
