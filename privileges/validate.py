import privileges.admins as admins

def check(message) -> bool:
    return admins.contains(str(message.from_user.username).lower()) or admins.contains(str(message.from_user.id))