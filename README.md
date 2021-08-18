# Demex-Batter-Bot

Welcome to the Demex Exchange Batter Bot!

The bot is designed to trade with concurrent access to strategies and websocket data. Because the bot is still in development, there may be missing storage files for trading pairs and candlesticks.  It can still be run from terminal with minimal changes to code.

Required: Python 3.8 +

Required: Tradehub (Install via pip tradehub)

Strategies Section:
The strategies section is developed with the intent to add more strategies for users of the exchange.  Currently in development, market making bot, Gann predictive intraday strategy and more predictive algorithms based on further building of pair candlestick storage files.

Setup Authenticated Client:

Go to authenticated_client\demex_auth.py

Alter mnemonic phrase

Running Main File:

Treway strategy is already setup to run from the main file as a separate asyncio function. Each bot can be created as a separate function, added to the main function as an asyncio task and gathered for concurrency.
