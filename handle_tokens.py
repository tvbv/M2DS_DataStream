from os import path
from cryptography.fernet import Fernet
from pwinput import pwinput


users = ['Luc', 'Thomas', 'Titouan', 'Other']
tokens_path = 'tokens.txt'
fernet_key_path = 'fernet_key.txt'


def get_user_name():
    print('To get started, choose a creator (enter the name or the associated number.)')
    print(f'The first {len(users) - 1} are the developers of this program.')
    print(f'If you are not one of them, enter {len(users)} or {users[-1]}.')
    while True:
        for i, creator in enumerate(users):
            print(f'{i+1}. {creator}')
        choice = input('Your choice: ')
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(users):
                return users[choice-1]
        elif choice in users:
            return choice
        print('Invalid choice, try again.')


def query_tokens():
    if not path.exists(tokens_path):
        with open(tokens_path, 'w') as f:
            f.write('')
        return {}
    with open(tokens_path, 'r') as f:
        tokens = f.read().splitlines()
    return {token.split(':')[0]: token.split(':')[1] for token in tokens}


def query_token(user):
    if isinstance(user, int):
        user = users[user]
    tokens = query_tokens()
    if user in tokens:
        return tokens[user]
    else:
        return None


def decode_token(encoded_token, fernet_key):
    return fernet_key.decrypt(encoded_token.encode()).decode()


def encode_token(token, fernet_key):
    return fernet_key.encrypt(token.encode('utf-8')).decode('utf-8')


def ask_for_token():
    tries = 3
    print('New user dectected.')
    print(f'Enter the token. You have {tries} tries.')
    print('(Note: this will be encoded with a password afterwards.)')
    while tries > 0:
        token = pwinput('Token: ')
        token_confirm = pwinput('Confirm the token: ')
        if token == token_confirm:
            return token
        tries -= 1
        print(f'The tokens do not match, you have {tries} tries left.')


def add_token(user_name, token_encoded):
    with open(tokens_path, 'a') as f:
        f.write(f'{user_name}:{token_encoded}')


def generate_fernet_key():
    return Fernet.generate_key().decode('utf-8')


def get_fernet_key():
    if not path.exists(fernet_key_path):
        with open(fernet_key_path, 'w') as f:
            key = generate_fernet_key()
            f.write(key)
    else:
        with open(fernet_key_path, 'r') as f:
            key = f.read()
    return key


def get_bearer_token():
    fernet_key = get_fernet_key()
    fernet_key = Fernet(fernet_key.encode('utf-8'))
    user_name = get_user_name()
    token = query_token(user_name)
    if token is None:
        token = ask_for_token()
        token_encoded = encode_token(token, fernet_key)
        add_token(user_name, token_encoded)
    else:
        token = decode_token(token, fernet_key)
    return token
