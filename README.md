<h1> COP3530 - Project 3 </h1>
<p> How to run our project on your computer. </p>

<h2> Steps </h2>

<ol>
  <li>
    <strong>Make sure you have Python installed on your computer.</strong>
  </li>

  <li>
    <strong>Create a virtual environment to install all of our installations by running these commands on your CLI after cloning the repository:</strong>
    <ul>
      <li><strong>(bash)</strong> -- run this command:</li>
      <pre><code>python -m venv venv</code></pre>
      <li><strong>(Windows)</strong> -- run this command:</li>
      <pre><code>venv\Scripts\activate</code></pre>
      <li><strong>(Mac)</strong> -- run this command:</li>
      <pre><code>source venv/bin/activate</code></pre>
    </ul>
  </li>

  <li>
    <strong>Now that you're in the virtual environment, install all required dependencies by running:</strong>
    <pre><code>pip install -r requirements.txt</code></pre>
  </li>

  <li>
    <strong>Next, install the front-end dependencies:</strong>
    <pre><code>npm install</code></pre>
  </li>

  <li>
    <strong>Great! Now you can start the backend server:</strong>
    <ul>
      <li><pre><code>python backend/main.py</code></pre></li>
      <li>Or alternatively, if you're using Python 3:</li>
      <li><pre><code>python3 backend/main.py</code></pre></li>
    </ul>
  </li>

  <li>
    <strong>Now that the backend is running, it's time to start the frontend server:</strong>
    <pre><code>npm run dev -- --open</code></pre>
  </li>

  <li>
    <strong>Once the frontend server is running, your browser will open automatically, and you can play our replica game!</strong>
  </li>
</ol>

<h3>Enjoy the game and let us know if you have any issues!</h3>
