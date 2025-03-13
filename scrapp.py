import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv

# Step 1: Process city names in chunks
def process_city_names_in_chunks(input_file, chunk_size=1000):
    cities = []
    for chunk in pd.read_csv(input_file, chunksize=chunk_size):
        for city in chunk['city']:
            processed_city = city.lower().replace(' ', '-')
            cities.append(processed_city)
    return cities

# Step 2: Generate URLs
def generate_urls(cities):
    base_url = "https://www.greatschools.org/best-high-schools/{city}/{city}?distance=60&gradeLevels%5B%5D=h&lat=40.6906&locationType=city&lon=-73.9488"
    urls = []
    for city in cities:
        url = base_url.format(city=city)
        urls.append((city, url))
    return urls

# Step 3: Scrape the URLs
def scrape_school_info(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        soup = BeautifulSoup(response.content, 'html.parser')
        
        schools = []
        for school_card in soup.find_all('li', class_='school-card'):
            header = school_card.find('div', class_='header')
            address = school_card.find('div', class_='address')
            
            if header and address:
                school_name = header.find('a', class_='name').text.strip()
                school_url = "https://www.greatschools.org" + header.find('a', class_='name')['href']
                school_address = address.text.strip()
                
                schools.append({
                    'name': school_name,
                    'url': school_url,
                    'address': school_address
                })
        
        return schools
    except requests.RequestException as e:
        print(f"Error scraping {url}: {e}")
        return []

# Step 4: Save the results to url.csv
def save_to_csv(data, output_file):
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['name', 'url', 'address'])
        writer.writeheader()
        for row in data:
            writer.writerow(row)

# Main function to execute the task
def main():
    input_file = 'uscities.csv'
    output_file = 'url.csv'
    chunk_size = 1000  # Number of rows to process at a time
    
    # Step 1: Process city names in chunks
    print("Processing city names...")
    cities = process_city_names_in_chunks(input_file, chunk_size)
    
    # Step 2: Generate URLs
    print("Generating URLs...")
    urls = generate_urls(cities)
    
    # Step 3: Scrape school info
    all_schools = []
    for city, url in urls:
        print(f"Scraping {city}...")
        schools = scrape_school_info(url)
        all_schools.extend(schools)
    
    # Step 4: Save to CSV
    print("Saving data to CSV...")
    save_to_csv(all_schools, output_file)
    print(f"Data saved to {output_file}")

if __name__ == "__main__":
    main()