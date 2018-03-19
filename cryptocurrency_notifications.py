import requests
import time
from datetime import datetime

BITCOIN_PRICE_THRESHOLD = 8000
CRYPTOCURRENCY_API_URL = 'https://api.coinmarketcap.com/v1/ticker/'
IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/{}/with/key/bNzEdms-P5bjPEH6QlEHzx'

def get_latest_cryptocurrency_price(cryptocurrency_name):
	response = requests.get(CRYPTOCURRENCY_API_URL + cryptocurrency_name)
	response_json = response.json()
	return float(response_json[0]['price_usd'])

def post_ifttt_webhook(event, value1, value2=''):
	data = {'value1': value1, 'value2': value2}   #the payload that will be sent to IFTTT service
	ifttt_event_url = IFTTT_WEBHOOKS_URL.format(event) #insert our event
	requests.post(ifttt_event_url, json=data)  #send HTTP POST request to the webhook URL

def format_cryptocurrency_history(cryptocurrency_history):
	rows = []
	for cryptocurrency_price in cryptocurrency_history:
		date = cryptocurrency_price['date'].strftime('%d.%m.%Y %H:%M')  # Formats the date into a string
		price = cryptocurrency_price['price']
		row = '{}: $<b>{}</b>'.format(date, price)
		rows.append(row)
	return '<br>'.join(rows)

def main():
	cryptocurrency_name = input('Write, please, the name of cryptocurrency --> ')
	cryptocurrency_history = []
	while True:
		price = get_latest_cryptocurrency_price(cryptocurrency_name)
		date = datetime.now()
		cryptocurrency_history.append({'date': date, 'price': price})

		#send emergency notification:
		if price < BITCOIN_PRICE_THRESHOLD:
			post_ifttt_webhook('bitcoin_price_emergency', price)	

		# send a Telegram notification
		#when will be 5 items - update
		if len(cryptocurrency_history) == 5:
			post_ifttt_webhook('cryptocurrency_price_update', format_cryptocurrency_history(cryptocurrency_history), cryptocurrency_name)
			cryptocurrency_history = []  #reset the histor

		time.sleep(5*60)  # Sleep for 5 minutes

if __name__ == '__main__':
	main()




