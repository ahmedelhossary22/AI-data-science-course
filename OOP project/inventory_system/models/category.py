class Category:
    next_id = 1

    def __init__(self, name, id=None):
        if id is not None:
            self._id = id
            if id >= Category.next_id:
                Category.next_id = id + 1
        else:
            self._id = Category.next_id
            Category.next_id += 1

        self._name = name
    @property
    def id(self):
        return self._id

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def __str__(self):
        return f"[{self._id}] {self._name}"