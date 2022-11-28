from enum import Enum

class AppendAdminStatus(Enum):
    OK = True
    USER_ALREADY_EXISTS = False

class DeleteAdminStatus(Enum):
    OK = 'Пользователь удалён'
    USER_NOT_ADMIN = 'Пользователь и так не администратор!'