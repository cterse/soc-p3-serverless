import os
conn = sqlite3.connect('/home/daria/Documents/test/test')
app = Flask(__name__)
from_ = "Merchant"
handlers = {}


def nop(message):
    pass


def handle_message(message):
    handler = handlers.get(message.message, nop)
    handler(message)


def handle_available(message_name):
    def store_handler(handler):  # handleRequestLabel is here <---
        handlers[message_name] = handler
    return store_handler


@handle_available("RequestLabel")
# pass smth like a cursor, construct enactment object if asked. doesnt have to query until asked
def handleRequestLabel(message):
    # < <--- dictionary of parameters
    print("Message: " + str(message.parameters))


@handle_available("RequestWrapping")
# pass smth like a cursor, construct enactment object if asked. doesnt have to query until asked
def handleRequestWrapping(message):
    print("Message: " + str(message["parameters"]))


@handle_available("Packed")
# pass smth like a cursor, construct enactment object if asked. doesnt have to query until asked
def handlePacked(message):
    print("Message: " + str(message["parameters"]))


def enable_adapter():
    global c
    c = conn.cursor()
    adapter.enable_adapter(c, "Merchant", "merchant_pos")


def sendRequestLabel(orderID, address):
    parameters = {"orderID": str(orderID), "address": str(address)}
    message = adapter.create_Message_(
        "Merchant", "Labeler", "RequestLabel", parameters)
    adapter.send(message, c)


def sendRequestWrapping(orderID, itemID, item):
    parameters = {"orderID": str(orderID), "itemID": str(
        itemID), "item": str(item)}
    message = adapter.create_Message_(
        "Merchant", "Wrapper", "RequestWrapping", parameters)
    adapter.send(message, c)


# Operationalize protocol. Configure_adapter() sounds better. and protocol path as a parameter.
enable_adapter()
sendRequestLabel("1", "Brunswick")

#adapter.handle_message({"from": "Merchant", "to": "Labeler", "message": "RequestLabel", "parameters": parameters})
print(handlers)


#sendRequestWrapping("1", "1","Laptop", c)
# pass the message instance to set available
# Available(message):
# diff available method for each msg
# methods are empty but programmer will fill them in. The logic would go in there. specialising methods in the classes
# available functions are empty but programmer can specialise it. decorators, higher order functions - takes a func as a param. but decorators betterself.#its a func you pass a func defself.

@app.route('/messaging/Packed', methods=['POST'])
def receivePacked():
    print(request.json)

    # @handlemsg. param - name of msg.  returns a func that takes a func as its paramself.
    # nested func definitions.
