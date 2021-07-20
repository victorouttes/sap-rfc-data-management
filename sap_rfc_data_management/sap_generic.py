from .connection import SAPConnection


class SAP:
    def __init__(self, connection: SAPConnection):
        self.connection = connection
