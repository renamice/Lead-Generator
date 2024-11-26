import datetime
import json
import os
import random
import re
import time

import requests
from bs4 import BeautifulSoup
from cleantext import clean
from googlesearch import search

from config import FIELD, LOCATION, RESULTS


def main():
    init(FIELD, LOCATION, RESULTS)


# String String Ineger -> String
# takes in field, area, and no.of results to produce; logs them and returns the filepath
def init(field, area, results):
    profiles = find_urls(field, area, results)

    data = get_info(profiles)

    return log_data(data)


# list -> String
# saves the list of dictiorany and returns the filepath
def log_data(data):
    # current time
    timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    filename = f"{timestamp} Instagram Leads.json"

    data.insert(0, {"timestamp": timestamp, "platform": "instagram"})

    sub_folder = os.path.join(".", "leads")
    os.makedirs(sub_folder, exist_ok=True)

    filepath = os.path.join(sub_folder, filename)

    with open(filepath, "w") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    print(f"Data logged successfully at {filepath}.")
    return filepath


# list -> list
# takes in a list of urls and returns a list of dictionaries
def get_info(urls):
    data = []
    tracker = 0
    for url in urls:
        data.append(info(url))
        if tracker % 5 == 0:
            delay_request()
    return data


# Integer Integer -> Integer
# sleeps for a random about of time between first integer and the second
# IMPORTANT: do not remove or shorten the time limit, the IP might get banned
def delay_request(min_delay=60, max_delay=120):
    delay = random.randint(min_delay, max_delay)  # Random delay between min and max
    time.sleep(delay)


# String String Integer -> List
# takes in "field" and "location" returns a list of provided length filled with instagram profile links satisfying them
def find_urls(field, location, number):
    query = f"site:instagram.com '{field}' '{location}' 'email'"

    results = search(query, num_results=number)
    # cleaning the urls in case they have a post attached to them instead of just being profile urls
    urls = [
        re.match(r"(https://www\.instagram\.com/[^/]+/)", url).group(1)
        for url in results
    ]
    return urls


# String -> Dictionary or None
# produces a "title:biography" dict or None if failed
def info(url):
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch profile: {response.status_code}")
        return None

    parsed = BeautifulSoup(response.text, "lxml")
    meta_tag_title = str(parsed.find("meta", property="og:title"))
    meta_tag_bio = parsed.find("meta", attrs={"name": "description"})
    bio_only = meta_tag_bio.get("content").replace("\n", "")
    meta_tag_bio = str(meta_tag_bio)

    profile_name = get_header(meta_tag_title, "name")
    profile_handle = get_header(meta_tag_title, "handle")

    email_in_bio = get_email(meta_tag_bio)

    return {
        "name": profile_name,
        "handle": profile_handle,
        "email": email_in_bio,
        "bio": bio_only,
    }


# String String -> String None
# takes the meta info and returns the data from it depending on the "value"
# returns None if does not match the accepted parameters
def get_header(text, value):
    match = re.match(r"^(.*?) \(@([a-zA-Z0-9._]+)\)", text)

    if value == "name":
        return match.group(1).replace('<meta content="', "")
    if value == "handle":
        return "@" + match.group(2)
    return None


# String String -> String None
# takes the meta info and returns the data from it depending on the "value"
# returns None if does not match the accepted parameters
def get_email(text):
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

    emails = re.findall(email_pattern, text)
    clean_emails = []
    for email in emails:
        clean_emails.append(clean(email, no_emoji=True))

    return clean_emails


if __name__ == "__main__":
    main()
