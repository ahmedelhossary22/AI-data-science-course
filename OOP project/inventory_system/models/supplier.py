from models.person import Person
class Supplier(Person):
    def __init__(self,name,email,id=None):
        super().__init__(name,email,id)
    def __str__(self):
        return f"Supplier: [{self.id}] {self.name} ({self.email})"   