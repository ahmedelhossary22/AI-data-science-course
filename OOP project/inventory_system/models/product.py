from models.offer import Offer
class Product:
    def __init__(self, id, name, category, productionDate, expirationDate, quantity, price, offer=None):
        self._id = id
        self._name = name
        self._category = category
        self._price = price
        self._productionDate = productionDate
        self._expirationDate = expirationDate
        self._quantity = quantity
        self._offer = offer

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_category(self):
        return self._category

    def set_category(self, category):
        self._category = category

    def get_production_date(self):
        return self._productionDate

    def set_production_date(self, productionDate):
        self._productionDate = productionDate

    def get_expiration_date(self):
        return self._expirationDate

    def set_expiration_date(self, expirationDate):
        self._expirationDate = expirationDate

    def get_quantity(self):
        return self._quantity

    def set_quantity(self, quantity):
        self._quantity = quantity

    def get_price(self):
        return self._price

    def set_price(self, price):
        self._price = price

    def get_offer(self):
        return self._offer

    def set_offer(self, offer):
        self._offer = offer

    def get_effective_price(self):
        if self._offer is not None and self._offer.is_active_today():
            return self._price * (1 - self._offer.get_discount())
        return self._price
    def __str__(self):
        return (
        f"[{self._id}] {self._name:<15} | {self._category:<10} | "
        f"Prod: {self._productionDate} | Exp: {self._expirationDate} | "
        f"Qty: {self._quantity} | Price: ${self._price:.2f} | "
        f"Effective: ${self.get_effective_price():.2f}"
        )