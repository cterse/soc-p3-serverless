import pos
import json
import uuid

name = "Labeler"

with open("logistics.json") as stream:
    protocol = json.load(stream)
with open("configuration.yml") as conf:
    configuration = yaml.safe_load(conf)

adapter = pos.Adapter(name, protocol, configuration, 'LabelerHistory')

@adapter.received(protocol['messages']['RequestLabel'])
def handleRequestLabel(message, enactment):
    print("RequestLabel received: " + json.dumps(message))
    labeled = {"orderID": message["orderID"], "address": message["address"], "label": uuid()}
    ok, msg = adapter.send("Packer", labeled)
    if not ok:
        print(msg)


@adapter.sent(protocol['messages']['Labeled'])
def handleLabeled(message, enactment):
    print("Labeled message has been sent: " + json.dumps(message))



def lambda_handler(*args):
    return adapter.handler(*args)
