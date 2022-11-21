from termcolor import colored

def log_admin_adding(granter: str, receiver: str, additional: str = ''):
    print(colored(f'@{granter}', 'blue'), colored('--admin previledges-->', 'green'), colored(f'@{receiver}', 'blue'), additional)

def log_admin_removing(granter: str, receiver: str, additional: str = ''):
    print(colored(f'@{granter}', 'blue'), colored('<--took admin previledges--', 'red'), colored(f'@{receiver}', 'blue'), additional)

def log_rejected_admin_adding(granter: str, receiver: str, additional: str = ''):
    print(colored(f'@{granter}', 'grey'), colored('--granting rejected-->', 'grey'), colored(f'@{receiver}', 'grey'), additional)

def log_rejected_admin_removing(granter: str, receiver: str, additional: str = ''):
    print(colored(f'@{granter}', 'grey'), colored('<--taking previledges rejected--', 'grey'), colored(f'@{receiver}', 'grey'), additional)
