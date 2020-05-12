import requests
import adapter
from flask import Flask, json, request
import sqlite3
conn = sqlite3.connect('/home/daria/Documents/test/test')

app = Flask(__name__)
role = "Labeler"
from_ = "Labeler"

#c = conn.cursor()
#adapter.enable_adapter(c, "Labeler")

@app.route('/labeled', methods=['POST'])
def add_item():
    if not request.json or not 'oID' in request.json:
        abort(400)
    oID = request.json['oID']
    print(oID)




@app.route('/messaging/RequestLabel', methods=['POST'])
def receiveRequestLabel():
	#print(request.json)
    #return True
    #insert message here
    print(request.json)

    msg = {
        'orderID':  request.json['orderID'],
        'address': request.json.get('address', "")
    }

    #This is reception from network - http
    #verify msg is correct and insert it in the database
    #once its there - let agent know that a new event has happened. "Available" - notify
    #generate handler.
    #if available then agent can use rule-engine to do processing. event-action rules - if/then. easy way to encode policies.
    #Rule could be that if address is x then send labeled msg. can write any rules in the engineself.
    #stellar whenevr msg is sent or received - notify agent(sender or receiver).
    #have to let db notify that a msg is available (a specific msg).#Terminology - receive for networking and available for history
    #dont do rule engine yet but focus on notfying agent of available messages (sent or received).
    #

    #adapter.create_Message_(from_, to_, message_name, parameters)
    #adapter.insert(..)

    #This function will handle insertion
    #adapter.process_received()
    #    if it fails then not Available
    #    else available
    #message = Message_(from_, to_, message_name, parameters)
    #return '',204

    #let agent know that a message has been sent as wellself.
    #when message is sent -> available
