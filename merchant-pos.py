#https://code.tutsplus.com/tutorials/how-to-write-package-and-distribute-a-library-in-python--cms-28693
import requests
import adapter
from flask import Flask, json
import sqlite3
conn = sqlite3.connect('/home/daria/Documents/test/test')

app = Flask(__name__)
role = "Merchant"
from_ = "Merchant"

c = conn.cursor()
adapter.enable_adapter(c)

orderID = 6
address = "Brunswiasdck"
parameters = {"orderID" : orderID, "address": address}
message = adapter.create_Message_(from_, "Labeler", parameters)
adapter.insert(message, c)
#adapter.send(message, c)
orderID = 7
address = "Brunswiasdck"
parameters = {"orderID" : orderID, "address": address}
message = adapter.create_Message_(from_, "Labeler", parameters)
adapter.insert(message, c)
adapter.insert(message, c)
orderID = ''
address = "Brunswiasdck"
parameters = {"orderID" : orderID, "address": address}
message = adapter.create_Message_(from_, "Labeler", parameters)
#adapter.insert(message, c)

orderID = '8'
address = ''
parameters = {"orderID" : orderID, "address": address}
message = adapter.create_Message_(from_, "Labeler", parameters)
#adapter.insert(message, c)

orderID = ''
address = ''
parameters = {"orderID" : orderID, "address": address}
message = adapter.create_Message_(from_, "Labeler", parameters)
#adapter.insert(message, c)

orderID = '10'
address = 'qwe'
packed = 'sdf'
parameters = {"orderID" : orderID, "address": address, "packed": packed}
message = adapter.create_Message_(from_, "Labeler", parameters)
#adapter.insert(message, c)

orderID = '6'
address = 'sdsfhsdfshs'

parameters = {"orderID" : orderID, "address": address}
message = adapter.create_Message_(from_, "Labeler", parameters)
adapter.insert(message, c)


conn.commit()
conn.close()


@app.route('/messaging/Packed', methods=['POST'])
def receivePacked():
	def do_smth_with_msg():
		return "Message received"
