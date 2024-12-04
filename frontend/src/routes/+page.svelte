<script>
  import { onMount } from 'svelte';
  
  let targetWord = '';
  let definition = '';
  let synonyms = [];
  let guess = '';
  let similarity = 0;
  let message = '';
  
  // Fetch the game details when the component mounts
  onMount(async () => {
    try {
      const res = await fetch('http://localhost:5000/start_game', {
        method: 'GET', 
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',  // Specify expected response type
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

  // Submit the user's guess to the backend
  async function submitGuess() {
    const res = await fetch('http://localhost:5000/guess', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ guess, target_word: targetWord }),
    });

    const data = await res.json();
    similarity = data.similarity;
    message = similarity > 0.5 ? "Good guess!" : "Try again!";
  }
</script>
  
<main>
  <h1>Contexto Game</h1>
  <p>Try to guess the target word!</p>
  <p>Hint: The target word has {targetWord.length} letters.</p>

  {#if definition}
    <p><strong>Definition:</strong> {definition}</p>
  {/if}

  {#if synonyms.length > 0}
    <p><strong>Synonyms (hidden for now):</strong> {synonyms.length} synonyms available.</p>
  {/if}

  <input type="text" bind:value={guess} placeholder="Enter your guess" />
  <button on:click={submitGuess}>Submit Guess</button>

  <p>{message}</p>
  <p>Similarity Score: {similarity}</p>
</main>

<style>
  main {
    text-align: center;
    margin-top: 50px;
  }

  input {
    padding: 10px;
    font-size: 16px;
  }

  button {
    padding: 10px;
    font-size: 16px;
    cursor: pointer;
  }
</style>
