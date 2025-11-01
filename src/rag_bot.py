import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import openai

# ----------------------------
# 1️⃣ Load environment variables
# ----------------------------
load_dotenv()
AZURE_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

openai.api_type = "azure"
openai.api_key = AZURE_API_KEY
openai.api_base = AZURE_ENDPOINT
openai.api_version = "2023-07-01-preview"

# ----------------------------
# 2️⃣ Load FAISS index + metadata
# ----------------------------
def load_index(index_path="data/vectors/faiss_index", metadata_path="data/vectors/metadata.pkl"):
    index = faiss.read_index(index_path)
    with open(metadata_path, "rb") as f:
        df = pickle.load(f)
    return index, df

# ----------------------------
# 3️⃣ Embed the query
# ----------------------------
def embed_query(query, model_name="all-MiniLM-L6-v2"):
    model = SentenceTransformer(model_name)
    embedding = model.encode([query])
    return np.array(embedding)

# ----------------------------
# 4️⃣ Retrieve top-k reviews
# ----------------------------
def retrieve_reviews(query_embedding, index, df, k=5):
    distances, indices = index.search(query_embedding, k)
    reviews = df.iloc[indices[0]]['cleaned_review'].tolist()
    return reviews

# ----------------------------
# 5️⃣ Call Azure OpenAI LLM
# ----------------------------
def generate_answer(query, retrieved_reviews, max_tokens=300):
    context = "\n".join(retrieved_reviews)
    prompt = f"""
You are a helpful assistant. Answer the user's question based on the following game reviews.
Answer the user’s question **ONLY using the retrieved Steam reviews** provided below. Please politely reject the other questions which are not related to game reviews.
Do not use tag like you and bot in the response, you can just give the response.
You can also provide numbers and percentages if required in the response.
DO NOT MAKEUP INFORMATION.

Context:
{context}

User Question:
{query}

Answer concisely using the review information.
"""
    response = openai.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),   # Use your Azure deployment name here
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens
    )
    answer = response.choices[0].message.content
    return answer


# ----------------------------
# 6️⃣ Main function to query bot
# ----------------------------
def ask_bot(query, k=5):
    index, df = load_index()
    query_embedding = embed_query(query)
    retrieved_reviews = retrieve_reviews(query_embedding, index, df, k)
    answer = generate_answer(query, retrieved_reviews)
    return answer

# ----------------------------
# 7️⃣ Example usage
# ----------------------------
if __name__ == "__main__":
    user_query = input("Enter your question about Assassin's Creed Shadows: ")
    answer = ask_bot(user_query)
    print("\nBot Answer:\n", answer)
