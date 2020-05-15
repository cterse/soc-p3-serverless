
#####CONFIGURATIONS#####
history_db = '/home/daria/Documents/test/test'
orders_db = '/home/daria/Documents/test/test3'
from_ = "Merchant"
protocol_path="protocol.txt"
configuration_path="configuration.txt"
import pos

########################
import random
import sqlite3
import sched, time

########################



adapter = pos.Adapter(from_, protocol_path, configuration_path, history_db)

connection=sqlite3.connect(orders_db)
cursor=connection.cursor()

last_id = -1
s = sched.scheduler(time.time, time.sleep)
def fetch_orders(sc):
    #print("Doing stuff...")
    # do your stuff
    global last_id
    query = "SELECT * FROM orders WHERE orderID>?"

    for row in cursor.execute(query, (str(last_id),)):

        orderID,address,items = row
        parameters = {
            "orderID": orderID,
            "address": address
        }

        adapter.send("RequestLabel", parameters)


        for itemID,item in enumerate(items.split(",")):
            parameters = {
                "orderID": orderID,
                "itemID": itemID,
                "item": item
            }
            adapter.send("RequestWrapping", parameters)

        last_id=orderID



    s.enter(1, 1, fetch_orders, (sc,))

s.enter(1, 1, fetch_orders, (s,))
s.run()


parameters = {
"orderID": 1,
"address": "Brunswick"
}
#adapter.send("RequestLabel", parameters)



@adapter.register_handler("RequestLabel")
def handleRequestLabel(message): #pass smth like a cursor, construct enactment object if asked. doesnt have to query until asked
	print("RequestLabel sent: " + str(message.parameters)) #< <--- dictionary of parameters

@adapter.register_handler("RequestWrapping")
def handleRequestWrapping(message): #pass smth like a cursor, construct enactment object if asked. doesnt have to query until asked
	print("RequestWrapping sent: " + str(message.parameters)) #< <--- dictionary of parameters

@adapter.register_handler("Packed")
def handlePacked(message): #pass smth like a cursor, construct enactment object if asked. doesnt have to query until asked
	print("An item has been successfully packed: " + str(message.parameters)) #< <--- dictionary of parameters


if __name__ == '__main__':
    adapter.run()
