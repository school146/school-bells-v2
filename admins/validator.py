import sqlite3
import admins.storage

def check(message, connection: sqlite3.Connection) -> bool:
    return admins.storage.contains(str(message.from_user.username).lower(), connection) or admins.storage.contains(str(message.from_user.id), connection)