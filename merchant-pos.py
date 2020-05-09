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

orderID = 1
address = "Brunswick"
parameters = {"orderID" : orderID, "address": address}


message = adapter.create_Message_(from_, "Labeler", parameters)
adapter.send(message, c)


conn.commit()
conn.close()


@app.route('/messaging/Packed', methods=['POST'])
def receivePacked():
	def do_smth_with_msg():
		return "Message received"
