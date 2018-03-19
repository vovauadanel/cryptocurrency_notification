import requests
import time
from datetime import datetime

BITCOIN_PRICE_THRESHOLD = 8000
BITCOIN_API_URL = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/'
IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/{}/with/key/bNzEdms-P5bjPEH6QlEHzx'

def get_latest_bitcoin_price(): 
	response = requests.get(BITCOIN_API_URL)
	response_json = response.json()
	return float(response_json[0]['price_usd'])  # convert the price to a floating point number

def post_ifttt_webhook(event, value):
	data = {'value1': value}  #the payload that will be sent to IFTTT service
	ifttt_event_url = IFTTT_WEBHOOKS_URL.format(event)	#insert our event
	requests.post(ifttt_event_url, json=data)  #send HTTP POST request to the webhook URL

def format_bitcoin_history(bitcoin_history):
	rows = []
	for bitcoin_price in bitcoin_history:
		date = bitcoin_price['date'].strftime('%d.%m.%Y %H:%M')  # Formats the date into a string
		price = bitcoin_price['price']
		row = '{}: $<b>{}</b>'.format(date, price)
		rows.append(row)

	return '<br>'.join(rows)

def main():
	bitcoin_history = []
	while True:
		price = get_latest_bitcoin_price()
		date = datetime.now()
		bitcoin_history.append({'date': date, 'price': price})

		#send emergency notification:
		if price < BITCOIN_PRICE_THRESHOLD:
			post_ifttt_webhook('bitcoin_price_emergency', price)
		
		# send a Telegram notification
		#when will be 5 items - update
		if len(bitcoin_history) == 5:
			post_ifttt_webhook('bitcoin_price_update', format_bitcoin_history(bitcoin_history))
			bitcoin_history = []   #reset the history

		time.sleep(5*60)  # Sleep for 5 minutes

if __name__ == '__main__':
	main()