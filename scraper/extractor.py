import time


def extract_card(card, seen_text: set) -> dict | None:
    """Extract review data from a single DOM card. Returns dict or None."""
    try:
        username_el = card.query_selector(".d4r55")
        if not username_el:
            return None
        username = username_el.inner_text().strip()

        # Expand long reviews
        try:
            more_btn = card.query_selector("button.w8nwRe")
            if more_btn:
                more_btn.click()
                time.sleep(0.3)
        except Exception:
            pass

        # Try multiple selectors for review text
        text_el = (
            card.query_selector(".wiI7pd")
            or card.query_selector(".MyEned")
            or card.query_selector(".wi772b")
        )
        if not text_el:
            return None

        text_content = text_el.inner_text().strip()
        if not text_content or text_content in seen_text:
            return None

        # Extract rating via JS (filter specifically for span[role="img"])
        rating = card.evaluate(
            """el => {
                const elements = el.querySelectorAll('span[role="img"][aria-label]');
                for (let e of elements) {
                    const label = e.getAttribute('aria-label').toLowerCase();
                    if (label.includes('bintang') || label.includes('star')) {
                        return e.getAttribute('aria-label');
                    }
                }
                
                const fallback = el.querySelector('.kvMYJb');
                if (fallback && fallback.hasAttribute('aria-label')) {
                    const label = fallback.getAttribute('aria-label').toLowerCase();
                    if (label.includes('bintang') || label.includes('star')) {
                        return fallback.getAttribute('aria-label');
                    }
                }
                
                return 'N/A';
            }"""
        )

        # Extract review relative time
        waktu = card.evaluate(
            """el => {
                const t = el.querySelector('.rsqaWe');
                return t ? t.innerText.trim() : 'N/A';
            }"""
        )

        return {
            "Username": username,
            "Rating": rating,
            "Isi Ulasan": text_content,
            "Waktu Ulasan": waktu,
        }

    except Exception:
        return None
