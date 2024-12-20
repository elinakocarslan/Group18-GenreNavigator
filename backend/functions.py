import numpy as np
import heapq
from scipy.spatial.distance import cosine
from PyDictionary import PyDictionary
import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet as wn


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


def is_synonym(guess, target_word):
    synonyms = get_synonyms(target_word)
    return guess in synonyms

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

def bellman_ford(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0

    for _ in range(len(graph) - 1):
        for node in graph:
            for weight, neighbor in graph[node]:
                if distances[node] + weight < distances[neighbor]:
                    distances[neighbor] = distances[node] + weight

    return distances

def LoadGlove(filepath):
    embeddings = {}
    with open(filepath, 'r', encoding = 'utf-8') as f:
        for line in f:
            values = line.split()
            word = values[0]
            vector = np.asarray(values[1:], dtype='float32')
            embeddings[word] = vector
    return embeddings

glove_file = "/Users/Jonathan/Downloads/glove.6B.50d.txt"
embeddings = LoadGlove(glove_file)

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
        if(is_synonym(word1,word2)):
            if (int((1-combined_similarity) * 1000)/2 - 50 < 0):
                graded_score = 2
            else:
                graded_score = int((1-combined_similarity) * 1000)/2 - 50
        else:
            graded_score = int((1-combined_similarity) * 1000)

        return graded_score


dictionary = PyDictionary()


# def get_hints(word, target):
#     synonyms = get_synonyms(word)
#     if not synonyms:
#         return "No synonyms available."

#     graph = build_synonym_graph(word, embeddings)
#     if word not in graph:
#         word = synonyms[0]

#     distances = dijkstra(graph, word)
#     sorted_distances = sorted((dist, synonym) for synonym, dist in distances.items() if synonym != word and synonym != target)
#     if not sorted_distances:
#         return "No valid hints available."

#     closest_synonym = sorted_distances[0][1]
#     return closest_synonym


##get hints for bellman ford

def get_hints(word, target):
    synonyms = get_synonyms(word)
    if not synonyms:
        return "No synonyms available."

    graph = build_synonym_graph(word, embeddings)
    if word not in graph:
        word = synonyms[0]

    try:
        distances = bellman_ford(graph, word)
    except ValueError as e:
        print(f"Error in graph: {e}")
        return "No valid hints available."

    sorted_distances = sorted((dist, synonym) for synonym, dist in distances.items() if synonym != word and synonym != target)
    if not sorted_distances:
        return "No valid hints available."

    closest_synonym = sorted_distances[0][1]
    return closest_synonym


import random

with open("words.txt", "r") as f:
    words = [line.strip() for line in f.readlines() if line.strip() in embeddings]

target_word = random.choice(words)

while(len(get_synonyms(target_word)) < 2):
    target_word = random.choice(words)
print(target_word)


def play_contexto():
    print("Welcome to Contexto!")
    print("Try to guess the target word. Similarity scores indicate closeness, the lower the closer.")

    attempts = 0
    hintWord = target_word
    previous_guesses = set()  

    while True:
        guess = input("Enter your guess: ").strip().lower()

        if guess == "give up":
            print(f"The word was {target_word}")
            break
        if guess != "hint":
            if guess in previous_guesses:
                print(f"You've already guessed '{guess}'. Try something different!")
                continue

        if guess not in embeddings:
            print("Invalid word or not in vocabulary. Try again.")
            continue

        previous_guesses.add(guess)

        if guess == "hint":
            word = get_hints(hintWord, target_word)
            if word == target_word:
                word = get_hints(word, target_word)
            hintWord = word
            print(f"Hint: {word}, Similarity: {calculate_similarity(word, target_word, embeddings)}")
        else:
            similarity = calculate_similarity(guess, target_word, embeddings)
            print(f"Your guess: {guess}, Similarity: {similarity:.4f}")

        attempts += 1

        if guess == target_word:
            print(f"Congratulations! You guessed the word in {attempts} attempts.")
            break


play_contexto()