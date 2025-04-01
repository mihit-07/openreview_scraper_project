import openreview
import pandas as pd
import time

import time
import openreview

def safe_get_notes(client, **kwargs):
    """Wraps get_notes with retry on rate limit (429)."""
    while True:
        try:
            return client.get_notes(**kwargs)
        except openreview.OpenReviewException as e:
            if isinstance(e.args[0], dict) and e.args[0].get('status') == 429:
                wait_time = 65  # wait 65 seconds before retrying
                print(f"⏳ Rate limit hit. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise e


client = openreview.Client(baseurl='https://api.openreview.net')

conference_id = 'ICLR.cc/2023/Conference'
submission_invitation = 'ICLR.cc/2023/Conference/-/Blind_Submission'
submissions = client.get_notes(invitation=submission_invitation, limit=1000)
print(f"Total submissions fetched: {len(submissions)}")


data = []

for submission in submissions:
    paper_id = submission.id
    title = submission.content.get('title', 'N/A')
    authors = submission.content.get('authors', [])

    reviews = safe_get_notes(client, forum=paper_id, invitation=f'{conference_id}/Paper{submission.number}/Official_Review')
    num_reviews = len(reviews)
    review_texts = [r.content.get('review', '') for r in reviews]
    avg_review_len = sum(len(r) for r in review_texts) / num_reviews if num_reviews > 0 else 0
    scores = [r.content.get('rating', 'N/A') for r in reviews]

    rebuttals = safe_get_notes(client, forum=paper_id, invitation=f'{conference_id}/Paper{submission.number}/Rebuttal')
    rebuttal_present = len(rebuttals) > 0
    rebuttal_text = rebuttals[0].content.get('comment', '') if rebuttal_present else 'N/A'

    decisions = safe_get_notes(client, forum=paper_id, invitation=f'{conference_id}/Paper{submission.number}/Decision')
    decision = decisions[0].content.get('decision', 'N/A') if decisions else 'N/A'

    data.append({
        'Paper Title': title,
        'Number of Reviews': num_reviews,
        'Average Review Length': avg_review_len,
        'Review Texts': review_texts,
        'Scores': scores,
        'Rebuttal Present': rebuttal_present,
        'Rebuttal Text': rebuttal_text,
        'Authors': authors,
        'Decision': decision
    })

time.sleep(1.5)

df = pd.DataFrame(data)
df.to_csv('iclr_2024_paper_metadata.csv', index=False)
print("✅ Metadata saved to iclr_2024_paper_metadata.csv")
