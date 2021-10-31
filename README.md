# Demex-Trading-Bot

Welcome to the Demex Exchange Trading Bot!

The bot is designed to trade with asychronous access to strategies and websocket data. Because the bot is still in development, there may be missing storage files for trading pairs and candlesticks.  It can still be run from terminal with minimal changes to code.

## Install Tradehub (Carbon)
Required: Python 3.8 + <br>
Use Package Manager pip to install tradehub
```
pip install tradehub
```
Please see WindowsAndLinuxInstall document for more details.

## Setup Authenticated Client
-Go to authenticated_client\demex_auth.py
-Alter mnemonic phrase<br>
You will also need to alter on_connect function in main.py. If you'd like to set the websocket to acquire address balances and orders, please apply your SWTH address to the subscription lines for balances and orders.<br>

## Strategies Section:
The strategies section is developed with the intent to add more strategies for users of the exchange.  Currently in development, market making bot, Gann predictive intraday strategy and more predictive algorithms based on further building of pair candlestick storage files.<br>

### Treway
Treway is a trianglular bot designed to locate an imbalance between pairs traded on Carbon. Because Carbon lists different trading pairs (Ex: WBTC/USDC, ETH/USDC, WBTC/ETH), Treway can search three trading pairs for an imbalance. If located, it will perform the according trades. The bot is not set to run on download. New upload for a fresh verision is imminent with better instructions for implementation and depth analytics.

### Grid
Grid is available to run upon immediate download (provided mnemonic has been altered). It will take four user inputs:
- Pair
- Buy or Sell
- Buy/Sell Price
- Buy/Sell Price
The bot will continue repeating the trades until cancelled. There are expected enhancements to the bot coming in the future.

##Enhancements
c1im4cu5 is working with a couple others to add strategies to the main bot. These include:
- UI based in Flash
- Cascade order creation for Grid
- Session timing for Grid

You are invited to partake. Please feel free to join the Mai-Te-Pora Telegram community!

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to added/altered.
