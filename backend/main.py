import numpy as np
import heapq
from scipy.spatial.distance import cosine
from PyDictionary import PyDictionary
import nltk
from nltk.corpus import wordnet as wn
import random
from flask import Flask, jsonify, request
from flask_cors import CORS

# Initialize Flask app and CORS
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

nltk.download('wordnet')

# Function to get synonyms using NLTK's WordNet
def get_synonyms(word):
    synonyms = set()
    synsets = wn.synsets(word, lang='eng')
    if not synsets:
        return []

    for synset in synsets:
        for lemma in synset.lemmas():
            synonym = lemma.name()
            if synonym.isalpha() and synonym.lower() != word.lower():
                synonyms.add(synonym.replace("_", " "))
    return list(synonyms)

# Function to calculate similarity using GloVe embeddings and WordNet
def calculate_similarity(word1, word2, embeddings, weight_glove=0.5, weight_wordnet=0.5):
    if word1 not in embeddings or word2 not in embeddings:
        glove_similarity = None
    else:
        vec1 = embeddings[word1]
        vec2 = embeddings[word2]
        glove_similarity = 1 - cosine(vec1, vec2)

    synsets1 = wn.synsets(word1)
    synsets2 = wn.synsets(word2)
    if not synsets1 or not synsets2:
        return 0

    synset1 = synsets1[0]
    synset2 = synsets2[0]

    wordnet_similarity = synset1.path_similarity(synset2)

    if glove_similarity is None and wordnet_similarity == 0:
        return 1000

    if glove_similarity is None:
        combined_similarity = wordnet_similarity
    elif wordnet_similarity == 0:
        combined_similarity = glove_similarity
    else:
        combined_similarity = (weight_glove * glove_similarity) + (weight_wordnet * wordnet_similarity)

    if combined_similarity == 1:
        return 1
    elif combined_similarity < 0:
        return 1000
    else:
        graded_score = int((1 - combined_similarity) * 1000)
        return graded_score

# Function to load GloVe embeddings
def LoadGlove(filepath):
    embeddings = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            values = line.split()
            word = values[0]
            vector = np.asarray(values[1:], dtype='float32')
            embeddings[word] = vector
    return embeddings

# Load GloVe embeddings
glove_file = "backend/glove.6B.50d.txt"  # Make sure this is the correct path to the GloVe file
embeddings = LoadGlove(glove_file)

# Function to get a random synonym
def get_random_synonym(word):
    synonyms = get_synonyms(word)
    if synonyms:
        return random.choice(synonyms)
    return "No synonyms available"

# Initialize game variables
with open("backend/words.txt", "r") as f:
    words = [line.strip() for line in f.readlines() if line.strip() in embeddings]

target_word = random.choice(words)
while len(get_synonyms(target_word)) < 2:
    target_word = random.choice(words)

def get_new_target_word():
    with open("backend/words.txt", "r") as f:
        words = [line.strip() for line in f.readlines() if line.strip() in embeddings]
    
    target_word = random.choice(words)
    while len(get_synonyms(target_word)) < 2:
        target_word = random.choice(words)
    
    return target_word
    
# Flask route to start the game
@app.route('/start_game', methods=['GET'])
def start_game():
    definition = "Definition of the word"
    target_word = get_new_target_word()
    synonyms = get_synonyms(target_word)
    return jsonify({
        'target_word': target_word,
        'definition': definition,
        'synonyms': synonyms
    })

# Flask route to submit a guess and get similarity score
@app.route('/guess', methods=['POST'])
def guess_word():
    data = request.json
    guess = data.get('guess')
    similarity = calculate_similarity(guess, target_word, embeddings)
    return jsonify({'similarity': similarity})

# Flask route to get a hint (synonym)
@app.route('/hint', methods=['POST'])
def hint():
    data = request.json
    target_word = data.get('target_word')
    synonym = get_random_synonym(target_word)
    return jsonify({'hint': synonym})

@app.before_request
def handle_preflight():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(debug=True)
