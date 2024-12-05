<H1> COP3530 - Project 3 </h1>
How to run our project on your computer. 
<h2> Steps </h2>
1. Make sure you have Python installed on your computer. 
2. Create a virtual enviroment to install all of our installations by...(running these commands on your CLI after cloning repository)
	a. (bash) -- run this --> python -m venv venv
 	b. (windows) -- run this --> venv\Scripts\activate
  	c. (mac) -- run this --> source venv/bin/activate
3. Now that you're in the virtual enviroment, install all requirements by...
	a. pip install -r requirements.txt
4. Next install front end dependencies
	a. npm install
5. Great! Now you can start the backend server
	a. python backend/main.py
 	b. (or) --> pyhton3 backend/main.py
6. Now that backend is running, time to run the frontend server
	a. npm run dev -- --open
7. Now the local host should open up a tab on your computer, and there you can play our replica game!


