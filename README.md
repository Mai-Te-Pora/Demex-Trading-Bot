# Demex-Trading-Bot

Welcome to the Demex Exchange Trading Bot!

The bot is designed to trade with concurrent access to strategies and websocket data. Because the bot is still in development, there may be missing storage files for trading pairs and candlesticks.  It can still be run from terminal with minimal changes to code.

Required: Python 3.8 + <br>
Required: Tradehub (Install via pip tradehub)<br>
Note: Tradehub will require Visual Studio Build Tools<br>
Recommended: Miniconda3<br>

Strategies Section:
The strategies section is developed with the intent to add more strategies for users of the exchange.  Currently in development, market making bot, Gann predictive intraday strategy and more predictive algorithms based on further building of pair candlestick storage files.

Setup Authenticated Client:<br>
Go to authenticated_client\demex_auth.py<br>
Alter mnemonic phrase<br>
You will also need to alter on_connect function in main.py. If you'd like to set the websocket to acquire address balances and orders, please apply your SWTH address to the subscription lines for balances and orders.<br>

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
