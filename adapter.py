import requests
import adapter
from flask import Flask, json
import sqlite3

protocol_path = "protocol.txt"
schema_path = "schema.txt"

def enable_adapter(c):
    #PARSING PROTOCOL
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

        for sets in parameter_set:

            sets = sets.split(" ")
            parameter_name = sets[1]
            if sets[0]=="in":
                ins.append(sets[1])
            elif sets[0]=="out":
                outs.append(sets[1])
            elif sets[0]=="nil":
                nils.append(sets[1])
            else:
                print("Error: No such type of parameter:" + sets[0])

            if len(sets)==3:

                if sets[2] == "key":
                    keys.append(sets[1])

        #Recoding information about a message retrieved from a protocol in a Message object
        #so that the protocol structure is stored on a list of Messages called "protocol"
        message = Message(from_, to_, message_name, outs, ins, nils, keys)
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
        print("***")



def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


def insert(message):
    #Check if message matches schema and
    #Throw error if message does NOT match schema
    #OR has an undefined key parameter,
    #OR is a duplicate,
    #OR its contents are inconsistent with a previously stored message of the same or a different name.
    print("Message inserted.")


def send(message):
    check(message)
    insert(message)
    print("Message sent.")


def receive(message):
    check(message)
    insert(message)


def check(message):
    print("Message passed checking")

#Class to represent a BSPL message that allows storing information about it
#Used to store a protocol structure as a list of BSPL messages
class Message:
    def __init__(self, from_, to_, message, out_param, in_param, nil_param, key_param):
        self.from_ = from_
        self.to_ = to_
        self.message = message
        self.out_param = out_param
        self.in_param = in_param
        self.nil_param = nil_param
        self.key_param = key_param
