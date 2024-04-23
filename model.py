# тут должен быть from pydantic ...
class Vehicle:
    class Meta:
        verbose_name = 'Vehicle'
        verbose_name_plural = 'Vehicles'

    def __init__(self, name: str, model: str, year: int, color: str, price: float, latitude: float, longitude: float, id: int = None) -> None:
        self.id = id
        self.name = name
        self.model = model
        self.year = year
        self.color = color
        self.price = price
        self.latitude = latitude
        self.longitude = longitude

    def to_dict(self): # -> Dict[str, Any]:
        return {
            "id": self.id,
            'name': self.name,
            'model': self.model,
            'year': self.year,
            'color': self.color,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude
        }

    def __str__(self):
        return f"{self.id}, {self.name}, {self.model}, {self.year}, {self.color}, {self.price}, {self.latitude}, {self.longitude}"
