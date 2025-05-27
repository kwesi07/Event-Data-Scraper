# Event Web Scraper

## Description
A Python-based web scraper that extracts event details (name, date, location) from Meetup’s Hong Kong events page (`https://www.meetup.com/find/?location=hk--Hong+Kong`) and saves them to a structured JSON file (`events.json`). The scraper uses BeautifulSoup for HTML parsing and Selenium to handle JavaScript-rendered content, making it ideal for event discovery applications. This project demonstrates web scraping skills and is hosted on GitHub for portfolio purposes.

## Prerequisites
Before setting up the project, ensure you have the following:
- **Python 3.8 or higher**: Download from [python.org](https://www.python.org/downloads/) if not installed.
- **Google Chrome Browser**: Required for Selenium to render web pages. Download from [google.com/chrome](https://www.google.com/chrome/) if needed.
- **pip**: Python’s package manager (usually included with Python).
- **A text editor**: VS Code, PyCharm, or any editor for modifying code.
- **Internet connection**: To download dependencies and access the Meetup website.

## Setup Instructions
Follow these steps to set up and run the scraper. The process takes approximately 10–15 minutes.

### Step 1: Clone or Create the Project Repository
1. **Create a project folder**:
   ```bash
   mkdir Event-Web-Scraper
   cd Event-Web-Scraper
   ```
2. **Initialize a Git repository** (optional, for GitHub):
   ```bash
   git init
   ```
   If you want to push to GitHub, create a repository on [github.com](https://github.com) and link it:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/Event-Web-Scraper.git
   ```

### Step 2: Install Python Dependencies
1. **Install required libraries**:
   Run the following command to install Selenium and BeautifulSoup:
   ```bash
   pip install selenium beautifulsoup4 lxml
   ```
2. **Verify installation**:
   Check that the libraries are installed:
   ```bash
   pip show selenium beautifulsoup4 lxml
   ```
   You should see version information for each.

### Step 3: Install and Configure ChromeDriver
Selenium requires ChromeDriver to interact with the Chrome browser. Since you couldn’t upload the Chrome app, here’s how to download and set it up:

1. **Check your Chrome version**:
   - Open Google Chrome.
   - Click the three-dot menu (top-right) > **Help** > **About Google Chrome**.
   - Note the version number (e.g., 129.0.6668.70).

2. **Download ChromeDriver**:
   - Visit the ChromeDriver download page: [chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads).
   - Find the ChromeDriver version that matches your Chrome version (e.g., for Chrome 129.x, download ChromeDriver 129.x).
   - Download the appropriate file for your operating system:
     - **Windows**: `chromedriver-win64.zip`
     - **Mac**: `chromedriver-mac-x64.zip` or `chromedriver-mac-arm64.zip` (for Apple Silicon)
     - **Linux**: `chromedriver-linux64.zip`
   - Unzip the downloaded file to get `chromedriver.exe` (Windows) or `chromedriver` (Mac/Linux).

3. **Place ChromeDriver**:
   - **Option 1: Project folder** (recommended for simplicity):
     - Move `chromedriver` to your `Event-Web-Scraper` folder (e.g., `Event-Web-Scraper/chromedriver.exe`).
   - **Option 2: System PATH** (for advanced users):
     - Move `chromedriver` to a directory in your system’s PATH (e.g., `/usr/local/bin` on Mac/Linux or `C:\Windows` on Windows).
     - Verify it’s accessible by running:
       ```bash
       chromedriver --version
       ```
       You should see the ChromeDriver version.

4. **Note for Windows**:
   - If you place ChromeDriver in the project folder, ensure the script references its path (see script modifications below).
   - If you add it to PATH, no script changes are needed.

### Step 4: Add the Scraper Script
1. Create a file named `scrape_meetup.py` in your `Event-Web-Scraper` folder.
2. Copy the following code into `scrape_meetup.py`:

```python
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
options.add_argument('user-agent=M