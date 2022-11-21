from termcolor import colored

def log_sucessful_ring(id):
    print(colored(f'🔔 @{id}', 'blue'), colored('initialised manual ring', 'green'))

def log_unsuccessful_ring(id):
    print(colored(f'🔕 @{id}', 'blue'), colored('failed to initialize manual ring', 'red'))
