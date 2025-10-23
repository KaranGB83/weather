# Weather App
#### Video Demo:  https://youtu.be/dSQembwqbOM
#### Description:
Web application That gives us the current weather report of a given city.
Technology Used:
Front-end-> HTML5,CSS3,Javascript  
Back-end->python3,flask
Database->pysqlite3
API->openweathermapapi
# weather.py
This Python file is a command-line tool that retrieves and displays current weather information for a specified city using the OpenWeatherMap API. It performs the following tasks:
Accepts a city name as input via command-line arguments.
Sends a GET request to the OpenWeatherMap API with the city name and API key.
Parses the JSON response to extract key weather details:
-Temperature (in Celsius)
-Humidity percentage
-Weather description (e.g., "clear sky", "light rain")
-Country code
-Sunrise and sunset times (converted to UTC format)
Handles errors gracefully, including:
-Network issues
-Invalid city names
-Missing data in the API response
Returns the weather data as a dictionary for further use or display.

# app.py
Flask web application that allows users to search for real-time weather information by city name. It integrates the OpenWeatherMap API for weather data and uses SQLite3 for user management and persistent search logging.

--Users can enter a city name to retrieve current temperature, humidity, weather description, and sunrise/sunset times.

--Secure login, logout, and registration system using hashed passwords with Werkzeug.

--Logged-in users have their weather searches saved and can view recent queries.

--Tracks logged-in users and restricts access to history and account pages.

--Provides real-time feedback for errors, login status, and form validation.

--Stores user credentials and weather search history in a local database.

# requirements.txt
flask: The main web framework used to build the server, handle routing, render templates, and manage sessions.

requests: Used to make HTTP requests to the OpenWeatherMap API for fetching real-time weather data.

werkzeug: Provides secure password hashing and verification utilities for user authentication.

pysqlite3: Enables interaction with a local SQLite database to store user credentials and weather search history.

# weather.db

The weather.db file is a SQLite database that stores user credentials and weather search history for Flask-based weather application.

sqlite> .schema
CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, hash NOT NULL);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE history (id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER,city TEXT,time DATETIME DEFAULT CURRENT_TIMESTAMP,FOREIGN KEY(user_id) REFERENCES users(id));
# layout.html
This HTML file is the base layout template for Flask weather application. It uses Bootstrap 5 for responsive design and styling, and includes dynamic content blocks and conditional rendering based on user login status.

--Navigation Bar:

Displays app name: Weather App by kgb
Shows different links based on login status:
Logged-in users see an Account link with an icon.
Guests see Login and Register options.

--Flash Messaging:

Displays alerts for login success, errors, or form feedback using Flask’s

--Footer:

Simple footer with a link back to the homepage and a signature label KGB.

# index.html

--HTML template serves as the homepage for a Flask-based weather application. 
--It extends base layout and displays a centered card containing weather search  -- form allows users to input a city name and submit it via POST 
--design uses Bootstrap classes for responsive alignment and styling,including     location icon from Bootstrap Icons.
--input field is required and optimized for user experience with autofocus and autocomplete disabled. 
The overall layout is clean, mobile-friendly, and visually balanced, making it easy for users to interact with the app and retrieve weather data.

# weather.html

-- HTML template displays the weather results page for a Flask-based application. -- extends a base layout and presents the weather data in a visually appealing, centered card format. 
--city name is highlighted in the header, followed by a list of weather attributes such as description, temperature, humidity, sunrise and sunset times. 
-- item is accompanied by a relevant Bootstrap icon for better visual context.--country code is shown in the footer of the card. 
The layout is responsive and styled using Bootstrap classes, ensuring a clean and user-friendly experience across devices.

# login.html 
--HTML template defines the login page for Flask weather application
--It extends the base layout and sets the page title to "LOG IN".
 -- body contains a vertically and horizontally centered login form styled with Bootstrap. 
 --form includes input fields for the username and password, both styled for a clean and compact appearance. 
 --username field is set to autofocus and disables autocomplete for better security and user experience. 
 -- LOG IN button is placed below the inputs, centered within a padded container. The overall design is responsive and minimal, ensuring a smooth login experience across devices.

# register.html   
-- HTML template defines the registration page for Flask weather application. -- extends the base layout and sets the page title to "REGISTER". 
--body contains a centered registration form styled with Bootstrap, featuring input fields for username, password, and password confirmation
--Each field is designed for clarity and ease of use, with autofocus enabled on the username and autocomplete disabled for security. 
-- form submits a POST request to the /register route. 
# history.html

--HTML template renders the search history page for Flask weather application. 
-- extends the base layout and sets the page title to "HISTORY". 
-- body contains a Bootstrap-styled table that displays a logged-in user's past weather searches
--Each row shows the city name and the corresponding timestamp, retrieved from the history variable passed by the backend
--The table uses a dark theme with striped rows for readability, and the layout is wrapped in a responsive container with top margin for spacing.
# account.html

--HTML template defines the account page for Flask weather application
--It extends the base layout and sets the page title to "Account"
--The page displays the logged-in user's username and a table of their ten most recent weather searches, including the city name and timestamp
--If no recent searches are available, a message is shown instead
--The layout includes links to view the full search history and log out, all styled with Bootstrap for a clean and responsive user experience

# modules
Flask : render_template, Flask, request, flash, session, and redirect for routing, form handling, session management, and user feedback.

SQLite3: Enables interaction with a local SQLite database to store user credentials and weather search history.

Werkzeug security: Provides secure password hashing and verification for user authentication.

weather module: get_weather is a user-defined function that fetches weather data from the OpenWeatherMap API.

Functools: wraps is used to create decorators like @login_required for protecting routes.

Requests: Allows HTTP requests to external APIs (used in get_weather).

Datetime : datetime and timezone are used to format sunrise and sunset times from UNIX timestamps into readable UTC format.



