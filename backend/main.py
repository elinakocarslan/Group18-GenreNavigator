from flask import Flask, jsonify, request
from flask_cors import CORS  # Import CORS
from scipy.spatial.distance import cosine
import numpy as np
import random
from PyDictionary import PyDictionary

app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*"}})
CORS(app)
# CORS(app, resources={r"/api/*": {"origins": "*"}})

# Load GloVe embeddings
def LoadGlove(filepath):
    embeddings = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            values = line.split()
            word = values[0]
            vector = np.asarray(values[1:], dtype='float32')
            embeddings[word] = vector
    return embeddings

glove_file = "backend/glove.6B.50d.txt"
 # Correct path to the file

embeddings = LoadGlove(glove_file)

def calculate_similarity(word1, word2, embeddings):
    """Calculate cosine similarity between two words using GloVe embeddings."""
    if word1 not in embeddings or word2 not in embeddings:
        return 0.0  # Return 0 if a word is not in vocabulary
    vec1 = embeddings[word1]
    vec2 = embeddings[word2]
    similarity = 1 - cosine(vec1, vec2)  # Cosine similarity
    return similarity

# API route to get a random word and its hints
@app.route('/start_game', methods=['GET'])
def start_game():
    print(f"Request received from {request.remote_addr}")
    dictionary = PyDictionary()
    with open("backend/words.txt", "r") as f:
        words = [line.strip() for line in f.readlines() if line.strip() in embeddings]

    target_word = random.choice(words)
    synonyms = dictionary.synonym(target_word) or []
    definition = dictionary.meaning(target_word)
    return jsonify({
        'target_word': target_word,
        'definition': list(definition.values())[0][0] if definition else '',
        'synonyms': synonyms
    })

# API route to calculate similarity between guess and target word
@app.route('/guess', methods=['POST'])
def guess_word():
    data = request.json
    guess = data.get('guess')
    target_word = data.get('target_word')
    similarity = calculate_similarity(guess, target_word, embeddings)
    return jsonify({
        'similarity': similarity
    })

if __name__ == '__main__':
    app.run(debug=True)
