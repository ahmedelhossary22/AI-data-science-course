from datetime import date

class Order:
    next_id = 1

    def __init__(self, client_id, product_id, quantity, total_amount, order_date=None, id=None):
        # Case 1: loading from file (manual id)
        if id is not None:
            self._id = id
            if id >= Order.next_id:
                Order.next_id = id + 1
        else:
            # Case 2: auto ID
            self._id = Order.next_id
            Order.next_id += 1

        self._client_id = client_id
        self._product_id = product_id
        self._quantity = quantity
        self._total_amount = total_amount
        self._order_date = order_date if order_date is not None else date.today()

    @property
    def id(self):
        return self._id

    @property
    def client_id(self):
        return self._client_id

    @property
    def product_id(self):
        return self._product_id

    @property
    def quantity(self):
        return self._quantity

    @property
    def date(self):
        return self._order_date

    @property
    def total(self):
        return self._total_amount

    def __str__(self):
        return (
            f"Order#{self.id} | "
            f"Client:{self.client_id} | "
            f"Prod:{self.product_id} | "
            f"Qty:{self.quantity} | "
            f"Date:{self.date} | "
            f"${self.total:.2f}"
        )