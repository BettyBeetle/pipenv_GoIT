import pickle 
import csv
from pathlib import Path
from datetime import datetime, timedelta

from collections import UserDict

from utility.record import Record
from utility.name import Name
from utility.phone import Phone
from utility.email import Email
from utility.birthday import Birthday
from utility.address import Address

class AddressBook(UserDict):
    """
    The AddressBook class extends the UserDict class by adding the add_record method
    and checking that the items added to the dictionary are valid (keys and values based on the Record class).

    Args:
        UserDict (class): parent class
    """

    # function used as a decorator to catch errors when item is adding to addressbook
    def _value_error(func):
        def inner(self, record):
            if not isinstance(record, Record):
                raise ValueError
            return func(self, record)

        return inner

    # Add record to addressbook
    @_value_error
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    # Return all names (keys) from addressbook as formated string
    def show_names(self):
        names = []
        for key in self.keys():
            names.append(key)
        names.sort()
        return "\n".join(names)

    # implementation of the iterator method which returns a generator
    def iterator(self, no_of_contacts_to_return=3):
        if len(self.data) > 0:
            current_record_no = 1
            records_info = ""
            for record in self.values():
                records_info += f"Name: {record.name}\n"
                if record.phones:
                    records_info += "Phones:\n"
                    for phone in record.phones:
                        records_info += f"    - {phone}\n"
                if record.emails:
                    records_info += "Emails:\n"
                    for email in record.emails:
                        records_info += f"    - {email}\n"
                if record.birthday:
                    records_info += f"Birthday:\n    {record.birthday}\n    {record.days_to_birthday()}\n"
                if record.address:
                    records_info += f"Address:\n    Street: {record.address.street}\n"
                    records_info += f"    City: {record.address.city}\n"
                    records_info += f"    Zip Code: {record.address.zip_code}\n"
                    records_info += f"    Country: {record.address.country}\n"
                records_info += "----------------------------------\n"
                
                if current_record_no >= no_of_contacts_to_return:
                    yield records_info
                    current_record_no = 1
                    records_info = ""
                    continue
                current_record_no += 1
            yield records_info  # returns the rest if there are no more records and record_no < no_of_contacts_to_return
        else:
            yield "Nothing to show.\n"

    # method to save addressbook to file
    def save_addressbook(self, filename):
        with open(filename, "wb") as fh:
            pickle.dump(self, fh)
       
    # method to read addressbook from file     
    def load_addressbook(self, filename):
        if Path.exists(Path(filename)):
            with open(filename, "rb") as fh:
                return pickle.load(fh)
        return self

    
    def search(self, query: str):
        """
        The method first looks for an exact match in the keys
        then searches the values of the individual records and adds them to the returned Addressbook object if the fragment matches the query.

        Returns:
            Addressbook: a new object of class Addressbook with records based on the query
        """
        query_addressbook = AddressBook()
        query = query.strip()
        key_query = query.title()
        if key_query in self.keys():
            query_addressbook[key_query] = self[key_query]
        for record in self.values():
            if query in record.name.value or key_query in record.name.value:
                query_addressbook[record.name.value] = record
            for phone in record.phones:
                if query in phone.value:
                    query_addressbook[record.name.value] = record
            for email in record.emails:
                if query in email.value:
                    query_addressbook[record.name.value] = record
            if record.birthday is not None:
                if query in str(record.birthday.value):
                    query_addressbook[record.name.value] = record
            if record.address and (query in record.address.street.lower() or
                                   query in record.address.city.lower() or
                                   query in record.address.zip_code.lower() or
                                   query in record.address.country.lower()):
                query_addressbook[record.name.value] = record
        return query_addressbook
            
       
    # export records form addressbook to csv file
    """
    The method exports the data to a csv file. Phones and emails are separated by the '|' char.
    """
    def export_to_csv(self, filename):
        if len(self.data) > 0:
            with open(filename, 'w', newline='') as fh:
                field_names = ['name', 'phones', 'emails', 'birthday', 'street', 'city', 'zip_code', 'country']
                writer = csv.DictWriter(fh, fieldnames=field_names)
                writer.writeheader()
                for record in self.data.values():
                    record_dict = {'name': record.name.value}
                    phones = []
                    for phone in record.phones:
                        phones.append(phone.value)
                    record_dict['phones'] = '|'.join(phones)
                    emails = []
                    for email in record.emails:
                        emails.append(email.value)
                    record_dict['emails'] = '|'.join(emails)
                    if record.birthday is not None:
                        record_dict['birthday'] = record.birthday.value.strftime("%d %m %Y")
                    if record.address:
                        record_dict['street'] = record.address.street
                        record_dict['city'] = record.address.city
                        record_dict['zip_code'] = record.address.zip_code
                        record_dict['country'] = record.address.country
                    writer.writerow(record_dict)
                
                    
    # import from csv file
    """
    The method imports data into a csv file. 
    
    Data structures in the file:
    name,phones,emails,birthsday
    
    Phones and emails are separated (if there is more than one phone or email) with "|".
    Birthday should be written as: day month year e.g. 21 12 1999 or 30-01-2012 or 09/01/1987
    """
    def import_from_csv(self, filename):
        with open(filename, 'r', newline='') as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                name = row['name']
                phones = row['phones'].split('|')
                phones_to_add = []
                for phone in phones:
                    if phone != '':
                        phones_to_add.append(Phone(phone))
                emails = row['emails'].split('|')
                emails_to_add = []
                for email in emails:
                    if email != '':
                        emails_to_add.append(Email(email))
                birthday = row['birthday']
                if birthday != '':
                    birthday = Birthday(birthday)
                else:
                    birthday = None
                street = row['street'] 
                city = row['city']
                zip_code = row['zip_code']
                country = row['country']
                if street or city or zip_code or country:
                    address = Address(street, city, zip_code, country)
                else:
                    address = None
                self.add_record(Record(Name(name), phones_to_add, emails_to_add, birthday, address))
                

    def records_with_upcoming_birthday(self, number_of_days) -> dict:
        """
        The function return a dict which the keys are the days of the week from current day and next 7 days as a datetime.date(), 
        and the values are lists with Records having birthdays on a given day.

        Returns:
            dict: key datetime.date from today + next 7 days, values lists of Records with birthdays in corresponding day
        """
        current_date = datetime.now().date()
        upcoming_birthdays = {current_date + timedelta(days=i): [] for i in range(number_of_days + 1)}
        for record in self.values():
            if record.birthday is not None:
                this_year_birthday = datetime(year=current_date.year, month=record.birthday.value.month, day=record.birthday.value.day).date()
                next_year_birthday = datetime(year=current_date.year + 1, month=record.birthday.value.month, day=record.birthday.value.day).date()

                difference_this_year = (this_year_birthday - current_date).days
                difference_next_year = (next_year_birthday - current_date).days

                difference = difference_this_year if difference_this_year > -1 else difference_next_year
                if -1 < difference <= number_of_days:
                    upcoming_birthdays[current_date + timedelta(difference)].append(record)
        return upcoming_birthdays