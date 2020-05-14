
#####CONFIGURATIONS#####
db_path = '/home/daria/Documents/test/test'
from_ = "Merchant"
protocol_path="protocol.txt"
configuration_path="configuration.txt"

########################
import merchant_skeleton as messaging
import pos
from flask import Flask, json, request

########################
app = Flask(__name__)
adapter= pos.Adapter(from_, protocol_path, configuration_path, db_path)




parameters = {
"orderID":"1",
"address": "Brusnwick"
}
#....YOUR CODE GOES HERE:

adapter.send("RequestLabel", parameters)

parameters = {
"orderID":"2",
"address": "Brusnwickasdasd"
}

adapter.send("RequestLabel", parameters)



#interface for programmer
@adapter.register_handler("RequestLabel")
def handleRequestLabel(message): #pass smth like a cursor, construct enactment object if asked. doesnt have to query until asked
	print("MESSAGE IS BEING HANDLED: " + str(message.parameters)) #< <--- dictionary of parameters

@adapter.register_handler("RequestWrapping")
def handleRequestWrapping(message): #pass smth like a cursor, construct enactment object if asked. doesnt have to query until asked
	print("Message: " + str(message.parameters)) #< <--- dictionary of parameters

@adapter.register_handler("Packed")
def handlePacked(message): #pass smth like a cursor, construct enactment object if asked. doesnt have to query until asked
	print("Message: " + str(message.parameters)) #< <--- dictionary of parameters
