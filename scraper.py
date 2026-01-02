import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import hashlib
import time

START_URL = "https://revnix.com"
OUTPUT_FILE = "revnix_data.txt"
DELAY = 1.0

visited_urls = set()
queued_urls = [START_URL]

seen_text_hashes = set()

HEADERS = {
    "User-Agent": "RevnixKnowledgeBot/1.0"
}

def canonical_url(url: str) -> str:
    parsed = urlparse(url)
    clean = parsed.scheme + "://" + parsed.netloc + parsed.path
    return clean.rstrip("/")

def is_internal(url: str) -> bool:
    return urlparse(url).netloc == urlparse(START_URL).netloc

def is_noise_page(url: str) -> bool:
    noise = [
        "/blog/tag/",
        "/blog/category/",
        "?",
    ]
    return any(n in url for n in noise)

def extract_job_text(soup: BeautifulSoup) -> str:
    """
    Extract structured job info if on a careers page or job detail page
    """
    blocks = []

    # Try to extract job listings
    job_sections = soup.find_all(["div", "section"], class_=lambda x: x and "job" in x.lower())
    for job in job_sections:
        # Title
        title = job.find(["h2", "h3", "h4"])
        if title:
            blocks.append(f"Job Title: {title.get_text(strip=True)}")

        # Description paragraphs
        for p in job.find_all("p"):
            text = p.get_text(" ", strip=True)
            if text:
                blocks.append(text)

        # Details like department, job type, location
        details = job.find_all("li")
        for d in details:
            text = d.get_text(" ", strip=True)
            if text:
                blocks.append(text)

    return "\n".join(blocks)

def extract_clean_text(html: str) -> str:
    """
    Extract normal page text, excluding noise
    """
    soup = BeautifulSoup(html, "html.parser")

    # Try to get job info first
    job_text = extract_job_text(soup)
    if job_text:
        return job_text

    # If no jobs found, extract normal content
    for tag in soup(["script", "style", "noscript", "svg", "header", "footer", "nav"]):
        tag.decompose()

    blocks = []
    for tag in soup.find_all(["h1", "h2", "h3", "h4", "p", "li"]):
        text = tag.get_text(" ", strip=True)
        if len(text) > 25:
            blocks.append(text)

    unique_blocks = []
    local_seen = set()
    for block in blocks:
        normalized = " ".join(block.lower().split())
        if normalized not in local_seen:
            local_seen.add(normalized)
            unique_blocks.append(block)

    return "\n".join(unique_blocks)

def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

with open(OUTPUT_FILE, "w", encoding="utf-8") as output:

    while queued_urls:
        url = canonical_url(queued_urls.pop(0))

        if url in visited_urls or is_noise_page(url):
            continue

        visited_urls.add(url)
        print(f"Scraping: {url}")

        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            if r.status_code != 200:
                continue

            soup = BeautifulSoup(r.text, "html.parser")

            text = extract_clean_text(r.text)
            if not text:
                continue

            h = content_hash(text)
            if h in seen_text_hashes:
                continue

            seen_text_hashes.add(h)

            output.write("\n" + "=" * 90 + "\n")
            output.write(f"URL: {url}\n")
            output.write("=" * 90 + "\n")
            output.write(text + "\n")

            # Queue internal links
            for link in soup.find_all("a", href=True):
                full = canonical_url(urljoin(url, link["href"]))
                if is_internal(full) and full not in visited_urls:
                    queued_urls.append(full)

            time.sleep(DELAY)

        except Exception as e:
            print(f"Error scraping {url}: {e}")

print("SCRAPING COMPLETE — revnix_data.txt READY")
print(f"Total unique pages: {len(visited_urls)}")
print(f"Total unique knowledge blocks: {len(seen_text_hashes)}")
