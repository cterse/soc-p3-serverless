
#####CONFIGURATIONS#####
db_path = '/home/daria/Documents/test/test'
from_ = "Merchant"
protocol_path="protocol.txt"
configuration_path="configuration.txt"
import pos
########################
import random

########################
adapter = pos.Adapter(from_, protocol_path, configuration_path, db_path)



#every time an input from terminal comes in then we proceed
#to send a message.

#merchant can have an internal database and if a value is inserted then do that
#from command line insert it in database that represents an order. write smth that monitors a database and whenever there is an order do smth with it


#Sending a RequestLabel message to Labeler

parameters = {
"orderID": 1,
"address": "Brunswick"
}
adapter.send("RequestLabel", parameters)







@adapter.register_handler("RequestLabel")
def handleRequestLabel(message): #pass smth like a cursor, construct enactment object if asked. doesnt have to query until asked
	print("RequestLabel sent: " + str(message.parameters)) #< <--- dictionary of parameters



@adapter.register_handler("RequestWrapping")
def handleRequestWrapping(message): #pass smth like a cursor, construct enactment object if asked. doesnt have to query until asked
	print("RequestWrapping sent: " + str(message.parameters)) #< <--- dictionary of parameters

@adapter.register_handler("Packed")
def handlePacked(message): #pass smth like a cursor, construct enactment object if asked. doesnt have to query until asked
	print("Packed received: " + str(message.parameters)) #< <--- dictionary of parameters


if __name__ == '__main__':
    adapter.run()
