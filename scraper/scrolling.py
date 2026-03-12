import time
from scraper.extractor import extract_card

SCROLLABLE_SELECTORS = [
    "div.m6QErb.DxyBCb",
    "div.m6QErb",
]


def _find_review_tab(page) -> bool:
    """Click the 'Reviews' tab on Google Maps."""
    tabs = page.query_selector_all("button.hh2c6")
    print(f"[DEBUG] Found {len(tabs)} tabs")
    for i, tab in enumerate(tabs):
        print(f"  tab[{i}] = '{tab.inner_text().strip()}'")

    for tab in tabs:
        text = tab.inner_text().strip().lower()
        if "ulasan" in text or "reviews" in text or text == "review":
            tab.click()
            return True

    print("[DEBUG] Review tab not found via selector, trying JS...")
    clicked = page.evaluate(
        """() => {
            const buttons = Array.from(document.querySelectorAll('button'));
            const btn = buttons.find(b => {
                const t = b.innerText.trim().toLowerCase();
                return t === 'ulasan' || t === 'reviews' || t === 'review';
            });
            if (btn) { btn.click(); return true; }
            return false;
        }"""
    )
    return bool(clicked)


def _find_scrollable_container(page):
    """Find the review scroll container. Returns selector string or None."""
    for sel in SCROLLABLE_SELECTORS:
        if page.query_selector(sel):
            return sel
    return None


def run_scrape(page, target: int) -> list[dict]:
    """Execute scraping process: click review tab, scroll, and extract data."""
    results = []
    seen_text = set()

    if not _find_review_tab(page):
        raise Exception("Review tab not found!")
    time.sleep(3)

    scrollable_sel = _find_scrollable_container(page)
    if scrollable_sel is None:
        raise Exception("Review container not found!")
    print(f"[DEBUG] Container found ({scrollable_sel}). Started scraping...")

    no_new_count = 0
    while len(results) < target:
        page.evaluate(f"document.querySelector('{scrollable_sel}').scrollTop += 3000")
        time.sleep(2)

        scrollable = page.query_selector(scrollable_sel)
        if scrollable is None:
            print("[INFO] Scroll container lost, stopping.")
            break

        cards = scrollable.query_selector_all(".jftiEf")
        count_before = len(results)

        for card in cards:
            data = extract_card(card, seen_text)
            if data:
                results.append(data)
                seen_text.add(data["Isi Ulasan"])

                if len(results) % 50 == 0:
                    print(f"Progress: {len(results)}/{target} collected")

                if len(results) >= target:
                    break

        # Stop if 5 consecutive scrolls yield no new data
        if len(results) == count_before:
            no_new_count += 1
            if no_new_count >= 5:
                print(f"[INFO] All available reviews loaded. Total: {len(results)}")
                break
        else:
            no_new_count = 0

    return results
