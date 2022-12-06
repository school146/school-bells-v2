import sqlite3
import admins.storage
import configuration

connection = configuration.connection

def check(message) -> bool:
    return admins.storage.contains(str(message.from_user.username).lower()) or admins.storage.contains(str(message.from_user.id))