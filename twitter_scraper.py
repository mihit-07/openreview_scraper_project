import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

# Load the dataset with Google Scholar profiles
df = pd.read_csv("top_100_ai_authors_with_scholar.csv")

# Function to extract Twitter handle from a webpage
def find_twitter_handle(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return "No Twitter found"

        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find all links on the page
        links = soup.find_all("a", href=True)
        
        # Look for Twitter links
        for link in links:
            if "twitter.com" in link["href"]:
                twitter_url = link["href"]
                match = re.search(r"twitter\.com/([A-Za-z0-9_]+)", twitter_url)
                if match:
                    return f"https://twitter.com/{match.group(1)}"
        
        return "No Twitter found"
    except Exception as e:
        return "Error"

# Iterate through each author and find Twitter handles
twitter_handles = []
for index, row in df.iterrows():
    website = row.get("Google Scholar Profile", "")
    if website != "No profile found":
        print(f"Scraping {row['Name']}'s website...")
        twitter_handle = find_twitter_handle(website)
    else:
        twitter_handle = "No profile found"

    twitter_handles.append(twitter_handle)
    time.sleep(2)  # Avoid rate limits

# Add Twitter data to the dataset
df["Twitter Handle"] = twitter_handles

# Save to CSV
df.to_csv("top_100_ai_authors_with_twitter.csv", index=False)

print("Twitter handles saved to 'top_100_ai_authors_with_twitter.csv'")
