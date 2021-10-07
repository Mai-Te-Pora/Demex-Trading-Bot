# Demex-Trading-Bot

Welcome to the Demex Exchange Trading Bot!

The bot is designed to trade with concurrent access to strategies and websocket data. Because the bot is still in development, there may be missing storage files for trading pairs and candlesticks.  It can still be run from terminal with minimal changes to code.

Required: Python 3.8 + <br>
Required: Tradehub (Install via pip tradehub)<br>
Note: Tradehub will require Visual Studio Built Tools<br>
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

Please note that certain strategies may implement more required Python libraries.
