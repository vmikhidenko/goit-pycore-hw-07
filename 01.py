from collections import UserDict
import re
from datetime import datetime

class Field:
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        super().__init__(value)

class Phone(Field):
    def __init__(self, value=None):
        super().__init__(value)
        
    def validate_phone(self):
        # Format phone number to delete all non-digit characters
        normalized_value = re.sub(r'\D', '', self.value)
        if re.fullmatch(r"\d{10}", normalized_value):
            self.value = normalized_value  # Update value with normalized phone number
            return True
        else:
            raise ValueError("Phone number must be exactly 10 digits")

class Birthday(Field):
    def __init__(self, value=None):
        super().__init__(value)

    def validate_birthday(self, fmt='%d/%m/%Y'):
        try:
            self.date = datetime.strptime(self.value, fmt)  # Date validation added
            return self.date
        except ValueError:
            raise ValueError("Invalid date format. Use DD/MM/YYYY")  # Adjusted format to DD/MM/YYYY

    def __str__(self):
        return self.value if self.value else "No birthday"  # String representation of birthday

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):
        phones_str = '; '.join(str(phone) for phone in self.phones) if self.phones else "No phones"
        birthday_str = str(self.birthday) if self.birthday else "No birthday"
        return f"Contact name: {self.name.value}, phones: {phones_str}, birthday: {birthday_str}"

    def add_birthday(self, birthday):
        birthday_field = Birthday(birthday)
        try:
            birthday_field.validate_birthday()
            self.birthday = birthday_field
        except ValueError as e:
            print(e)
    
    def add_phone(self, phone):
        phone_field = Phone(phone)
        try:
            phone_field.validate_phone()
            self.phones.append(phone_field)
        except ValueError as e:
            print(e)

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if str(p) != phone]

    def edit_phone(self, old_phone, new_phone):
        for idx, phone in enumerate(self.phones):
            if str(phone) == old_phone:
                phone_field = Phone(new_phone)
                try:
                    phone_field.validate_phone()
                    self.phones[idx] = phone_field
                except ValueError as e:
                    print(e)
                break

    def find_phone(self, phone):
        for p in self.phones:
            if str(p) == phone:
                return p
        return None

class AddressBook(UserDict):
    def add_record(self, record):
        if not isinstance(record, Record):
            raise ValueError("Value must be an instance of Record")
        self.data[record.name.value] = record
        
    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

# Creating a new address book
book = AddressBook()

# Creating a record for John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")
john_record.add_birthday("28/03/1996")  # Fix: Provide date as a string

# Adding John's record to the address book
book.add_record(john_record)

# Creating and adding a new record for Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Printing all records in the book
for name, record in book.data.items():
    print(record)

# Finding and editing a phone number for John
john = book.find("John")
if john:
    john.edit_phone("1234567890", "1112223333")

# Finding a specific phone number in John's record
found_phone = john.find_phone("5555555555") if john else None
if found_phone:
    print(f"{john.name}: {found_phone}")

# Deleting Jane's record
book.delete("Jane")
