def check(message, admins) -> bool:
    return admins.contains(str(message.from_user.username).lower()) or admins.contains(str(message.from_user.id))