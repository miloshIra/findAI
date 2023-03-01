import datetime


class User:
    def __init__(self, username, password, company):
        self.username = username
        self.password = password
        self.company = company
        self.created = datetime.datetime.now()

    def __repr__(self):
        return self

    def __str__(self):
        return self.username

