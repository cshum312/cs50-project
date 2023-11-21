# FlightBase
#### Video Demo:  [Introductory Video](https://youtu.be/-UNtKmqMSNQ)

#### Quick Start: [App Link](https://flightbase.onrender.com/)

#### Description:
Hello :smile:!

This project is a simple web-app that allows registered users to track up to 5 flights, including the current details of the flight, origin airport, destination airport, as well as the weather at both locations. It provides users with the weather at both the origin and destination. All information is provided in one simple page for ease of use.

It integrates [AirLabs Data API](https://airlabs.co/) and [OpenWeather API](https://openweathermap.org/) to obtain data. 

The project uses Python for the backend, with [Flask](https://flask.palletsprojects.com/). User data is stored in [sqlite3](https://www.sqlite.org/). The frontend, assisted by [Bootstrap 5.2.3](https://getbootstrap.com/), uses HTML and CSS. 

Flag emojis are courtesy of [FlagCDN](https://flagcdn.com/) and the background video is from [Vecteezy](https://vecteezy.com/). Other miscellaneous icons are from [OnlineWebFonts](https://www.onlinewebfonts.com/icon).


#### API Instructions:
Upon cloning the repository, create a file '.env' to store your AirLabs API key and OpenWeather API key as follows:
```
AIRLABS_DATA_API_KEY = {API KEY}
OPENWEATHER_API_KEY = {API KEY}
```

#### Required packages:
dotenv:
```
pip uninstall python-dotenv
```

Werkzeug:
```
pip install Werkzeug
```

Flask and Flask_Session:
```
pip install Flask
pip install Flask-Session
```

requests:
```
pip install requests
```

#### Usage Instructions:
Users may register an account and log in. Upon logging in, users may search for a flight number (IATA) and click 'follow'.
This will add the flight to the user's list and provide updated flight status and current weather conditions whenever the page refreshes.
Upon adding a flight to the follow list, users may check current weather conditions at either origin or destination by clicking 'Check Weather'.

To unfollow a flight, users may click the red 'unfollow' button. This will remove the flight from the follow list.
Users may add up to 5 flights to follow.
Flights will be automatically removed from the follow list when the flight number becomes invalid.

#### Structure of the Project:
flightbase
 - static
    airplane.png
        This file stores the .png airplane icon that is used to show the progress of the flight.
    logo.svg
        This file stores the logo icon in .svg format that is used to display next to FlightBase.
    styles.css
        This CSS file contains the customized .css that adds onto the CDN bootstrap files.

 - templates
    error.html
        This html file is for the error message if the user does something that leads to an error on the website.
    index.html
        This html file is the main bulk of the web-app. It includes the search bar to add flights, as well as displays all flight and weather information for users.
    layout.html
        This html file stores the overall layout of the web-app. It is referenced in all other html files.
    login.html
        This html file is for the login page. Users can log into their accounts on this page.
    register.html
        This html file is for the registration page. Users can register for an account on this page.

 app.py
    This .py file contains the main backend and routes for the web-app. It contains functions for all the various search and unfollow actions, as well as the login and registering.
 flights.db
    This is the database file, that uses sqlite3. It stores two databases. One being the users table, which includes the user login information. The other is a flights table that lists all the flights that a user follows.
 helpers.py
    This .py file contains additional functions that are referenced from the main app.py file. It mainly has functions that interact with both API to return a dictionary that the front-end will use as content on the web-app.
 requirements.txt
    This file is used for deployment on [Render](https://render.com/).
