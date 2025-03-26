from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
from bs4 import BeautifulSoup
import time
import os
import json

class FirmScraper:
    def __init__(self):
        self.base_url = "https://www.bdu.de/beraterdatenbank/"
        self.output_dir = "scraped_firms"
        self.progress_file = "scraping_progress.json"
        
        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        # Initialize progress
        self.progress = {
            'last_id': -1,
            'found_firms': [],
            'checked_ids': set()  # Using a set for faster lookups
        }
        
        # Load existing progress if available
        if os.path.exists(self.progress_file):
            with open(self.progress_file, 'r') as f:
                saved_progress = json.load(f)
                self.progress['last_id'] = saved_progress.get('last_id', -1)
                self.progress['found_firms'] = saved_progress.get('found_firms', [])
                self.progress['checked_ids'] = set(saved_progress.get('checked_ids', []))
    
    def save_progress(self):
        """Save progress to file"""
        save_data = {
            'last_id': self.progress['last_id'],
            'found_firms': self.progress['found_firms'],
            'checked_ids': list(self.progress['checked_ids'])
        }
        with open(self.progress_file, 'w') as f:
            json.dump(save_data, f)
    
    def setup_driver(self):
        """Setup Chrome driver with stealth settings"""
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
        
        stealth(driver,
            languages=["de-DE", "de"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )
        
        return driver
    
    def format_id(self, num):
        """Format number as 6-digit string with leading zeros"""
        return f"{num:06d}"
    
    def extract_firm_content(self, driver, url):
        """Extract all visible text content from the page"""
        try:
            print(f"\nChecking URL: {url}")
            driver.get(url)
            time.sleep(2)  # Short wait for page load
            
            # Check if page exists by looking for error messages
            if "Seite nicht gefunden" in driver.page_source:
                print("Page not found")
                return None
                
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "meta", "link"]):
                script.decompose()
            
            # Get text and split into lines
            lines = soup.get_text(separator='\n').split('\n')
            
            # Clean up the lines
            cleaned_lines = [line.strip() for line in lines if line.strip()]
            
            # Check if this is a valid firm entry
            if len(cleaned_lines) > 63:
                print("Valid firm entry found!")
                return '\n'.join(cleaned_lines)
            else:
                print(f"Found exactly {len(cleaned_lines)} lines - empty entry")
                return None
                
        except Exception as e:
            print(f"Error extracting content from {url}: {str(e)}")
            return None
    
    def scrape_firms(self, start_id=None, end_id=999999, batch_size=100):
        """Scrape firms within the specified ID range"""
        driver = self.setup_driver()
        
        try:
            current_id = start_id if start_id is not None else self.progress['last_id'] + 1
            
            while current_id <= end_id:
                batch_start_time = time.time()
                
                print(f"\nProcessing batch starting at ID: {self.format_id(current_id)}")
                
                try:
                    for num in range(current_id, min(current_id + batch_size, end_id + 1)):
                        firm_id = self.format_id(num)
                        
                        # Skip if already processed
                        if firm_id in self.progress['checked_ids']:
                            continue
                        
                        url = f"{self.base_url}{firm_id}/"
                        content = self.extract_firm_content(driver, url)
                        
                        if content:
                            # Save the content to a file
                            filename = os.path.join(self.output_dir, f"firm_{firm_id}.txt")
                            with open(filename, 'w', encoding='utf-8') as f:
                                f.write(content)
                            
                            self.progress['found_firms'].append(firm_id)
                            print(f"Found firm: {firm_id}")
                        
                        self.progress['checked_ids'].add(firm_id)
                        self.progress['last_id'] = num
                        
                        # Random delay between requests
                        time.sleep(1)  # 1 second delay
                
                except ValueError as e:
                    print(f"Error during batch processing: {str(e)}")
                    break
                
                # Save progress after each batch
                self.save_progress()
                
                batch_time = time.time() - batch_start_time
                firms_found = len([id for id in self.progress['found_firms'] 
                                 if int(id) >= current_id and int(id) < current_id + batch_size])
                print(f"Batch completed in {batch_time:.2f} seconds")
                print(f"Firms found in this batch: {firms_found}")
                print(f"Total firms found so far: {len(self.progress['found_firms'])}")
                
                current_id += batch_size
                
        except KeyboardInterrupt:
            print("\nScraping interrupted by user")
        except Exception as e:
            print(f"Error during scraping: {str(e)}")
        finally:
            driver.quit()
            self.save_progress()
            print("\nScraping session completed")
            print(f"Total firms found: {len(self.progress['found_firms'])}")

def main():
    scraper = FirmScraper()
    
    # Start at ID 002200
    start_id = int("000000")  # Stores as 2200 but maintains correct format when printing
    num_urls = 1000
    end_id = start_id + num_urls - 1
    batch_size = 20
    
    print("\nStarting test run with the following parameters:")
    print(f"Start ID: {start_id:06d}")  # Ensures 002200 is displayed correctly
    print(f"End ID: {end_id:06d}")
    print(f"Number of URLs to check: {num_urls}")
    print(f"Batch size: {batch_size}")
    print("\nPress Ctrl+C to stop the scraping at any time.\n")
    
    scraper.scrape_firms(start_id=start_id, end_id=end_id, batch_size=batch_size)

if __name__ == "__main__":
    main()
