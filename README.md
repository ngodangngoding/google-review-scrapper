# Google Maps Review Scraper

A Python script to scrape review data from Google Maps. It uses Playwright and connects directly to a local, independently launched Chrome browser instance to bypass Google's bot detection mechanisms.

The extracted data includes:
- Reviewer name
- Rating (Stars)
- Review relative time
- Review text content

The final output is saved automatically as an Excel (.xlsx) file inside the `data/` folder.

## Prerequisites

1. Python installed (version 3.9+ recommended)
2. Google Chrome installed on your local machine

## Installation

1. Clone this repository:
```bash
git clone https://github.com/ngodangngoding/google-review-scrapper.git
cd google-review-scrapper
```

2. (Recommended) Create and activate a virtual environment:
```bash
python -m venv venv
```
Activate it:
- Windows: `venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`

3. Install the required python packages:
```bash
pip install -r requirement.txt
```

4. Install the Playwright browser binaries (only needed once):
```bash
playwright install chromium
```

## Configuration

Before running the script, you need to set up your local configuration.

1. Duplicate the `config.example.py` file.
2. Rename the duplicated file to `config.py`.
3. Open `config.py` and change the `URL_TARGET` to the specific Google Maps place URL you want to scrape.
4. Ensure the `CHROME_PATH` matches the location of the Google Chrome executable on your local machine.

## Usage

You can run the script via the command line or terminal.

To run with the default number of target reviews (defined in config.py):
```bash
python main.py
```

To specify the exact number of reviews you want to scrape (e.g., 100 reviews):
```bash
python main.py 100
```
Alternatively:
```bash
python main.py --target 100
```

### How It Works:
When executed, the script will automatically launch a new Chrome window dedicated strictly for debugging (this prevents conflicts with your primary Chrome profile). Leave this Chrome window open. Once the scraper has collected the required amount of data, the browser will close automatically, and you can find your generated Excel file inside the `data/` directory.

## Project Structure

- `main.py`: The entry point to run the scraper.
- `config.py`: Local settings configuration (URL target, Chrome paths, default targets).
- `scraper/`: Contains the core scraping logic (browser connection, tab navigation, scrolling, and DOM element extraction).
- `data/`: The directory where all output Excel (.xlsx) files are saved.
