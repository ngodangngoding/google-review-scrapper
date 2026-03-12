# config.example.py

# --- Chrome Configuration ---
# Path to your Chrome executable. Change this based on your OS:
# Windows: r"C:\Program Files\Google\Chrome\Application\chrome.exe"
# macOS:   "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
# Linux:   "/usr/bin/google-chrome"
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# Folder path for a dedicated debug profile (keeps your main profile safe)
# Ensure this directory is writable by your user.
CHROME_USER_DATA_DIR = r"C:\temp\chrome-debug"

# Port for CDP (Chrome DevTools Protocol)
CDP_PORT = 9222
CDP_URL = f"http://localhost:{CDP_PORT}"


# --- Scraping Configuration ---
# Target Google Maps URL to scrape reviews from
# Example: Monas in Jakarta
URL_TARGET = (
    "https://www.google.com/maps/place/Monumen+Nasional/"
    "@-6.1753924,106.8271528,15z/data=!4m6!3m5!"
    "1s0x2e69f5d2e764b12d:0x3d2ad6e1e0e9bcc8!8m2!"
    "3d-6.1753924!4d106.8271528!16s%2Fg%2F11b6y8z7x0"
)

# Default number of reviews to collect
TARGET_COUNT = 50
