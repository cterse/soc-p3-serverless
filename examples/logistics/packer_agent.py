import pos
import os
logistics_dir = os.path.dirname(__file__)
db_path = os.path.join(logistics_dir, "test")
protocol_path = os.path.join(logistics_dir, "protocol.txt")
configuration_path = os.path.join(logistics_dir, "configuration.txt")

name = "Packer"
adapter = pos.Adapter(name, protocol_path, configuration_path, db_path)

enactments = {}
@adapter.register_handler("Wrapped")
def Wrapped(message):  # need enactment parameter...
    pass


@adapter.register_handler("Labeled")
def Labeled(message):
    pass


if __name__ == '__main__':
    adapter.run()
