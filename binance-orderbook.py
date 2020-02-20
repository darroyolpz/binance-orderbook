from binance.client import Client
from datetime import datetime
import pandas as pd

# Create the Binance client, no need for api key
client = Client("", "")

# Get the data
coin = 'BTC'
tickers = client.get_order_book(symbol=coin + 'USDT', limit=1000)

# Create dataframe
df = pd.DataFrame(tickers)

# Remove the ID
df.drop('lastUpdateId', axis=1, inplace=True)

# Function for limit positions
def limit_positions(field):
	# Set the field
	df_field = df[field]

	# Get the price
	df_field = df_field.apply(lambda x: pd.Series(str(x).split(',')))
	df_field_price = df_field[0].apply(lambda x:float(x[2:12]))

	# Get the amount
	df_field_qty = df_field[1]
	df_field_qty = df_field_qty.apply(lambda x:float(x[2:12]))

	return df_field_price, df_field_qty

# Bids dataframe
price, qty = limit_positions('bids')
df_bids = pd.DataFrame(columns=['Price', 'Amount'])
df_bids['Price'] = price
df_bids['Amount'] = qty
df_bids['Time'] = datetime.now()

# Asks dataframe
price, qty = limit_positions('asks')
df_asks = pd.DataFrame(columns=['Price', 'Amount'])
df_asks['Price'] = price
df_asks['Amount'] = qty
df_asks['Time'] = datetime.now()

print(df_bids)
