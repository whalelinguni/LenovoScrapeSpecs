# working. warrnaty html save is trash. screen shot function is also trash.
# python script.py <serial> [--mobile option] [--headless option] --wait <Num Seconds>

import sys
import time
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


clear_screen()

# Check if the serial number is provided as a command-line argument
if len(sys.argv) < 2:
    print(
        "Usage: python script_name.py <serial_number> [--headless] [--mobile] [--wait <seconds>]"
    )
    sys.exit(1)

# Extract serial number from command-line arguments
serial_number = sys.argv[1]

# Check if headless mode is enabled from command-line argument
headless = "--headless" in sys.argv
print("Headless mode:", headless)

# Check if mobile mode is enabled from command-line argument
mobile = "--mobile" in sys.argv
print("Mobile mode:", mobile)


# Extract wait time from command-line arguments
wait_time = 5  # Default wait time in seconds
if "--wait" in sys.argv:
    try:
        wait_index = sys.argv.index("--wait")
        wait_time = int(sys.argv[wait_index + 1])
        print("Wait time:", wait_time)
    except (IndexError, ValueError):
        print("Invalid wait time specified. Using default wait time of 5 seconds.")

# Configure Firefox WebDriver to simulate a mobile device
if mobile:
    mobile_emulation = {"deviceName": "iPhone X"}
    options = webdriver.FirefoxOptions()
    options.add_argument("--window-size=375,812")  # Set viewport size to match iPhone X
else:
    options = webdriver.FirefoxOptions()

if headless:
    options.add_argument("--headless")  # Run browser in headless mode

print("Starting Verbose.")
print("")
# Initialize Firefox WebDriver with GeckoDriver
print("Initializing selenium driver.")
driver = webdriver.Firefox(options=options)

try:
    print("Launching browser...")
    # Open Lenovo warranty lookup webpage
    print("Navigating to Lenovo warranty lookup webpage...")
    driver.get("https://pcsupport.lenovo.com/us/en/warranty-lookup#/")

    # Wait for the input field for serial number to be visible and enabled
    print("Waiting for the input field for serial number...")
    serial_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "button-placeholder__input"))
    )

    # Fill in the serial number
    print("Filling in the serial number:", serial_number)
    serial_input.send_keys(serial_number)

    # Find the submit button using its class name
    print("Waiting for the submit button...")
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "basic-search__suffix-btn"))
    )

    # Click on the 'Submit' button
    print("Clicking on the 'Submit' button...")
    submit_button.click()

    # Wait for the warranty information to load
    print(f"Waiting {wait_time} seconds for the warranty information to load...")
    time.sleep(wait_time)

    # Get the HTML content of the page
    print("Getting the HTML content of the page...")
    html_content = driver.page_source

    ### I didn't really care to save this so it was not implimented. Just used the warranty page as a start point. No direct HW Specs page.
    # Save the HTML content to a file
    # file_name = "warranty_info_mobile.html" if mobile else "warranty_info.html"
    # if headless:
    #    file_name = "headless_" + file_name
    # with open(file_name, "w", encoding="utf-8") as f:
    #    f.write(html_content)

    # print("Warranty information saved to", file_name)

    # Get the current URL of the browser
    current_url = driver.current_url
    print("Current URL:", current_url)

    # Remove '/warranty' from the end of the URL if it exists
    if current_url.endswith("/warranty"):
        current_url = current_url[: -len("/warranty")]
        print("Machine URL:", current_url)

    # Navigate to a new URL
    print("Navigating to the machine URL...")
    driver.get(current_url)
    print("Waiting page to load...")

    # Wait for the information to load  <---- this seems to have issues, which is why it just waits in seconds instead.
    # print(f"Waiting for page to load...")
    # page_info = WebDriverWait(driver, 10).until(
    #    EC.visibility_of_element_located((By.CLASS_NAME, "new-home-title"))
    # )

    # Wait for the information to load more
    print(f"Waiting {wait_time} seconds more for information to load...")
    time.sleep(wait_time)

    # Check if cookies popup is open and close
    try:
        close_button = driver.find_element(By.CLASS_NAME, "close-btn")
        # Click the close button
        close_button.click()
        print("Closed the window.")
    except NoSuchElementException:
        print("Close button not found.")

    # Scroll down by 500 pixels
    driver.execute_script("window.scrollBy(0, 300);")

    # Find the specs button using its XPath
    print("Waiting for the specs button...")
    submit_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "/html/body/div[2]/section[2]/div[2]/div[2]/div/div[2]/div[2]/section/div/div/div[4]/div[3]/div[2]/div/span",
            )
        )
    )

    # Click the button
    print("Clicking on the specs button...")
    submit_button.click()

    # Find the element containing the specs information
    print("Waiting for the specs information to load...")
    specs_element = WebDriverWait(driver, 10).until(
        # EC.visibility_of_element_located((By.CLASS_NAME, "spec-info-title"))
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "/html/body/div[2]/section[2]/div[2]/div[2]/div/div[2]/div[2]/section/div/div/div[4]/div[3]/div[2]/div/div",
            )
        )
    )

    ##screenshot <-- not as good as I thought it would be. Visually gets obstucted when screen shotting.
    # Scroll the element into view if necessary (optional)
    #    print("Scrolling the element into view...")
    #    driver.execute_script("arguments[0].scrollIntoView();", specs_element)

    # Take a screenshot of the specs element
    #    print("Taking a screenshot of the specs element...")
    #    specs_screenshot = specs_element.screenshot_as_png

    # Write the screenshot data to a file
    #    with open("specs_screenshot.png", "wb") as f:
    #        f.write(specs_screenshot)

    ##save html
    # Find the element containing the specific class
    specific_element = driver.find_element(By.CLASS_NAME, "new-machinfo-desc")

    # Get the HTML content of the specific element
    specific_html = specific_element.get_attribute("outerHTML")

    # Replace the style attribute to remove display: none
    specific_html = specific_html.replace('style="display: none;"', 'style="')

    # Add the required HTML structure
    html_content = f"<!DOCTYPE html>\n<html>\n<body>\n{specific_html}\n</body>\n</html>"

    # Define the file name with the serial number included
    file_name = f"{serial_number}-HardwareSpecs.html"

    # Save the HTML content to a file
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(html_content)

    print("Machine specs saved to", file_name)

except Exception as e:
    import traceback

    traceback.print_exc()
    print("An error occurred:", e)

finally:
    # Close the browser
    print("Closing the browser...")
    driver.quit()

# Formatting html

print("Parsing HTML file")

# Load HTML file content
with open(file_name, "r") as f:
    html_content = f.read()

# Parse HTML
soup = BeautifulSoup(html_content, "html.parser")

print("Extracting information.")
# Extract title
title = soup.find("h3", attrs={"t": "spec info|Spec Info"}).text

# Extract information
info = soup.find(
    "span",
    attrs={
        "t": "machine info explain|The information contained on this website is for reference only, and its exclusive purpose is to facilitate the service delivery of the factory warranty services for Lenovo products. This information may change at any time without notice."
    },
).text

# Extract configurations
configs = []
config_elements = soup.find_all(class_="desc-config-name")
for element in config_elements:
    name = element.text.strip()
    detail = element.find_next(class_="desc-config-detail").text.strip()
    configs.append((name, detail))

print("Saving formatted information to text file")
# Output formatted information
output_file = os.path.splitext(file_name)[0] + ".txt"
with open(output_file, "w") as f:
    f.write("#####--- " + serial_number + " Hardware Configuration ---#####\n")
    f.write("")
    # f.write("Title: {}\n".format(title))
    # f.write("Information: {}\n".format(info))
    f.write("Configuration:\n")
    for name, detail in configs:
        f.write("  {}: {}\n".format(name, detail))

print("Formatted information saved to", output_file)


print("")
print("")
print("#####---", serial_number, "Hardware Configuration ---#####")
print("")
# Print to console
# print("Title:", title)
# print("Information:", info)
print("Configuration:")
for name, detail in configs:
    print("  {}: {}".format(name, detail))

print("")
print("")
