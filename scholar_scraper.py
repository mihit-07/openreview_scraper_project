from serpapi import GoogleSearch
import pandas as pd
import time

# Your SerpAPI key (Replace with your actual key)
SERPAPI_KEY = "e02324fb9d253d0ff09a2ad03407e03123977feaae1427573f4a0c2570772c7c"

# Load the top 100 AI authors from the CSV file
authors_df = pd.read_csv("top_100_ai_authors.csv")

# Function to search Google Scholar profile using SerpAPI
def get_google_scholar_profile(name, affiliation):
    query = f"{name} {affiliation} site:scholar.google.com"
    
    params = {
        "q": query,
        "engine": "google",
        "api_key": SERPAPI_KEY
    }
    
    search = GoogleSearch(params)
    results = search.get_dict()
    
    for result in results.get("organic_results", []):
        if "scholar.google.com/citations" in result["link"]:
            return result["link"]  # Return the profile link
    
    return "No profile found"

# Iterate over each author and find their Google Scholar profile
scholar_profiles = []
for index, row in authors_df.iterrows():
    print(f"Searching for {row['Name']}...")
    profile_link = get_google_scholar_profile(row["Name"], row["Affiliation"])
    scholar_profiles.append(profile_link)
    
    time.sleep(2)  # Prevent rate-limiting

# Add results to the DataFrame
authors_df["Google Scholar Profile"] = scholar_profiles

# Save to CSV
authors_df.to_csv("top_100_ai_authors_with_scholar.csv", index=False)

print("✅ Google Scholar profiles saved to top_100_ai_authors_with_scholar.csv")
