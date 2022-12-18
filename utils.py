from kafka import KafkaConsumer, KafkaProducer
import os


#########
# Kafka #
#########


def get_bearer_token():
    tokens_path = 'token/token.txt'
    with open(tokens_path, 'r') as f:
        token = f.read().splitlines()
    return token[0]


def get_kafka_topic(default_topic):
    kafka_topic = input(f'Enter the name of the Kafka topic (leave blank to use "{default_topic}"): ')
    if kafka_topic == '':
        kafka_topic = default_topic
    return kafka_topic


def get_kafka_producer(port='9092'):
    return KafkaProducer(bootstrap_servers=f'localhost:{port}', value_serializer=lambda x: x.encode('utf-8'))


def get_kafka_consumer(kafka_topic, port='9092', group_id=None):
    # kafka_topic can be a string or a list of strings
    if group_id is None:
        consumer = KafkaConsumer(bootstrap_servers=f'localhost:{port}', value_deserializer=lambda x: x.decode('utf-8'))
    else:
        consumer = KafkaConsumer(bootstrap_servers=f'localhost:{port}', value_deserializer=lambda x: x.decode('utf-8'),
                                 group_id=group_id)
    consumer.subscribe(kafka_topic)
    return consumer


############
# Keywords #
############


def get_keywords():
    while True:
        print('Select an option:')
        print('1. Load keywords')
        print('2. Enter keywords')
        print('3. Do nothing (use default keywords)')
        option = input('Option: ')
        try:
            option = int(option)
            if option < 1 or option > 3:
                print('Invalid option. Try again.')
                continue
            break
        except:
            print('Invalid option. Try again.')

    if option == 1:
        return load_keywords()
    elif option == 2:
        keywords = add_keywords()
        save = input('Save keywords? (y/n): ')
        if save.lower() == 'y':
            save_keywords(keywords)
    if option == 3:
        return load_keywords('default_keywords')
    return keywords


def add_keywords():
    keywords = []
    while True:
        keyword = input('Enter a keyword (leave blank to stop): ')
        if keyword == '':
            if len(keywords) == 0:
                print('You must enter at least one keyword.')
                continue
            break
        else:
            keywords.append(keyword)
    return keywords


def load_keywords(keywords_path='', default_extension='txt'):
    keywords_path = get_path(keywords_path, 'keywords', default_extension)
    with open(keywords_path, 'r') as f:
        keywords = f.read().splitlines()
    return keywords


def save_keywords(keywords, keywords_path='', default_extension='txt'):
    keywords_path = get_path(keywords_path, 'keywords', default_extension)
    if not os.path.exists(os.path.dirname(keywords_path)):
        os.makedirs(os.path.dirname(keywords_path))
    with open(keywords_path, 'w') as f:
        for keyword in keywords:
            f.write(f'{keyword}\n')


###############
# Files paths #
###############


def get_path(path, usage='keywords', default_extension='txt'):
    if path != '':
        return enrich_path(path, usage, default_extension)
    print(f'Default directory: {usage + "/"}')
    print(f'Default extension: ".{default_extension}"')
    print('To change these default values, provide a full path with the desired directory and extension')
    while True:
        path = input(f'Enter the path to the file: ')
        if path == '':
            print('Path cannot be empty.')
        else:
            break
    return enrich_path(path, usage, default_extension)


def enrich_path(path, usage, default_extension):
    # if not extension provided
    extensions = ['.txt', '.csv', '.json', 'xlsx', '.xls', '.xml']
    if not any(path.endswith(extension) for extension in extensions):
        path += '.' + default_extension
    # if the user didn't provide a path to a directory, assume they want to use usage/ as the directory
    if '/' not in path:
        path = f'{usage}/{path}'
    return path
