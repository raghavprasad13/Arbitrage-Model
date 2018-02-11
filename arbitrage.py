import requests
import json
import re
from bs4 import BeautifulSoup
import queue
from threading import *

def Watch_Buyucoin(junk):

	response_buyucoin = requests.get("https://www.buyucoin.com/api")  ''' retrieving data from the api url '''

	if response_buyucoin.status_code == 200:
		#print("BuyUCoin Success")
		soup_buyucoin = BeautifulSoup(response_buyucoin.text, 'html.parser')

	keep_going = True

	count = 1

	while (keep_going):		# for now i have limited the program to run 10 times

		for link in soup_buyucoin.findAll('a', attrs={'href': re.compile("xrp/$")}):  ''' obtaining specifically XRP data '''
			data = requests.get(link.text)

			json_string = data.content.decode('utf-8').replace("'", "\"")

			buyucoin_data = json.loads(json_string)

		buyucoin_xrp_buy_price =  buyucoin_data['BuyUcoin_data'][0]['xrp_buy_price']
		buyucoin_xrp_sell_price = buyucoin_data['BuyUcoin_data'][0]['xrp_sell_price']

		if count == 10:
			keep_going = False


		print("Buyucoin count: ", count)

		count+=1

		#print('BuyUCoin XRP buy price: ', buyucoin_xrp_buy_price, " BuyUCoin XRP sell price: ", buyucoin_xrp_sell_price)

		#print(type(buyucoin_data))
		#print(buyucoin_data)

		#print("")

	# results = "Buyucoin final count: ".join(str(count-1))

	return {'BuyUCoin_XRP_buy_price': buyucoin_xrp_buy_price, 'BuyUCoin_XRP_sell_price': buyucoin_xrp_sell_price}
	''' the data collected from the buyucoin api '''


def Watch_Koinex(junk):

	# KOINEX_BREAKEVEN_POINT =

	keep_going = True

	count=1

	while (keep_going):

		response_koinex = requests.get("https://koinex.in/api/ticker")		''' retrieving data from the api url '''

		if response_koinex.status_code == 200:
			#print("Koinex Success")
			
			json_string = response_koinex.text.replace("'", "\"")

			koinex_data = json.loads(json_string)

			koinex_xrp_price = koinex_data['prices']['XRP']

			print("Koinex count: ", count)

			#print(koinex_xrp_price)

			#print(type(koinex_data))
			#print(koinex_data)

			#print("")

		elif response_koinex.status_code == 403:
			print("Error 403: Access denied")
			keep_going = False

		elif response_koinex.status_code == 404:
			print("Error 404: Not found")
			keep_going = False

		if count == 10:
			keep_going = False

		count+=1

	# results = "Koinex final count: ".join(str(count-1))	

	return koinex_xrp_price  ''' data from the koinex api '''




def Watch_Coindelta(junk):

	# COINDELTA_BREAKEVEN_POINT = 

	keep_going = True

	count=1

	while (keep_going):

		response_coindelta = requests.get("https://coindelta.com/api/v1/public/getticker/")  ''' retrieving data from the api url '''

		if response_coindelta.status_code == 200:
			#print("CoinDelta Success")

			json_string = response_coindelta.text.replace("'", "\"")

			coindelta_data = json.loads(json_string)

			coindelta_xrp_price = coindelta_data[9]['Ask']

			print("Coindelta count: ", count)

			#print(coindelta_xrp_price)

			#print(type(coindelta_data))
			#print(coindelta_data)

			#print("")

		elif response_coindelta.status_code == 403:
			print("Error 403: Access denied")
			keep_going = False

		elif response_coindelta.status_code == 404:
			print("Error 404: Not found")
			keep_going = False

		if count == 10:
			keep_going = False

		count+=1

	# results = "Coindelta final count: ".join(str(count-1))

	return coindelta_xrp_price		''' data collected from the coindelta api '''


que = queue.Queue()



thread_buyucoin = Thread(target=lambda q, arg1: q.put(Watch_Buyucoin(arg1)), args=(que, "junk"))
thread_koinex = Thread(target=lambda q, arg1: q.put(Watch_Koinex(arg1)), args=(que, "junk"))
thread_coindelta = Thread(target=lambda q, arg1: q.put(Watch_Coindelta(arg1)), args=(que, "junk"))

''' Three different threads to parallely run the check on all 3 APIs '''

# threads = [thread_buyucoin, thread_koinex, thread_coindelta]


thread_buyucoin.start()
thread_koinex.start()
thread_coindelta.start()

thread_buyucoin.join()
thread_koinex.join()
thread_coindelta.join()

# print(que.qsize())

while not que.empty():

	result = que.get()

	print(result)














