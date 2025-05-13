# Semantic RAG: Replace keyword-matching with vector search on idea history
import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# File to read previous ideas from
SESSION_LOG_FILE = "JSON\\session_log.json"

# Build vector index from past ideas
def build_faiss_index(log_file=SESSION_LOG_FILE):
    #Open the Json file and Load the data
    if not os.path.exists(log_file):
        return None, []

    #And store the dat in a variable call sessions
    with open(log_file, "r", encoding="utf-8") as f:
        sessions = json.load(f)

    #Extract the existing ideas from the sessions and store them in embeddings. Embedding is a process of converting the text into a numerical representation that can be used for similarity search.
    ideas = [entry["Idea"] for entry in sessions if "Idea" in entry]
    if not ideas:
        return None, []
    embeddings = model.encode(ideas, normalize_embeddings=True)
    
    # Create a FAISS index for the embeddings and store the embeddings into it.
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))

    return index, sessions

# Search by semantic meaning
def find_related_context(current_idea: str, k=2, threshold=0.7) -> str:
    index, sessions = build_faiss_index()
    #If there is no index value from the faiss index or no sessions value from the session history, return an empty string.
    if not index or not sessions:
        return ""

    #Embed the current idea that user put it in
    query_vector = model.encode([current_idea], normalize_embeddings=True) #A[1,1] and B[10,10] so by doing noramlization it will be more accurate. Both are going same direction but the value is just bigger
    #Ask the faiss to find the k closest(user input) vectors in the index.
    D, I = index.search(np.array(query_vector), k)

    #Fassis will return the closest matches, even if they’re not very close, if distance D[0] is really high, it means that the idea is not similar to any of the previous ones. Fassis just chose the one that least unrelated.
    #Since we set k = 2 it will return 2 closest matches, So D[[0.12, 0.5]] the first index(Distance) is the closest match, and the second one is the second closest match.
    #And also I[[0,2]] the first index is the index of the closest match, and the second one is the index of the second closest match.
    
    #Format it into a string that can be injected into an LLM prompt
    results = []
    for dist, i in zip(D[0],I[0]):
        if dist < threshold:
            session = sessions[i]
            context_block = f"Idea: {session['Idea']}\nAnalysis: {session.get('Market Analysis', '')}\nSuggestions: {session.get('Suggestions', '')}\n---"
            results.append(context_block)
        else:
            print(f"Distance {dist} exceeds threshold {threshold}. Skipping session.")
    return "\n".join(results).strip()

# Example
# if __name__ == "__main__":
#     idea = "Dog toy market"
#     context = find_related_context(idea)
#     print("\n🔍 Similar Past Ideas Based on Meaning:\n")
#     print(context or "No related sessions found.")
