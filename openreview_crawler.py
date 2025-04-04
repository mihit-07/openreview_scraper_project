import requests
import pandas as pd
from tqdm import tqdm
import time

# Output file name
VENUE_ID = "ICLR.cc/2023/Conference"
VENUE_SHORT = "iclr2023"
DATE_STR = time.strftime("%Y%m%d")
OUTPUT_FILE = f"{VENUE_SHORT}_{DATE_STR}_simplified.csv"

def get_all_notes():
    """Fetches all blind submissions for ICLR 2023."""
    invitation = f"{VENUE_ID}/-/Blind_Submission"
    offset = 0
    notes = []

    while True:
        print(f"Fetching offset {offset}...")
        url = f"https://api.openreview.net/notes?invitation={invitation}&offset={offset}"
        response = requests.get(url)
        data = response.json()

        if not data.get("notes"):
            break

        notes.extend(data["notes"])
        offset += 1000

    print(f"✅ Total submissions fetched: {len(notes)}")
    return notes

def simplify_note(note):
    """Extracts useful fields from each submission."""
    return {
        "Paper Title": note.get("content", {}).get("title", ""),
        "Authors": note.get("content", {}).get("authors", []),
        "TLDR": note.get("content", {}).get("TL;DR", ""),
        "Abstract": note.get("content", {}).get("abstract", ""),
        "Keywords": note.get("content", {}).get("keywords", []),
        "PDF Link": f"https://openreview.net{note.get('content', {}).get('pdf', '')}",
        "OpenReview Forum": f"https://openreview.net/forum?id={note.get('forum')}"
    }

def main():
    raw_notes = get_all_notes()
    print("🔍 Gathering metadata for each paper...")
    simplified_data = [simplify_note(note) for note in tqdm(raw_notes)]
    df = pd.DataFrame(simplified_data)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"📁 Done! Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
