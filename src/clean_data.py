import pandas as pd
import re
from textblob import TextBlob

# ----------------------------
# 1️⃣ Function to clean text
# ----------------------------
def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = re.sub(r"http\S+", "", text)              # remove URLs
    text = re.sub(r"<.*?>", "", text)                # remove HTML tags
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)      # remove special chars / emojis
    text = text.lower().strip()                      # lowercase + strip
    text = re.sub(r"\s+", " ", text)                # remove extra spaces
    return text

# ----------------------------
# 2️⃣ Function to get sentiment
# ----------------------------
def get_sentiment(text):
    blob = TextBlob(text)
    score = blob.sentiment.polarity
    if score > 0.1:
        return "Positive"
    elif score < -0.1:
        return "Negative"
    else:
        return "Neutral"

# ----------------------------
# 3️⃣ Main function
# ----------------------------
def main():
    # Read raw CSV
    df = pd.read_csv("../data/ac_shadows_reviews.csv")

    # Clean reviews
    df['cleaned_review'] = df['review'].apply(clean_text)

    # Add sentiment
    df['sentiment'] = df['cleaned_review'].apply(get_sentiment)

    # Save cleaned CSV
    df.to_csv("../data/ac_shadows_reviews_cleaned.csv", index=False)
    print(f"Saved cleaned data to ../data/ac_shadows_reviews_cleaned.csv")
    print(f"Total reviews processed: {len(df)}")

# ----------------------------
# 4️⃣ Run if executed directly
# ----------------------------
if __name__ == "__main__":
    main()
