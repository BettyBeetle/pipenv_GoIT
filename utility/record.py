from datetime import datetime, timedelta
from utility.name import Name
from utility.phone import Phone
from utility.email import Email
from utility.birthday import Birthday
from utility.address import Address


class Record:
    """
    Record class represents a single address book record consisting of name, phone list, email list and birthday.
    """

    def __init__(self, name: Name, phones=[], emails=[], birthday=None, address=None) -> None:
        self._name = name
        self._phones = phones
        self._emails = emails
        self._birthday = birthday
        self._address = address

    # overridden method __repr__
    def __repr__(self) -> str:
        record_info = f"Name: {self.name}\n"
        if self.phones:
            record_info += "Phones:\n"
            for phone in self.phones:
                record_info += f"    - {phone}\n"
        if self.emails:
            record_info += "Emails:\n"
            for email in self.emails:
                record_info += f"    - {email}\n"
        if self.birthday:
            record_info += f"Birthday:\n    {self.birthday}\n    {self.days_to_birthday()}\n"
        if self.address:
            record_info += f"Address:\n    Street: {self.address.street}\n"
            record_info += f"    City: {self.address.city}\n"
            record_info += f"    Zip Code: {self.address.zip_code}\n"
            record_info += f"    Country: {self.address.country}\n"
        record_info += "----------------------------------\n"
        return record_info

    # name section
    # Getter for name
    @property
    def name(self):
        return self._name

    # Setter name
    @name.setter
    def name(self, name):
        self._name = name

    # phones section
    # Getter for phones
    @property
    def phones(self):
        return self._phones

    # Setter phones
    @phones.setter
    def phones(self, phones):
        self._phones = phones

    # Add phone to phones list
    def add_phone(self, phone: Phone):
        self._phones.append(phone)

    # Remove phone from phones list
    def remove_phone(self, phone: Phone):
        self._phones.remove(phone)

    # Change phone - add new one and remove old one
    def change_phone(self, old_phone, new_phone):
        index = self._phones.index(old_phone)
        self._phones[index] = new_phone

    # Show return formated string with all phones
    def show_phones(self):
        phones_str = ""
        i = 1
        for phone in self._phones:
            phones_str += f"\n{i}) {phone};"
            i += 1
        return phones_str

    # emails section
    # Getter for emails
    @property
    def emails(self):
        return self._emails

    # Setter emails
    @emails.setter
    def emails(self, emails):
        self._emails = emails

    # Add email to emails list
    def add_email(self, email: Email):
        self._emails.append(email)

    # Remove email from emails list
    def remove_email(self, email: Email):
        self._emails.remove(email)

    # Change email - add new one an dremove old one
    def change_email(self, old_email, new_email):
        index = self._emails.index(old_email)
        self._emails[index] = new_email

    # Show return formated string with all emails
    def show_emails(self):
        emails_str = ""
        i = 1
        for email in self._emails:
            emails_str += f"\n{i}) {email};"
            i += 1
        return emails_str

    # birthday section
    # Getter for birthday
    @property
    def birthday(self):
        return self._birthday

    # Setter birthday
    @birthday.setter
    def birthday(self, birthday):
        self._birthday = birthday

    def days_to_birthday(self):
        current_date = datetime.now().date()
        this_year_birthday = datetime(
            year=current_date.year,
            month=self.birthday.value.month,
            day=self.birthday.value.day,
        ).date()
        difference = this_year_birthday - current_date
        if difference.days == 0:
            return f"{self.name}'s birthday is today!"
        elif difference.days > 0:  # if the birthday is before this year's end
            return f"day(s) to next birthday: {difference.days}"
        # if the next birthday is in next year
        next_birthday = datetime(
            year=this_year_birthday.year + 1,
            month=this_year_birthday.month,
            day=this_year_birthday.day,
        ).date()
        return f"day(s) to next birthday: {(next_birthday -  current_date).days}"
    
    # address section
    # Getter for address
    @property
    def address(self):
        return self._address

    # Setter for address
    @address.setter
    def address(self, address):
        self._address = address

    # Add address to the record
    def add_address(self, address: Address):
        self._address = address

    # Change address in the record
    def change_address(self, new_address: Address):
        self._address = new_address
