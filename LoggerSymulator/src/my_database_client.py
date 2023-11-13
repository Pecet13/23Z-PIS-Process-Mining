class my_database_client:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def connect(self):
        # implementation of database connection
        pass

    def disconnect(self):
        # implementation of database disconnection
        pass

    def execute_query(self, query):
        # implementation of query execution
        pass
