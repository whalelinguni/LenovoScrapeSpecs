# Lenovo Warranty Lookup and Hardware Specifications Scraper

This Python script automates the process of looking up warranty information for Lenovo products and scraping hardware specifications from the Lenovo support website. It uses Selenium WebDriver to interact with the website and extract relevant information.

## Usage

To use this script, follow the instructions below:

1. Clone this repository to your local machine:
2. Install the required dependencies:
   ```
   pip install selenium
   ```
3. Run the script with the following command:
   ```
   python script.py <serial_number> [--mobile] [--headless] --wait <seconds>
   ```
   Replace `<serial_number>` with the serial number of your Lenovo product.

## Command-line Arguments

- `<serial_number>`: The serial number of the Lenovo product.
- `--mobile`: (Optional) Enable mobile mode to simulate browsing from a mobile device.
- `--headless`: (Optional) Enable headless mode to run the browser without a graphical interface.
- `--wait <seconds>`: (Optional) Specify the wait time in seconds for the page to load.

Example usage:
```
python script.py PG01GTB2 --headless --wait 10
```

This command will look up the warranty information for the product with serial number `PG01GTB2`, console only, and wait for 10 seconds for the page to load.

## Notes

- The warranty HTML save functionality is not fully implemented and is commented out.
- The screenshot function may not capture the desired content accurately and was also commented out.
- Make sure to verify the saved HTML file for hardware specifications as it may not always capture the exact content due to website changes or inconsistencies.
