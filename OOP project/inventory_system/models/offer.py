from datetime import date

class Offer:
    def __init__(self, product_id, discount, start_date, end_date):
        self._product_id = product_id
        self._discount = discount  
        self._start_date = start_date
        self._end_date = end_date

    # Getters
    def get_product_id(self):
        return self._product_id

    def get_discount(self):
        return self._discount

    def get_start_date(self):
        return self._start_date

    def get_end_date(self):
        return self._end_date

    
    def is_active_today(self):
        today = date.today()
        return self._start_date <= today <= self._end_date

    
    def __str__(self):
        return (
            f"Offer on ProductID {self._product_id}: "
            f"{self._discount * 100:.0f}% off from "
            f"{self._start_date} to {self._end_date}"
        )