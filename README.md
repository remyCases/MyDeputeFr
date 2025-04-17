# MyDeputeFr
[![codecov](https://codecov.io/gh/remyCases/MyDeputeFr/branch/main/graph/badge.svg)](https://codecov.io/gh/remyCases/MyDeputeFr)

**MyDeputeFr** is a Discord bot built with Python that provides users with information about members of parliament in France. The bot helps you quickly fetch details like the names, party affiliations, and other relevant data for any parliament member, directly from your Discord server.

## Features

- **Find Your Representatives**: Locate your French Members of Parliament (MPs) in your constituency (circonscription).
- **Display Member Information**: Get detailed information about French Members of Parliament (MPs).
- **Scrutins Information**: View information about the latest scrutins (voting results).

## Powered By

- **Python**: Core programming language.
- **discord.py**: Python wrapper for the Discord API.

---

## Installation

### Prerequisites

Make sure you have Python 3.8 or higher installed.

### Steps to Install

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/MyDeputeFr.git
   cd MyDeputeFr
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your Discord bot**:
   - Go to the [Discord Developer Portal](https://discord.com/developers/applications) and create a new bot.
   - Copy the bot token and add it to your `.env` file (create it if it doesn't exist).
   
   Example `.env` file:
   ```
   DISCORD_TOKEN=your-bot-token-here
   ```

4. **Run the bot**:
   ```bash
   python main.py
   ```

   Your bot should now be up and running on your Discord server.

---

## Development

### Running Tests

To run the tests follow these steps:

1. **Install test dependencies** (if you haven't already):
   ```bash
   pip install -r requirements-dev.txt
   ```

2. **Run the tests**:
   ```bash
   pytest
   ```

---

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
