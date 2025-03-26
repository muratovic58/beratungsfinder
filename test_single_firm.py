from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
from bs4 import BeautifulSoup
import time

def setup_driver():
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

def extract_visible_text(driver, url):
    driver.get(url)
    time.sleep(3)  # Wait for page to load
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Remove script and style elements
    for script in soup(["script", "style", "meta", "link"]):
        script.decompose()
    
    # Get text and split into lines
    lines = soup.get_text(separator='\n').split('\n')
    
    # Clean up the lines
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if line and not line.isspace():  # Keep non-empty lines
            cleaned_lines.append(line)
    
    # Write to file
    with open('firm_text.txt', 'w', encoding='utf-8') as f:
        for line in cleaned_lines:
            f.write(line + '\n')
    
    print("\nExtracted text content:")
    print("-" * 50)
    for line in cleaned_lines:
        print(line)

def main():
    url = "https://www.bdu.de/beraterdatenbank/007456/helbling-business-advisors-gmbh"
    driver = setup_driver()
    
    try:
        extract_visible_text(driver, url)
        print("\nText content has been saved to firm_text.txt")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
