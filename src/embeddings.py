import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import os
import pickle

# ----------------------------
# 1️⃣ Load cleaned reviews
# ----------------------------
def load_cleaned_reviews(csv_path="../data/ac_shadows_reviews_cleaned.csv"):
    df = pd.read_csv(csv_path)
    # Use the cleaned review text
    texts = df['cleaned_review'].astype(str).tolist()
    return df, texts

# ----------------------------
# 2️⃣ Generate embeddings
# ----------------------------
def generate_embeddings(texts, model_name="all-MiniLM-L6-v2"):
    print("Loading Sentence Transformer model...")
    model = SentenceTransformer(model_name)
    print("Generating embeddings...")
    embeddings = model.encode(texts, show_progress_bar=True)
    return embeddings

# ----------------------------
# 3️⃣ Create FAISS index
# ----------------------------
def create_faiss_index(embeddings, dim=384):
    index = faiss.IndexFlatL2(dim)  # L2 distance
    index.add(np.array(embeddings))
    return index

# ----------------------------
# 4️⃣ Save index and metadata
# ----------------------------
def save_index(index, df, index_path="../data/vectors/faiss_index", metadata_path="../data/vectors/metadata.pkl"):
    os.makedirs(os.path.dirname(index_path), exist_ok=True)
    faiss.write_index(index, index_path)
    # Save metadata (like author, sentiment, votes) for later reference
    df.to_pickle(metadata_path)
    print(f"Saved FAISS index to {index_path}")
    print(f"Saved metadata to {metadata_path}")

# ----------------------------
# 5️⃣ Main function
# ----------------------------
def main():
    df, texts = load_cleaned_reviews()
    embeddings = generate_embeddings(texts)
    index = create_faiss_index(embeddings, dim=embeddings.shape[1])
    save_index(index, df)

if __name__ == "__main__":
    main()
