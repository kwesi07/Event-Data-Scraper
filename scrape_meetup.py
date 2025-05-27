from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import time

# Function to extract event details from a container
def extract_event(container):
    name_tag = container.select_one('h2.text-gray7')
    date_tag = container.select_one('time')
    location_tags = container.select('p.line-clamp-1.md\\:hidden')
    # Filter out <p> tags that contain 'Group name:' (i.e., those with <span class="s1uol3r6">)
    location_text = [p.get_text(strip=True) for p in location_tags if not p.select('span.s1uol3r6')]
    location = location_text[-1] if location_text else 'Online'
    return {
        'name': name_tag.get_text(strip=True) if name_tag else '',
        'date': date_tag.get_text(strip=True) if date_tag else '',
        'location': location
    }

# Set up Chrome options for headless browsing
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124 Safari/537.36')

# Initialize the webdriver (ensure ChromeDriver is in PATH or specify executable_path)
# If ChromeDriver is not in PATH, uncomment and adjust the next line
# driver = webdriver.Chrome(executable_path='/path/to/chromedriver', options=options)
driver = webdriver.Chrome(options=options)

try:
    # Navigate to the URL and wait for the page to load
    url = 'https://www.meetup.com/find/?location=hk--Hong+Kong'
    driver.get(url)
    time.sleep(10)  # Adjust wait time if needed

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'lxml')

    # Find all event containers
    event_containers = soup.select('div[data-event-id]')
    if not event_containers:
        print("No event containers found. The page might not have loaded properly.")
    else:
        # Extract events, only including those with a name
        events = [extract_event(container) for container in event_containers if extract_event(container)['name']]
        print(f"Scraped {len(events)} events.")
        if events:
            print("First event:", events[0])

        # Prepare data with timestamp
        scraped_at = "05:09 PM HKT on Tuesday, May 27, 2025"  # Based on current context
        data = {'scraped_at': scraped_at, 'events': events}

        # Write to JSON file
        with open('events.json', 'w') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

finally:
    # Ensure the browser is closed
    driver.quit()