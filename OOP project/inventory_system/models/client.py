from models.person import Person 

class Client(Person):
    def __init__(self,name,email,phone,id=None):
        super().__init__(name,email,id)
        self._phone = phone
    @property
    def phone(self):
        return self._phone
    
    def set_phone(self,phone):
        self._phone = phone
    def __str__(self):
         return f"Client: [{self.id}] {self.name} ({self.email}, {self.phone})"