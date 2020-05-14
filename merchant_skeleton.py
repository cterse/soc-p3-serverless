import requests
import adapter
from flask import Flask, json
import sqlite3
app = Flask(__name__)
handlers = {}
#change name from skeleton
#its part of adapter



#make generic send method - takes message namd and payload (parameters as dictionary)
#  !!!!!!!!!
def sendRequestLabel(orderID, address):
	parameters = {"orderID" : str(orderID), "address": str(address)}
	message = adapter.create_Message_("Merchant", "Labeler", "RequestLabel", parameters)
	#adapter.send(message)
	adapter.insert(message)

def sendRequestWrapping(orderID, itemID, item):
	parameters = {"orderID" : str(orderID), "itemID": str(itemID), "item": str(item)}
	message = adapter.create_Message_("Merchant", "Wrapper", "RequestWrapping", parameters)
	adapter.send(message)


###############################################################################################################################


###############################################################################################################################


#Operationalize protocol. Configure_adapter() sounds better. and protocol path as a parameter.
#sendRequestWrapping("1", "1", "Laptop")

#adapter.handle_message({"from": "Merchant", "to": "Labeler", "message": "RequestLabel", "parameters": parameters})
#sendRequestWrapping("1", "1","Laptop", c)
#pass the message instance to set available
#Available(message):
#diff available method for each msg
#methods are empty but programmer will fill them in. The logic would go in there. specialising methods in the classes
#available functions are empty but programmer can specialise it. decorators, higher order functions - takes a func as a param. but decorators betterself.#its a func you pass a func defself.



###############################################################################################################################


@app.route('/messaging/Packed', methods=['POST'])
def receivePacked():
	print(request.json)

	#@handlemsg. param - name of msg.  returns a func that takes a func as its paramself.
	#nested func definitions.
