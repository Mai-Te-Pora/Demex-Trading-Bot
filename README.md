# Demex-Trading-Bot

Welcome to the Demex Exchange Trading Bot!

The bot is designed to trade with asychronous access to strategies and websocket data. Because the bot is still in development, there may be missing storage files for trading pairs and candlesticks.  It can still be run from terminal with minimal changes to code.

## Install Bot Instructions for Linux
Required: Python 3.8 + <br>
Use Package Manager pip to install tradehub
```
sudo apt-get update 
sudo apt-get install python3.8
sudo apt-get install python3-pip
sudo apt-get install python3.8-dev
pip install tradehub
```

If you're having any troubles setting up Python (or already possess a prior python version, please go to the following link for assistance in installing a new version)
https://tech.serhatteker.com/post/2019-12/upgrade-python38-on-ubuntu/


- Download github repository
ONLY DOWNLOAD FROM TRUSTED SITE - https://github.com/Mai-Te-Pora
```
git clone https://github.com/Mai-Te-Pora/Demex-Trading-Bot
```

- Navigate to Demex-Bot dir
```
cd Demex-Trading-Bot
```

- Navigate to authenticated client folder to alter mnemonic
```
cd authenticated_client
```

- Open python file to alter mnemonic (Note performing this line of code will open a text editor in the terminal window. You will need to change the section of the document that looks like this:
 - mnemonic='ENTER YOUR MNEMONIC HERE FOR CONNECTION TO TRADEHUB'
 - You will want to enter your mnemonic with spaces between the parenthesis
 - After alterations, please make sure to save it!<br>
```
nano demex_auth.py
```

- Move back to main dir
```
cd
```
- Navigate back to Demex-Dir
```
cd Demex-Trading-Bot
```

- Run Bot
```
python3 main.py
```

## Strategies Section:
The strategies section is developed with the intent to add more strategies for users of the exchange.<br>

### Treway
Treway is a trianglular bot designed to locate an imbalance between pairs traded on Carbon. Because Carbon lists different trading pairs (Ex: WBTC/USDC, ETH/USDC, WBTC/ETH), Treway can search three trading pairs for an imbalance. If located, it will perform the according trades. The bot is not set to run on download. New upload for a fresh verision is imminent with better instructions for implementation and depth analytics.

### Grid
Grid is available to run upon immediate download (provided mnemonic has been altered). It will take four user inputs:
- Pair
- Buy or Sell
- Buy/Sell Price
- Buy/Sell Price

The bot will continue repeating the trades until cancelled. There are expected enhancements to the bot coming in the future.

## Enhancements
c1im4cu5 is working with a couple others to add strategies to the main bot. These include:
- UI based in Flash
- Cascade order creation for Grid
- Session timing for Grid
- Base or Quote profit taking
- Binance Arbritrage Bot (Coco's bot will be moved. He has agreed to test! Thank you, Coco!)
- Coinbase Arbritrage Bot (once Atom had been added to the exchange)

You are invited to partake. Please feel free to join the Mai-Te-Pora Telegram community!

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to added/altered.
