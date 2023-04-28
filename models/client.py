class ClientModel:
    def __init__(self, client_id, nome):
        self.client_id = client_id
        self.nome=nome

    def exists(clientlist, client_id):
        for client in clientlist:
            if client['client_id'] == client_id:
                return True
        return False