# UNIVERSIDADE FEDERAL DO RIO GRANDE DO NORTE
# DEPARTAMENTO DE ENGENHARIA DE COMPUTACAO E AUTOMACAO
# DISCIPLINA REDES DE COMPUTADORES (DCA0113)
# AUTOR: PROF. CARLOS M D VIEGAS (viegas 'at' dca.ufrn.br)
#
# SCRIPT: Cliente de sockets TCP modificado para enviar texto minusculo ao servidor e aguardar resposta em maiuscula
#

# importacao das bibliotecas
from socket import *
import threading
import sys

# definicao das variaveis
serverName = '192.168.0.17' # ip do servidor
serverPort = 12000 # porta a se conectar
clientSocket = socket(AF_INET,SOCK_STREAM) # criacao do socket TCP
clientSocket.connect((serverName, serverPort)) # conecta o socket ao servidor

sentence = input('Digite o seu nome de usuario: ')
clientSocket.send(sentence.encode('utf-8')) # envia o texto para o servidor

#montando cabeçalho
tamMSG = ''
destNOME = 'server'
meuIP = '192.168.0.17'
destIP = '192.168.0.17'
comando = ''
dado = ''

def recebe():
    while True:
        msg = clientSocket.recv(1024).decode('utf-8')  # recebe do servidor a resposta
        #print(msg)
        msg = msg.split('|')
        #print(msg)
        tamMSG = msg[0]
        #destNOME = msg[3]
        meuIP = msg[1]
        destIP = msg[2]
        comando = msg[4]
        dado = msg[5]
        print(dado)
        if dado == 'Voce saiu do chat!':
            clientSocket.close() # encerramento do socket do cliente
            break

t = threading.Thread(target=recebe)
t.start()

while True:
    sentence = input('');
    sentence = sentence.split('(')
    #print(sentence)
    comando = sentence[0]
    if comando == 'nome' and len(sentence) > 1:
        sentence = sentence[1].split(')')
        if(len(sentence) > 1):
            #print(sentence)
            if sentence[1] == '' and sentence[0] != '':
                dado = sentence[0]
                msg = meuIP + '|' + destIP + '|' + destNOME + '|' + comando + '|' + dado
                tamMSG = len(msg)
                tamMSG = tamMSG + 1 + len(str(tamMSG))
                if len(dado) > 320:
                    print('Texto muito grande')
                else:
                    msg = str(tamMSG) + '|' + msg
                    #print(msg)
                    clientSocket.send(msg.encode('utf-8'))  # envia o texto para o servidor
            else:
                print('Comando invalido!')
        else:
            print('Comando invalido!')
    elif comando == 'lista' and len(sentence) > 1:
        sentence = sentence[1].split(')')
        if (len(sentence) > 1):
            #print(sentence)
            if sentence[1] == '':
                dado = sentence[0]
                msg = meuIP + '|' + destIP + '|' + destNOME + '|' + comando + '|' + dado
                tamMSG = len(msg)
                tamMSG = tamMSG + 1 + len(str(tamMSG))
                if dado != '':
                    print('Comando inválido')
                else:
                    msg = str(tamMSG) + '|' + msg
                    clientSocket.send(msg.encode('utf-8'))  # envia o texto para o servidor
            else:
                print('Comando invalido!')
        else:
            print('Comando invalido!')
    elif comando == 'sair' and len(sentence) > 1:
        sentence = sentence[1].split(')')
        if (len(sentence) > 1):
            #print(sentence)
            if sentence[1] == '':
                dado = sentence[0]
                msg = meuIP + '|' + destIP + '|' + destNOME + '|' + comando + '|' + dado
                tamMSG = len(msg)
                tamMSG = tamMSG + 1 + len(str(tamMSG))
                if dado != '':
                    print('Comando inválido')
                else:
                    msg = str(tamMSG) + '|' + msg
                    clientSocket.send(msg.encode('utf-8'))  # envia o texto para o servidor
                    break
            else:
                print('Comando invalido!')
        else:
            print('Comando invalido!')
    elif comando == 'privado' and len(sentence) > 1:
        teste = sentence
        sentence = sentence[1].split(')')
        if (len(sentence) > 1):
            #print(sentence)
            if sentence[1] != '' and sentence[0] != '':
                dado = teste[1]
                msg = meuIP + '|' + destIP + '|' + destNOME + '|' + comando + '|' + dado
                tamMSG = len(msg)
                tamMSG = tamMSG + 1 + len(str(tamMSG))
                if len(dado) > 320:
                    print('Texto muito grande')
                else:
                    msg = str(tamMSG) + '|' + msg
                    #print(msg)
                    clientSocket.send(msg.encode('utf-8'))  # envia o texto para o servidor
            else:
                print('Comando invalido!')
        else:
            print('Comando invalido!')
    else:
        dado = sentence[0]
        comando = 'null'
        msg = meuIP + '|' + destIP + '|' + destNOME + '|' + comando + '|' + dado
        tamMSG = len(msg)
        tamMSG = tamMSG + 1 + len(str(tamMSG))
        #print(len(dado))
        if len(dado) > 320:
            print('Texto muito grande')
        else:
            msg = str(tamMSG) + '|' + msg
            clientSocket.send(msg.encode('utf-8'))  # envia o texto para o servidor