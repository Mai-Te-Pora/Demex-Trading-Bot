# Demex-Batter-Bot

Welcome to the Demex Exchange Batter Bot!

The bot is designed to trade with concurrent access to strategies and websocket data. Because the bot is still in development, there may be missing storage files for trading pairs and candlesticks.  It can still be run from terminal with minimal changes to code.

Required: Python 3.8 +

Required: Tradehub (Install via pip tradehub)

Strategies Section:
The strategies section is developed with the intent to add more strategies for users of the exchange.  Currently in development, market making bot, Gann predictive intraday strategy and more predictive algorithms based on further building of pair candlestick storage files.

Treway Bot:
A simple triangular (similar to delta neural) bot that will attempt to locate an imbalance between ETH-SWTH, ETH-USDC and SWTH-USDC. The bot will monitor the websocket feed for  an imbalance between the trading pairs. If an imbalance exists in favor of more SWTH, the bot will place three trades. Please feel free to review code. 

Note about the bot: It does not currently monitor fees.

Setup Treway Strategy Bot: Alter the self.usdc_max_quantity to your choice of usdc amount (Trades will be placed based upon this max amount). Alter self.swth_min_quantity_extra to amount of imbalance SWTH to execute trades

Setup Authenticated Client:

Go to authenticated_client\demex_auth.py

Alter mnemonic phrase

Running Main File:

Treway strategy is already setup to run from the main file as a separate asyncio function. Each bot can be created as a separate function, added to the main function as an asyncio task and gathered for concurrency.
