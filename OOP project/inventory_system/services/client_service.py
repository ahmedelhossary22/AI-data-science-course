class ClientService:
    def __init__(self):
        self._clients = []

    def add_client(self, client):
        self._clients.append(client)

    def get_all_clients(self):
        return self._clients.copy()

    def find_client_by_id(self, client_id):
        for client in self._clients:
            if client.id == client_id:
                return client
        return None

    def delete_client(self, client_id):
        original_len = len(self._clients)
        self._clients = [c for c in self._clients if c.id != client_id]
        return len(self._clients) < original_len

    def update_client(self, client_id, name=None, email=None, phone=None):
        client = self.find_client_by_id(client_id)
        if client:
            if name is not None:
                client.set_name(name)
            if email is not None:
                client.set_email(email)
            if phone is not None:
                client.set_phone(phone)
            return True
        return False

    def search_by_name(self, name):
        return [
            c for c in self._clients
            if name.lower() in c.name.lower()
        ]