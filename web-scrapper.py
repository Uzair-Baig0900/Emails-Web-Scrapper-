from bs4 import BeautifulSoup
import requests
from urllib.parse import urlsplit, urljoin
from collections import deque
import re

# def print_quotes():
#     quotes = [
# #  @@@@@@@@@@@        @      @  @@      @@  @@@@@@@@  @  @@@@@@@@  @@@@@@@
# #            @        @      @  @ @    @ @  @      @  @  @      @  @
# #            @        @      @  @  @  @  @  @      @  @  @      @  @
# #  @@@@@@@@@@@        @      @  @   @@   @  @@@@@@@@  @  @@@@@@@@  @@@@@@@
# #            @        @      @  @        @  @         @  @  @      @
# #            @        @      @  @        @  @         @  @    @    @
# #  @@@@@@@@@@@  RD    @@@@@@@@  @        @  @         @  @     @   @@@@@@@
#     ]
def extract_emails(url):
    """
    Extracts emails from a given URL and its sub-pages.
    """
    urls = deque([url])
    scrapped_url = set()
    emails = set()

    count = 0
    while len(urls):
        count += 1
        if count == 100:
            break
        url = urls.popleft()
        scrapped_url.add(url)

        parts = urlsplit(url)
        base_url = f"{parts.scheme}://{parts.netloc}"
        path = url[:url.rfind('/')+1] if '/' in parts.path else url
        print(f"[{count}] Processing {url}")

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            continue

        new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text))
        emails.update(new_emails)

        soup = BeautifulSoup(response.text, features="lxml")

        for anchor in soup.find_all("a"):
            link = anchor.get("href")
            if link:
                if link.startswith("/"):
                    link = urljoin(base_url, link)
                elif not link.startswith("http"):
                    link = urljoin(path, link)
                if link not in urls and link not in scrapped_url:
                    urls.append(link)

    return emails

if __name__ == "__main__":
    user_url = input("[+] Enter Target URL to scan: ")
    emails = extract_emails(user_url)
    print("Extracted Emails:")
    for email in emails:
        print(email)