import requests
import pandas as pd
import time

def fetch_steam_reviews(app_id, target_reviews=1000, reviews_per_page=100):
    """
    Fetch Steam reviews with pagination until target_reviews is reached.
    """
    base_url = f"https://store.steampowered.com/appreviews/{app_id}"
    cursor = '*'
    all_reviews = []

    while len(all_reviews) < target_reviews:
        params = {
            'json': 1,
            'filter': 'recent',
            'language': 'english',
            'review_type': 'all',
            'purchase_type': 'all',
            'num_per_page': reviews_per_page,
            'cursor': cursor
        }

        response = requests.get(base_url, params=params)
        data = response.json()

        reviews = data.get('reviews', [])
        if not reviews:
            print("No more reviews found.")
            break

        for r in reviews:
            all_reviews.append({
                "author": r.get('author', {}).get('steamid', ''),
                "review": r.get('review', ''),
                "voted_up": r.get('voted_up', False),
                "votes_up": r.get('votes_up', 0),
                "votes_funny": r.get('votes_funny', 0),
                "weighted_vote_score": r.get('weighted_vote_score', 0),
                "comment_count": r.get('comment_count', 0),
                "timestamp_created": r.get('timestamp_created', 0),
                "timestamp_updated": r.get('timestamp_updated', 0),
            })

        cursor = data.get('cursor')
        print(f"Fetched {len(all_reviews)} reviews so far...")
        if not cursor:
            break

        time.sleep(1)  # avoid hitting Steam servers

    # Trim to target_reviews
    all_reviews = all_reviews[:target_reviews]

    # Convert to DataFrame and save
    df = pd.DataFrame(all_reviews)
    df.to_csv("../data/ac_shadows_reviews.csv", index=False)
    print(f"Saved {len(df)} reviews to ../data/ac_shadows_reviews.csv")

if __name__ == "__main__":
    app_id = 3159330  # Assassin’s Creed Shadows
    fetch_steam_reviews(app_id, target_reviews=1000)
