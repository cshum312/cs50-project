# FlightBase
#### Video Demo:  [Introductory Video] (link here)

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
