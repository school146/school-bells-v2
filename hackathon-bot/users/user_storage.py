import os

class UserStorage():
    file = None
    path : str

    def __init__(self, path: str):
        self.path = path
        
        permissions = 'r+'
        if not os.path.isfile(self.path):
            permissions = 'w+'

        self.file = open(self.path, permissions)
        if self.file.read() == '': 
            self.file.write('[]')
        self.file.close()

    def deserialize(self) -> object:
        self.file = open(self.path, 'r')
        content = self.file.read()
        self.file.close()

        return content.replace('[', '').replace(']', '').replace(',', '').replace('\'', '').split()

    def append_user(self, id): # -> UserStorage
        users = self.deserialize()
        id = str(id).replace('@', '').lower()

        if str(id) not in users:
            users.append(id)

        self.file = open(self.path, 'w')
        self.file.write(str(users))
        self.file.close()

        return self

    def remove_user(self, id):
        users = self.deserialize()
        id = str(id).replace('@', '').lower()

        if id in users:
            del users[users.index(id)]

        self.file = open(self.path, 'w')
        self.file.write(str(users))
        self.file.close()

        return self

    def contains(self, id: str):
        users = self.deserialize()
        return id in users

