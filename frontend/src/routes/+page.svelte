<script>
  import { onMount } from 'svelte';
  
  let targetWord = '';
  let definition = '';
  let synonyms = [];
  let guess = '';
  let similarity = 0;
  let message = '';
  let hintMessage = '';
  
  onMount(async () => {
    try {
    const res = await fetch('/start_game', {  // No need for full URL
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
});

async function getHint() {
  const res = await fetch('/hint', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    },
  });
  const data = await res.json();
    hintMessage = data.hint;
  }

async function submitGuess() {
  const res = await fetch('/guess', {  // No need for full URL
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ guess, target_word: targetWord }),
  });

    const data = await res.json();
    similarity = data.similarity;
    message = similarity > 0.5 ? "Try Again!" : "Good Guess!";
  }
</script>
  
<main>
  <h1>Contexto Game</h1>
  <p class="hint">Try to guess the target word!</p>


  <input type="text" bind:value={guess} placeholder="Enter your guess" />
  <button on:click={submitGuess}>Submit Guess</button>
  {#if message}
  <p>{message}</p>
  {/if}

  <button on:click={getHint}>Get a Hint</button>
  {#if hintMessage}
    <p><strong>Hint:</strong> {hintMessage}</p>
  {/if}
  
  <p>Similarity Score: {similarity}</p>
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
</style>
