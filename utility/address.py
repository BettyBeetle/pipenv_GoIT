# class Address defined in separate file 
# address.py

class Address:
    def __init__(self, street, city, zip_code, country):
        self.street = street
        self.city = city
        self.zip_code = zip_code
        self.country = country

    def __str__(self):
        return f"Address:\nStreet: {self.street}\nCity: {self.city}\nZIP Code: {self.zip_code}\nCountry: {self.country}\n"

