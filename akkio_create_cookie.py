from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import time

# Path to ChromeDriver and where you want the new persistent profile
chromedriver_path = r"chrome_driver\chromedriver.exe"
custom_profile_path = r"C:\SeleniumProfiles\Akkio"  # Make sure this folder exists or will be created

# Create folder if it doesn't exist
os.makedirs(custom_profile_path, exist_ok=True)

# Set up Chrome options
options = Options()
options.add_argument(f"--user-data-dir={custom_profile_path}")
options.add_argument("--no-first-run")
options.add_argument("--no-default-browser-check")
options.add_argument("--disable-extensions")
options.add_experimental_option("detach", True)  # Keep browser open after script ends

# Set up Chrome driver service
service = Service(executable_path=chromedriver_path)

# Launch browser
print("🚀 Launching Chrome with persistent Selenium profile...")
driver = webdriver.Chrome(service=service, options=options)

# Go to Akkio
print("🌐 Navigating to https://app.akkio.com/")
driver.get("https://app.akkio.com/")

print("✅ Please log in manually if not already.")
print("📌 Your session will be saved in:")
print(f"   {custom_profile_path}")
