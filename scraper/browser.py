import subprocess
import time

from playwright.sync_api import sync_playwright
from config import CDP_URL, CDP_PORT, CHROME_PATH, CHROME_USER_DATA_DIR


def _is_chrome_running() -> bool:
    """Check if Chrome CDP port is active."""
    import urllib.request
    try:
        urllib.request.urlopen(f"http://localhost:{CDP_PORT}/json", timeout=2)
        return True
    except Exception:
        return False


def launch_chrome() -> subprocess.Popen | None:
    """Launch Chrome with remote debugging if not running."""
    if _is_chrome_running():
        print("[INFO] Chrome already running, connecting...")
        return None

    print("[INFO] Starting Chrome...")
    proc = subprocess.Popen([
        CHROME_PATH,
        f"--remote-debugging-port={CDP_PORT}",
        f"--user-data-dir={CHROME_USER_DATA_DIR}",
    ])

    for i in range(10):
        time.sleep(1)
        if _is_chrome_running():
            print(f"[INFO] Chrome ready ({i + 1}s).")
            return proc

    print("[ERROR] Chrome timeout.")
    proc.terminate()
    return None


def connect_browser():
    """Connect to Chrome via CDP. Returns (playwright, browser, page)."""
    p = sync_playwright().start()

    try:
        browser = p.chromium.connect_over_cdp(CDP_URL)
    except Exception as e:
        p.stop()
        print(f"[ERROR] Connection failed: {e}")
        return None, None, None

    context = browser.contexts[0]
    page = context.new_page()
    page.set_extra_http_headers({"Accept-Language": "id-ID,id;q=0.9"})

    return p, browser, page
