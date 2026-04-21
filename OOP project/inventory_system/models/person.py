class Person:
    next_id = 1

    def __init__(self, name, email, id=None):
        if id is not None:
            self._id = id
            if id >= Person.next_id:
                Person.next_id = id + 1
        else:
            self._id = Person.next_id
            Person.next_id += 1

        self._name = name
        self._email = email

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    
    @property
    def email(self):
        return self._email

    def set_email(self, email):
        self._email = email