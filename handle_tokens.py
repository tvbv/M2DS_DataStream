from os import path


tokens_path = 'tokens.txt'


def get_username():
    return input('To get started, enter your username: ')


def query_tokens():
    if not path.exists(tokens_path):
        with open(tokens_path, 'w') as f:
            f.write('')
        return {}
    with open(tokens_path, 'r') as f:
        tokens = f.read().splitlines()
    return {token.split(':')[0]: token.split(':')[1] for token in tokens}


def query_token(user):
    tokens = query_tokens()
    if user in tokens:
        return tokens[user]
    else:
        return None


def ask_for_token():
    return input('New user dectected. Enter your bearer token: ')


def add_token(username, token_encoded):
    with open(tokens_path, 'a') as f:
        f.write(f'{username}:{token_encoded}\n')


def get_bearer_token():
    username = get_username()
    token = query_token(username)
    new_user = False
    if token is None:
        new_user = True
        token = ask_for_token()
    return username, token, new_user


def remove_token(username):
    tokens = query_tokens()
    if username in tokens:
        del tokens[username]
        with open(tokens_path, 'w') as f:
            for username, token in tokens.items():
                f.write(f'{username}:{token}\n')
        return True
    else:
        return False
