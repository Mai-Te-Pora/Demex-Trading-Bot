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
pip install pandas
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
Treway is a trianglular bot designed to locate an imbalance between pairs traded on Carbon. Because Carbon lists different trading pairs (Ex: WBTC/USDC, ETH/USDC, WBTC/ETH), Treway can search three trading pairs for an imbalance. If located, it will perform the according trades. The bot is not set to run on download. 

Enhancements have been added to include depth analytics. Depth analytics allows the bot to consider the quantity of tokens and price. Here is a quick example:

- Purchase Lot One for 25 @ 0.10 for a total of 2.50 USDC
- Purchase Lot Two for 50 @ 0.11 for a total of 5.50 USDC
- Purchase Lot Three for 100 at 0.12 for a total of 12.00 USDC

There are three available analytics (SWTH, WBTC or ETH) functions. With each movement between the pairs, Treway is calculating the amount of tokens based up two initial inputs. 

- The first input is a total amount of the analytics token. From this input, Treway will calculate the appropriate amount of tokens for each of the secondary tokens.
- The second input is a total amount of overage from the token imbalance check. 
- Notes
- - Users should consider both inputs as the same token; which is appropriately named within the analytics function 
- - Always remember to include the ones digit (0.01)

Treway has been miminally tested. While it performs market orders in succession with correction, c1im4cu5 has not tested performance without possessing all quantities in advance of operation. Treway is designed to trade in succession to acquire more tokens at the end of the session. In theory, a user should only need the starting token for the given function. This has not been tested. Starting quantities for all tokens were always in possession prior to execution.

Taker fees are considered! While it will take these fees into consideration, it will not attempt to make them up. The user is expected to understand this concept prior to execution. The user should make sure to input slightly higher quantities in "Input Two" of the function.

Users should understand the bot will create and execute market orders. If another user of the exchange places an order prior to your order, there is a chance of losing tokens rather than gaining; which is the nature of trading. In order to help mitigate this possibility, the bot does not react to orderbook events. It will check the orderbook at an interval of the users choosing to impartially attempt to locate an imbalance.

### Grid
Grid has been completely rebuilt! Novice and experienced users were considered in the build process. Here are the enhancements:
- Sets order creation (Min = 3, Max = 16)
- Base and quote profit taking
- Linear versus cascade order creation
- Better visual printing experience for user
- Ability to reload data in case of websocket timeout/error (or for more experienced users....uploading their own list of dicts)
- Ability to print current list of potential orders
- Ability to start over

Notes:
If you are choosing auto order creation, please be aware of rounding. Demex offers tokens in different digit depths. Creation of Grid was difficult due to this feature of the exchange. When uploading a new order, Demex will automatically round the price and/or quantity of a token. It may cause slight variations in the total amount calculated for price and quantity.

## Enhancements
c1im4cu5 is working with a couple others to add strategies to the main bot. These include:
- Session timing for Grid
- Binance Arbritrage Bot (Coco's bot will be moved. He has agreed to test! Thank you, Coco!)
- Coinbase Arbritrage Bot (once Atom had been added to the exchange)

You are invited to partake. Please feel free to join the Mai-Te-Pora Telegram community!

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to added/altered.
