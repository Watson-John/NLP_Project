from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
import random
import json

#This function helps crawl the page content#
def scrape_usnews_economy(url="https://www.washingtonpost.com/economy/", 
                           num_pages=1, 
                           headless=True):
    """
    Connect to US News Economy page using Selenium with Edge and extract the raw text.
    
    Parameters:
    url (str): URL to scrape, defaults to US News Economy section
    num_pages (int): Number of pages to scrape
    headless (bool): Whether to run browser in headless mode
    
    Returns:
    list: List of dictionaries containing page_number and raw_text for each page
    """
    results = []
    
    # Set up Edge options
    options = Options()
    if headless:
        options.add_argument("--headless")
    
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-extensions")
    options.add_argument("--inprivate")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188")
    
    try:
        # Initialize the Edge driver
        print("Setting up Microsoft Edge WebDriver...")
        service = Service(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
        
        # Loop through the pages
        for page in range(1, num_pages + 1):
            try:
                # Construct the URL for the current page
                current_url = url if page == 1 else f"{url}?page={page}"
                print(f"Scraping page {page}: {current_url}")
                
                # Navigate to the page
                driver.get(current_url)
                
                # Wait for page to load
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                
                # Scroll down to load any lazy-loaded content
                _scroll_page(driver)
                
                # Get all the text from the page
                page_text = driver.find_element(By.TAG_NAME, "body").text
                
                # Add to results
                results.append({
                    "page_number": page,
                    "url": current_url,
                    "raw_text": page_text
                })
                
                # Wait a random amount of time before moving to the next page
                if page < num_pages:
                    delay = random.uniform(3, 6)
                    print(f"Waiting {delay:.2f} seconds before next page...")
                    time.sleep(delay)
                    
            except Exception as e:
                print(f"Error scraping page {page}: {e}")
                # Continue to the next page
        
        print(f"Successfully scraped {len(results)} pages")
        return results
        
    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
        return results
        
    finally:
        # Make sure to close the browser
        if 'driver' in locals():
            driver.quit()
            print("Browser closed")

#this function help loading all the content#
def _scroll_page(driver):
    """Helper function to scroll the page gradually to load all content"""
    try:
        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        # Define number of steps for a smoother scroll
        num_steps = random.randint(3, 5)
        
        for step in range(num_steps):
            # Calculate scroll position for this step
            target_height = int(last_height * (step + 1) / num_steps)
            
            # Scroll to that position
            driver.execute_script(f"window.scrollTo(0, {target_height});")
            
            # Wait a random amount after each scroll
            time.sleep(random.uniform(0.2, 0.5))
    except:
        pass

#this function help retrieving the necessary contents#
def processing_filtered_items(results):
    filtered_items = []
    for item in results[0]['raw_text'].split('\n')[13:67]:
        if len(item.split(' '))>3:
            filtered_items.append(item)
    return filtered_items
    

#this function will finalize the output to dictionary#
def convert_to_dict_list(input_list):
    """
    Convert a list where odd-indexed items are titles and even-indexed items are contents
    into a list of dictionaries with title-content pairs.
    
    Args:
        input_list: A list where items at odd indices (1, 3, 5...) are titles and 
                   items at even indices (0, 2, 4...) are contents
    
    Returns:
        A list of dictionaries, each with a 'title' and 'content' key
    """
    result = []
    
    # Ensure we have pairs to work with
    if len(input_list) < 2:
        return result
    
    # Process the list in pairs
    for i in range(0, len(input_list), 2):
        # Make sure we don't go out of bounds
        if i+1 < len(input_list):
            title = input_list[i]
            content = input_list[i+1]
            result.append({"title": title, "content": content})
    
    return result


def export_to_json(filtered_items):
	print('------------------------------')
	print('Exporting data to Json')
	print('------------------------------')
	with open('data_wp.json', 'w') as fp:
		json.dump(filtered_items, fp)

if __name__ == "__main__":
    # Get user input
    try:
        num_pages = int(input("How many pages to scrape? (default: 1): ") or "1")
    except ValueError:
        num_pages = 1
    
    headless = input("Run in headless mode ( Open browser ? ) ? [Y/n]: ").lower() != 'n'
    print('------------------------------------')
    print('Starting crawling the economy articles data')
    print('------------------------------------')
    # Scrape the pages
    results = scrape_usnews_economy(num_pages=num_pages, headless=headless)
    print('------------------------------------')
    print('Showing some scraped data')
    print('------------------------------------')
    # Show some results
    if results:
        print(f"\nScraped {len(results)} pages.")
        sample_text = results[0]["raw_text"][:500]
        print(f"\nSample text from first page:\n{sample_text}...\n")
    print('------------------------------------')
    print('Starting processing the scraped data')
    print('------------------------------------')
    filtered_items = processing_filtered_items(results)
    print('------------------------------------')
    print('Finalizing the output')
    print('------------------------------------')
    filtered_items = convert_to_dict_list(filtered_items)
    print(filtered_items)
    print('------------------------------------')
    print('Exporting the output to JSON')
    print('------------------------------------')
    export_to_json(filtered_items)
    print('Task finished')


