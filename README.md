# Weather Bot

Welcome to the Weather Bot! This bot provides current weather information for cities around the world. Developed by Niels Coert, it utilizes the OpenWeather API to deliver real-time weather updates directly to your Discord messages.

## Features

### 1. Get Current Weather
- **Command:** `/weather <city>`
- **Description:** Fetches the current weather for the specified city.
- **Example:** `/weather London`
- **Response:** The bot will reply with:
  - Temperature (in °C)
  - Humidity (in %)
  - Weather description (with an emoji)
  - Weather icon

### 2. Error Handling
- The bot provides informative error messages for:
  - Invalid commands
  - Missing city names
  - Unsuccessful weather data retrieval

### 3. Weather Emojis
- The bot adds relevant emojis based on the weather description:
  - ☀️ Clear
  - ☁️ Cloudy
  - 🌧️ Rainy
  - ❄️ Snowy
  - ⛈️ Stormy
  - 🌫️ Foggy
  - 🌈 Default for other weather

### 5. Information Command
- **Command:** `/info`
- **Description:** Displays information about how to interact with the bot and its features.
- **Response:** An embedded message detailing the command usage and credits.

## Getting Started

1. Invite the bot to your Discord server.
2. Use the `/weather <city>` command to get started with weather updates.
3. Type `/info` for more information about the bot's features.

## Credits
- Developed by **Niels Coert**
- Weather data provided by **OpenWeather**
- Hosted on Discord by **niels__69**
