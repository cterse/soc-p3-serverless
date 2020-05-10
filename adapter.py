import requests
import adapter
from flask import Flask, json
from collections import OrderedDict
import sqlite3

protocol_path = "protocol.txt"
schema_path = "schema.txt"

def enable_adapter(c):
    #PARSING PROTOCOL
    global protocol
    protocol = open(protocol_path, "r")

    #Skipping unnecessary lines of the protocol
    next(protocol)
    next(protocol)
    next(protocol)

    #Reading messages
    messages = protocol.readlines()
    messages = messages[:-1]
    protocol = []

    #Parsing information about messages line by line
    for message in messages:

        parameters = find_between(message, "[", "]")
        words = message.split()
        from_ = words[0]
        to_ = words[2].replace(':', '')
        message_name = words[3]
        message_name = message_name[:message_name.index("[")]
        parameter_set = parameters.split(", ")

        outs = []
        ins = []
        nils = []
        keys = []
        list = []

        for sets in parameter_set:

            sets = sets.split(" ")
            parameter_name = sets[1]
            if sets[0]=="in":
                ins.append(sets[1])
                list.append(sets[1])
            elif sets[0]=="out":
                outs.append(sets[1])
                list.append(sets[1])
            elif sets[0]=="nil":
                nils.append(sets[1])
                list.append(sets[1])
            else:
                print("Error: No such type of parameter:" + sets[0])

            if len(sets)==3:

                if sets[2] == "key":
                    keys.append(sets[1])

        #Recoding information about a message retrieved from a protocol in a Message object
        #so that the protocol structure is stored on a list of Messages called "protocol"
        message = Message(from_, to_, message_name, outs, ins, nils, keys, list)
        protocol.append(message)

    #DEBUGGING: printing protocol struture
    for message in protocol:
        print("From: " + message.from_)
        print("To: " + message.to_)
        print("Message: " + message.message)
        print("Out parameters: " + str(message.out_param))
        print("In parameters: " + str(message.in_param))
        print("Nil parameters: " + str(message.nil_param))
        print("Key parameters: " + str(message.key_param))
        print("Listed parameters: " + str(message.list_param))
        print("***")

        #CREATING A TABLE TO STORE MESSAGES THAT HAVE BEEN SEEN
        query = "create table " + message.message + " ( "
        counter = 0
        for param in message.list_param:
            counter = counter + 1
            query = query + str(param) + " text "
            if not counter == len(message.list_param):
                query = query + ", "

        if message.key_param is not []:
            query = query + ", primary key ("
        counter2 = 0

        for param in message.key_param:
            counter2 = counter2 + 1
            query = query + param
            if not counter2 == len(message.key_param):
                query = query + ", "

        if message.key_param is not []:
            query = query + ")"
        query = query + ")"
        print(query)
        #c.execute(query)
    c.execute("delete from RequestLabel;")
    #c.execute("insert into RequestLabel (orderID, address) values ('1', 'Brunswick'); ")
    #c.execute("insert into RequestLabel (orderID, address) values ('2', 'Bruasdasfnswick'); ")
    #c.execute("insert into RequestLabel (orderID, address) values ('3', 'Brunasdswick'); ")


def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


def insert(message, c):
    #Check if message matches schema and
    #Throw error if message does NOT match schema
    #OR has an undefined key parameter,
    #OR is a duplicate,
    #OR its contents are inconsistent with a previously stored message of the same or a different name.

    print("INSERTION STARTED")
    #Check against the protocol schema ot the db one.
    #Write an email before implemeting something to get opinion.
    schema = []
    for key in message.parameters:
        schema.append(key)

    match = None

    print("Schema is: " + str(schema))
    for message_type in protocol:
        print(message_type.list_param)
        if set(schema) == set(message_type.list_param):
            match = message_type.message
            matched_message = message_type

    if match is None:
        print("No table matching the schema was found. UNDEFINED-MESSAGE exception.")
        raise Exception("No table matching the schema was found. UNDEFINED-MESSAGE exception.")
    else:
        print("Match found: " + match)

        #Check if any key or non-nilable parameter of m has nil binding in tself.
    parameters = message.parameters
    print("Parameters: " + str(parameters))

    schema_exception = False

    for keys in matched_message.key_param:
        if str(parameters[keys]) is None or str(parameters[keys]) == '':
            schema_exception = True
    for keys in matched_message.in_param:
        if str(parameters[keys]) is None or str(parameters[keys]) == '':
            schema_exception = True
    for keys in matched_message.out_param:
        if str(parameters[keys]) is None or str(parameters[keys]) == '':
            schema_exception = True


    if schema_exception:
        print("SCHEMA VIOLATION exception.")
        raise Exception("SCHEMA VIOLATION exception.")
    else:
        query = "SELECT EXISTS" + "(" + "SELECT 1 FROM " + match + " WHERE "
        counter6=0
        for params in message.parameters:
            counter6 = counter6 + 1
            query = query + params + "=" + "\"" + str(message.parameters[params]) + "\""
            if counter6 is not len(schema):
                query = query + " AND "
            else:
                query = query + ");"
        print(query)

        c.execute(query)
        result = c.fetchone()
        print(result[0])

        #DOesnt work?
        if result[0]==1:
            print("Such entry already exists.")
            return False
        else:
            #Check for every table if despite key values being there, non-key values are DIFFERET from intersections.
            for message_type in protocol:
                print(str(message_type.message))
                intersection = []
                keys = []
                for params in message.parameters:
                    if params in message_type.list_param:
                        intersection.append(params)
                print("Intersection with " + message_type.message + " is " + str(intersection))
                #Finding subset of KEYS in the Intersection
                for params in intersection:
                    if params in message_type.key_param:
                        keys.append(params)
                print("Keys in the intersection are: " + str(keys))

                #Check if these keys exist in the relation AND the any of other params differ:
                query = "SELECT EXISTS" + "(" + "SELECT 1 FROM " + message_type.message + " WHERE "

                counter6 = 0
                for key in keys:
                    counter6 = counter6 + 1
                    query = query + str(key) + "='" + str(message.parameters[key]) + "'"
                    if counter6 is not len(keys):
                        query = query + " AND "
                    else:
                        query = query + ");"
                print(query)

                c.execute(query)
                result = c.fetchone()
                belongs = True
                print(result)
                if result[0]==1:
                    print("ENTRY FIELD WITH SUCH KEYS EXISTS")
                    for param in intersection:
                        query = "SELECT " + str(param) + " FROM " + str(message_type.message) + " WHERE "

                        counter7 = 0
                        for key in keys:
                            counter7 = counter7 + 1
                            query = query + str(key) + "=" + str(message.parameters[key])

                            if counter7 is not len(keys):
                                query = query + " AND "
                            else:
                                query = query + ";"

                        print(query)
                        c.execute(query)
                        value = c.fetchone()

                        print("Value is " + value[0])

                        #Compare that the value matches the one in the message

                        if str(value[0])!=str(message.parameters[param]):
                            belongs = False

                    if belongs == False:
                        print("INCONSISTENT-MESSAGE EXCEPTION")
                        raise Exception("INCONSISTENT-MESSAGE EXCEPTION")


            #Inserting a message into local store
            insert_query = "INSERT INTO " + match + " ("

            counter7 = 0
            for columns in schema:
                counter7 = counter7 + 1
                insert_query = insert_query + columns

                if counter7 is not len(schema):
                    insert_query = insert_query + ", "
                else:
                    insert_query = insert_query + ")"

            insert_query = insert_query + " VALUES ("

            counter8 = 0
            for columns in schema:
                counter8 = counter8 + 1
                insert_query = insert_query + "'" + str(message.parameters[columns]) + "'"

                if counter8 is not len(schema):
                    insert_query = insert_query + ", "
                else:
                    insert_query = insert_query + ")"
            insert_query = insert_query + ";"

            print("QUERY: " + insert_query)

            c.execute(insert_query)
            inserted = c.fetchone()
            print(inserted)


    return False


def send(message, c):
    #for all parameters p in schema m do:   known ← false
    # p = [o1, brunswick], m = [orderID, address]
    # for each p in m
    # known = False
    # 1) for orderID: for each table - if orderID is in it then U=[orderID,address]/\[orderID, address, blabla] = [orderID, address]
    known = {}

    intersection = OrderedDict()

    print("SENDING ALGORITHM STARTED")
    for parameters in message.parameters:
        print("************")
        print("Parameter " + parameters)
        print("************")
        known[parameters] = False

        #For every message type that mentions this parameter need to find intersection in schemas
        for message_type in protocol:
            if parameters in message_type.list_param:
                #take this particular db table and check if this message instance is alrerady there
                print(parameters + " parameter is in " + message_type.message)
                #Find intersection between schemas
                #keys = set(message_type.list_param).intersection(message.parameters)

                s1 = set(message_type.list_param)
                s2 = set(message.parameters.keys())
                s3 = s1 & s2

                intersection = dict([(k,message.parameters[k]) for k in s3])
                #intersection = {k:message.parameters[k] for k in keys}
                print(message_type.list_param)
                print(str(message.parameters))
                print(intersection)

                query = "SELECT * FROM " + message_type.message + " WHERE "
                counter3 = 0
                for key in intersection:
                    counter3 = counter3 + 1
                    query = query + str(key) + "='" + str(intersection[key]) + "'"
                    if len(intersection) is not counter3:
                        query = query + " and "

                query = query + ";"
                print(query)
                c.execute(query)
                result = c.fetchone()
                print(result)

                comparison = "("
                counter4 = 0
                for key in intersection:
                    counter4 = counter4 + 1
                    comparison = comparison + "'" + str(intersection[key]) + "'"
                    if counter4 is not len(intersection):
                        comparison = comparison + ", "
                comparison = comparison + ")"
                print("Comparison : " + comparison)
                #print("Result : " + result)

                print(str(result))

                if str(result) == comparison:
                    print("The values are known!")
                    known[parameters] = True


            if not known[parameters] and parameters in message_type.in_param:
                print("In-adornment violation exception")
                raise Exception("In-adornment violation exception")
            if known[parameters] and parameters in message_type.out_param:
                print("Out-adornment violation exception")
                raise Exception("Out-adornment violation exception")
            if known[parameters] and parameters in message_type.nil_param:
                print("Nil-adornment violation exception")
                raise Exception("Nil-adornment violation exception")

        insert(message,c)



def receive(message):
    check(message)
    insert(message)


def check(message):
    print("Message passed checking")

#Class to represent a BSPL message that allows storing information about it
#Used to store a protocol structure as a list of BSPL messages
class Message:
    def __init__(self, from_, to_, message, out_param, in_param, nil_param, key_param, list_param):
        self.from_ = from_
        self.to_ = to_
        self.message = message
        self.out_param = out_param
        self.in_param = in_param
        self.nil_param = nil_param
        self.key_param = key_param
        self.list_param = list_param


class Message_:
    def __init__(self, from_, to_, parameters):
        self.from_ = from_
        self.to_ = to_
        self.parameters = parameters


def create_Message_(from_, to_, parameters):
    message = Message_(from_, to_, parameters)
    return message
