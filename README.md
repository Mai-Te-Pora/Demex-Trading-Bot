# Demex-Trading-Bot

Welcome to the Demex Exchange Trading Bot!

The bot is designed to trade with concurrent access to strategies and websocket data. Because the bot is still in development, there may be missing storage files for trading pairs and candlesticks.  It can still be run from terminal with minimal changes to code.

## Installation
Required: Python 3.8 + <br>
Use Package Manager pip to install tradehub
'''bash
pip install tradehub
'''
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
- Grid is available to run upon immediate download (provided mnemonic has been altered). It will take four user inputs:
- Pair
- Buy or Sell
- Buy/Sell Price
- Buy/Sell Price

##Enhancements


Running Main File in Parent Folder:<br>
python main.py (or python3 depending on miniconda3 downlaod)<br>

Treway strategy is already setup (Please check math) to run from the main file as a separate asyncio function. Each bot can be created as a separate function, added to the main function as an asyncio task and gathered for concurrency.<br>
Note about Treway: It is currently disabled in code.<br>

The Grid Bot/ MM strategy is set to run upon immediate download. A user will only need to change the mnemonic (as stated above) to begin trading!<br>
Notes about Grid Strategy: <br>
Pairs MUST be typed exactly! Users are given a list for reference.<br>
Order quantities should always possess the ones digit (0.01)<br>
The bot will continue replicating the designated orders until stopped <br>
If a connection to the websocket is lost, the bot will attempt to cancel all active user orders placed with the bot<br>

Please note that certain strategies may implement more required Python libraries.
