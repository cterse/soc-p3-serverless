#####CONFIGURATIONS#####
db_path = '/home/daria/Documents/test/test2'
from_ = "Labeler"
protocol_path="protocol.txt"
configuration_path="configuration.txt"

########################
import merchant_skeleton as messaging
import pos
from flask import Flask, json, request

########################
app = Flask(__name__)
adapter= pos.Adapter(from_, protocol_path, configuration_path, db_path)



@adapter.register_handler("RequestLabel")
def handleRequestLabel(message): #pass smth like a cursor, construct enactment object if asked. doesnt have to query until asked
	print("MESSAGE IS BEING HANDLED: " + str(message.parameters))


###############################################################################################################################

#our concepts
#generic reception method.
#create a func register_reception. flask has to notify adapter - generic. adapter has to figure out what kind of message it is and notify handleRequestLabel
@app.route('/messaging/RequestLabel', methods=['POST'])
def receiveRequestLabel():
	received = adapter.receive("RequestLabel", json.loads(request.json))
	if received:
		return '', 204
	else:
		return 'error'

#1 specify protocol provide programming model - adapter component, handlers
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
