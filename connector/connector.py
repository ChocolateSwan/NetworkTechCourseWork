import sys
import signal
import os
import subprocess


def parse_connections_file():
    connections = {}
    with open('connections', 'r') as file:
        content = file.read().strip()
        if not content.isspace() and len(content) != 0:
            for str in content.split(';'):
                y = str.split(':')
                connections[y[0].strip()] = y[1].strip()
    return connections


def write_connections_file(connections):
    with open('connections', 'w') as file:
        file.write(';'.join('{}:{}'.format(key, val) for key, val in connections.items()))


def print_connect(alias):
    print(alias + '_1 <=> ' + alias + '_2')


def connect(alias, connections):
    if alias in connections.keys():
        print('Соединение с таким алиасом уже существует')
        return
    command = [
        '/usr/bin/socat',
        'PTY,link=./{0}_1,b9600'.format(alias),
        'PTY,link=./{0}_2,b9600'.format(alias)
    ]
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    connections[alias] = process.pid
    write_connections_file(connections)
    print_connect(alias)


def disconnect(alias, connections):
    if alias not in connections.keys():
        print('Соединение с таким алиасом не существует')
        return
    os.kill(int(connections[alias]), signal.SIGTERM)
    del connections[alias]
    write_connections_file(connections)


def show(connections):
    for x in connections.keys():
        print_connect(x)


def help():
    print('usage:')
    print('connector.py connect alias - create two virtual ports(alias_1, alias_2) and connect them')
    print('connector.py disconnect alias - remove connect and virtual ports(alias_1, alias_2')
    print('connector.py show - print current connections')
    print('connector.py help - show this message')

if __name__ == '__main__':
    if( not (len(sys.argv) == 2 and sys.argv[1] in ('show', 'help')
            or len(sys.argv) == 3 and sys.argv[1] in ('connect', 'disconnect'))):
        help()
        exit(0)

    connections = {}
    try:
        connections = parse_connections_file()
    except:
        print('Ошибка чтения файла подключений')
        print('Файл будет сконфигурирован заново')

    if sys.argv[1] == 'connect':
        connect(sys.argv[2], connections)
    elif sys.argv[1] == 'disconnect':
        disconnect(sys.argv[2], connections)
    elif sys.argv[1] == 'show':
        show(connections)
    elif sys.argv[1] == 'help':
        help()
    else:
        print('Неверная команда')
