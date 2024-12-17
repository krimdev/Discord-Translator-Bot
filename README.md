# Discord Translator Bot 🌐

A Discord bot that translates messages with a user-friendly interface. Users can select their preferred language with flag emojis and translate messages using context menu commands.

## Features ✨

- 🔠 Support for 10 major languages with flag emojis
- 📜 Context menu translation (right-click on messages)
- 🎯 Personal language preferences for each user
- 🔒 Private translations (only visible to the requesting user)
- 🎨 Clean embeds for translated messages

## Supported Languages 🗣️

- 🇺🇸 English
- 🇫🇷 French
- 🇪🇸 Spanish
- 🇩🇪 German
- 🇮🇹 Italian
- 🇵🇹 Portuguese
- 🇷🇺 Russian
- 🇯🇵 Japanese
- 🇰🇷 Korean
- 🇨🇳 Chinese
- 🇮🇳 Hindi

## Installation 🚀

1. Clone the repository:
```bash
git clone https://github.com/yourusername/discord-translator-bot.git
cd discord-translator-bot
```

2. Install the required packages:
```bash
pip install discord.py googletrans==4.0.0-rc1
```

3. Create a Discord application and bot:
- Go to [Discord Developer Portal](https://discord.com/developers/applications)
- Create a new application
- Go to the "Bot" section and create a bot
- Copy the bot token

4. Configure the bot:
- Open the `bot.py` file
- Replace `'YOUR_TOKEN_HERE'` with your bot token

5. Set up bot permissions:
- In the Discord Developer Portal, go to OAuth2 > URL Generator
- Select the following scopes:
  - `bot`
  - `applications.commands`
- Select the following bot permissions:
  - Read Messages/View Channels
  - Send Messages
  - Read Message History
  - Add Reactions

6. Run the bot:
```bash
python bot.py
```

## Usage 📝

1. Set your preferred language:
   - Type `/language` in any channel
   - Select your language from the dropdown menu with flags

2. Translate messages:
   - Right-click on any message
   - Go to Apps > Translate Message
   - The translation will appear only visible to you

## Commands 🔧

- `/language` - Open the language selection menu
- Right-click menu > Apps > Translate Message - Translate a specific message

## Requirements 📋

- Python 3.8 or higher
- discord.py
- googletrans 4.0.0-rc1

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits 👏

Created by KrimDev

---

For support or questions, please open an issue on GitHub.
