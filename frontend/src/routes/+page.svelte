<script>
  import { onMount } from 'svelte';

  let targetWord = '';
  let definition = '';
  let synonyms = [];
  let guess = '';
  let similarity = 0;
  let message = '';
  let hintMessage = '';
  let gameOver = false;
  let showCongrats = false;
  let gameWon = false;
  let guessHistory = []; // Array to track guesses and similarity scores
  let numberOfGuesses = 0; // Counter for the number of guesses

  onMount(async () => {
    await startNewGame();
  });

  // Function to start a new game
  async function startNewGame() {
    // Reset all necessary state
    gameOver = false;
    showCongrats = false;
    gameWon = false;
    guess = '';
    similarity = 0;
    message = '';
    hintMessage = '';
    guessHistory = [];
    numberOfGuesses = 0;

    // Fetch the game data from the backend
    try {
      const res = await fetch('/start_game', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      });

      if (res.ok) {
        const data = await res.json();
        targetWord = data.target_word;
        definition = data.definition;
        synonyms = data.synonyms;
      } else {
        console.error("Failed to fetch the game data:", res.statusText);
      }
    } catch (error) {
      console.error('Error fetching game data:', error);
    }
  }

  // Function to handle guess submission
  async function submitGuess() {
    if (gameOver) return;  // If the game is over, do not accept any more guesses

    if (guess === "give up") {
      message = `The target word was: ${targetWord}`;
      gameOver = true; 
      showCongrats = true;
      return;
    }

    if (guess === "hint") {
      getHint();
    } else {
      const res = await fetch('/guess', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ guess }),
      });

      const data = await res.json();
      similarity = data.similarity;
      message = similarity > 0.5 ? "Try Again!" : "Good Guess!";

      // Store the guess and its similarity
      guessHistory.push({ guess, similarity });
      numberOfGuesses++;

      // Check if the guess is correct
      if (guess === targetWord) {
        gameOver = true;
        gameWon = true;
        message = `Congratulations! You guessed the word: ${targetWord}`;
      }
    }
  }

  // Function to handle hint request
  async function getHint() {
    if (targetWord) {
      const res = await fetch('/hint', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ target_word: targetWord }),
      });

      const data = await res.json();
      hintMessage = data.hint;
    }
  }
</script>

<main>
  <h1>Contexto Game</h1>
  <p class="hint">Try to guess the target word!</p>
  <p><strong>Hint:</strong> The target word has {targetWord.length} letters.</p>

  <input type="text" bind:value={guess} placeholder="Enter your guess or 'hint' for a clue" />
  <button on:click={submitGuess} disabled={gameOver}>Submit Guess</button>

  {#if hintMessage}
    <p><strong>Hint:</strong> {hintMessage}</p>
  {/if}

  {#if message}
    <p>{message}</p>
  {/if}

  <p>Similarity Score: {similarity}</p>

  <h3>Guess History</h3>
  <ul>
    {#each guessHistory as { guess, similarity }}
      <li>Guess: {guess} - Similarity: {similarity}</li>
    {/each}
  </ul>

  <p>Total Guesses: {numberOfGuesses}</p>

  {#if gameOver}
    <div class="congrats">
      {#if gameWon}
      <h2>Congrats!</h2>
      {/if}
      <p>The target word was: <strong>{targetWord}</strong></p>
      {#if !gameWon}
        <p>You gave up after {numberOfGuesses} guesses!</p>
      {/if}
    </div>

    <!-- Play Again Button -->
    <button on:click={startNewGame}>Play Again</button>
  {/if}
</main>

<style>
  main {
    text-align: center;
    font-family: Arial, sans-serif;
    padding: 20px;
    background-color: #f7f7f7;
    border-radius: 8px;
    width: 400px;
    margin: 0 auto;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }

  h1 {
    font-size: 32px;
    color: #333;
  }

  p {
    font-size: 16px;
    color: #555;
  }

  .hint {
    font-weight: bold;
    color: #007BFF;
  }

  input {
    padding: 12px;
    font-size: 18px;
    width: 100%;
    margin-bottom: 20px;
    border-radius: 4px;
    border: 1px solid #ccc;
    box-sizing: border-box;
  }

  button {
    padding: 12px 20px;
    font-size: 16px;
    cursor: pointer;
    background-color: #007BFF;
    color: white;
    border: none;
    border-radius: 4px;
    transition: background-color 0.3s;
  }

  button:hover {
    background-color: #0056b3;
  }

  p:last-child {
    font-weight: bold;
    font-size: 18px;
    color: #333;
  }

  .congrats {
    text-align: center;
    margin-top: 20px;
    font-size: 20px;
    background-color: #f7f7f7;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }

  .congrats h2 {
    font-size: 48px; 
    color: #4CAF50;
    font-weight: bold;
    margin-bottom: 20px;
  }

  .congrats p {
    font-size: 24px;
    color: #333;
  }

  ul {
    list-style-type: none;
    padding: 0;
  }

  li {
    font-size: 16px;
    color: #333;
  }
</style>
