# -*- coding: utf-8 -*-
import socket
import os

def get_response(request):
    headlines = request.split('\r')
    first_headline = headlines[0].split(' ')
    url = first_headline[1]
    way = url.split('/')
    del way[0]
    way.append('')
    if way[0] == '':
        for line in headlines:
            if line.find('User-Agent') != -1:
                return 'Hello mister! \nYou are:' + line
    if way[0] == 'test':
        return request
    if way[0] == 'media':
        if way[1] == '':
            files = os.listdir('../files')
            file_names = ''
            for file in files:
                file_names = file_names + file + '\n'
            return file_names
        try:
            file = open('../files/' + way[1])
        except:
            return 'File not found'
        return file.read()
    return 'Page not found'

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 8000))  # назначение хоста и порта для сервера
server_socket.listen(0)  # запуск режима прослушивания для данного сокета
                         # аргумент метода - размер очереди на входящие соединения

print "Started"

while 1:
    try:
        (client_socket, address) = server_socket.accept()
        print 'Got new client', client_socket.getsockname()  # вывод IP клиента, подключившегося к серверу
        request_string = client_socket.recv(2048)  # получение данных от клиента
        client_socket.send(get_response(request_string))  # отправка данных в сокет
        client_socket.close()
    except KeyboardInterrupt:  # остановка сервера
        print 'Stopped'
        server_socket.close()  # закрытие сокета
        exit()
