import re
import time
import argparse
import pandas as pd
from datetime import datetime
from config import URL_TARGET, TARGET_COUNT
from scraper.browser import launch_chrome, connect_browser
from scraper.scrolling import run_scrape


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Google Maps Review Scraper",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "target",
        nargs="?",                 
        type=int,
        default=TARGET_COUNT,
        help=f"Target number of reviews to collect (default: {TARGET_COUNT})",
    )
    
    parser.add_argument(
        "--target",
        dest="target_flag",
        type=int,
        default=None,
        metavar="N",
        help="Alternative: --target 100",
    )
    return parser.parse_args()


def build_filename(url: str) -> str:
    """Generate Excel filename from place name and timestamp."""
    match = re.search(r"/place/([^/@]+)", url)
    place_raw = match.group(1) if match else "place"
    place_name = place_raw.replace("+", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"data/{place_name}_{timestamp}.xlsx"


def main():
    args = parse_args()
    target = args.target_flag if args.target_flag is not None else args.target
    print(f"Target reviews: {target}")

    chrome_proc = launch_chrome()

    p, browser, page = connect_browser()
    if page is None:
        return

    try:
        separator = "&" if "?" in URL_TARGET else "?"
        url_id = URL_TARGET + separator + "hl=id"

        print(f"Opening URL...")
        page.goto(url_id, wait_until="domcontentloaded", timeout=60000)
        time.sleep(6) 

        print("Starting scrape...")
        data = run_scrape(page, target)

    finally:
        page.close()
        p.stop()
        if chrome_proc is not None:
            print("[INFO] Closing Chrome...")
            chrome_proc.terminate()

    if data:
        filename = build_filename(URL_TARGET)
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)
        print(f"\nDone! {len(data)} records saved to '{filename}'")
    else:
        print("\nNo data collected.")


if __name__ == "__main__":
    main()
