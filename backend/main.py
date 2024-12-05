from flask import Flask, jsonify, request
from flask_cors import CORS  # Ensure you have this imported
from PyDictionary import PyDictionary
import nltk
import random
import numpy as np
from nltk.corpus import wordnet as wn
from scipy.spatial.distance import cosine

# Initialize Flask app and CORS
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
# CORS(app, resources={r"/*": {"origins": "*", "allow_headers": "*", "methods": "*"}})
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

# Function to check if a word is a synonym of another word
def is_synonym(guess, target_word):
    synonyms = get_synonyms(target_word)
    return guess in synonyms

# Function to load GloVe embeddings from file
def LoadGlove(filepath):
    embeddings = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            values = line.split()
            word = values[0]
            vector = np.asarray(values[1:], dtype='float32')
            embeddings[word] = vector
    return embeddings

# Function to calculate similarity between two words using GloVe and WordNet
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
        if is_synonym(word1, word2):
            graded_score = int((1 - combined_similarity) * 1000) / 2 - 50
        else:
            graded_score = int((1 - combined_similarity) * 1000)
        return graded_score

# Function to get hints for a word (synonyms and related words)
def get_hints(word, embeddings):
    synonyms = get_synonyms(word)
    if not synonyms:
        return "No synonyms available."
    
    graph = build_synonym_graph(word, embeddings)

    if word not in graph:
        word = synonyms[0]

    distances = dijkstra(graph, word)
    closest_synonym = min(distances, key=distances.get)  
    return closest_synonym

# Function to build a graph of synonyms based on similarity
def build_synonym_graph(word, embeddings):
    synonyms = get_synonyms(word)
    if not synonyms:
        print(f"No synonyms to build graph for {word}")
        return {}  
    graph = {}
    for synonym1 in synonyms:
        graph[synonym1] = []
        for synonym2 in synonyms:
            if synonym1 != synonym2:
                if synonym1 in embeddings and synonym2 in embeddings:
                    dist = calculate_similarity(synonym1, synonym2, embeddings, weight_glove=0.5, weight_wordnet=0.5)
                    graph[synonym1].append((dist, synonym2))
    return graph

# Dijkstra's algorithm for finding shortest paths
def dijkstra(graph, start):
    pq = [(0, start)]  
    distances = {node: float('inf') for node in graph}
    distances[start] = 0

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        if current_distance > distances[current_node]:
            continue

        for neighbor_distance, neighbor in graph[current_node]:
            distance = current_distance + neighbor_distance

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))

    return distances

# Loading GloVe file for embeddings
glove_file = "backend/glove.6B.50d.txt"  # Path to GloVe file
embeddings = LoadGlove(glove_file)

# List of words to choose a random target word from
with open("backend/words.txt", "r") as f:
    words = [line.strip() for line in f.readlines() if line.strip() in embeddings]

# Choosing a random target word
target_word = random.choice(words)
while len(get_synonyms(target_word)) == 0:
    target_word = random.choice(words)

print(target_word)

def get_random_synonym(word):
    synonyms = get_synonyms(word)
    if synonyms:
        return random.choice(synonyms)  # Return a random synonym
    return "No synonyms available"

# Flask route to start the game and provide the target word and hints
@app.route('/start_game', methods=['GET'])
def start_game():
    synonyms = get_synonyms(target_word)
    definition = "Definition of the word"  # Add logic for definition if needed
    return jsonify({
        'target_word': target_word,
        'definition': definition,
        'synonyms': synonyms
    })

# Flask route to submit a guess and get the similarity score
@app.route('/guess', methods=['POST'])
def guess_word():
    data = request.json
    guess = data.get('guess')
    similarity = calculate_similarity(guess, target_word, embeddings)
    return jsonify({
        'similarity': similarity
    })

@app.route('/hint', methods=['GET'])
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
