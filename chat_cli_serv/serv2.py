# UNIVERSIDADE FEDERAL DO RIO GRANDE DO NORTE
# DEPARTAMENTO DE ENGENHARIA DE COMPUTACAO E AUTOMACAO
# DISCIPLINA REDES DE COMPUTADORES (DCA0113)
# AUTOR: PROF. CARLOS M D VIEGAS (viegas 'at' dca.ufrn.br)
#
# SCRIPT: Servidor de sockets TCP modificado para receber texto minusculo do cliente enviar resposta em maiuscula
#

# importacao das bibliotecas
from socket import * # sockets
import threading  # threads
global listaNomes
import time
listaNomes = {} #os que ja tem login no chat

def enviamsg(list, adress, var2, var3, var4, var5, var6): #tamMSG, meuIP, destIP, destNOME, comando, dado
    msg = var2 + '|' + var3 + '|' + var4 + '|' + var5 + '|' + var6
    var1 = len(msg)
    var1 = var1 + 1 + len(str(var1))
    msg = str(var1) + '|' + msg
    #print(msg)
    list[adress].send(bytes(msg, 'utf-8'))

#funcao padrao que ira ser chamada na thread
def recebe(socketClient, address):
    meuIP = '192.168.0.17'
    sentence = socketClient.recv(1024) #espera receber mensagens
    nome = str(sentence) #recebe o nome de usuario
    nome = nome.split("'")
    nome = nome[1]
    listaNomes[address] = nome #o IP ira enderecar os users
    #for index in listaNomes:
        #print('<' + str(nome) + ', ' + str(index[0]) + ', ' + str(index[1]) + '>') #exibe <nome, ip, porta>
    for index in listaNomes: #envia a mensagem que o user entrou no chat, exceto para ele
        if listaNomes[index] != nome:
            sentence = nome + ' entrou no chat...'  # forma a mensagem de login
            msg = str(sentence)
            enviamsg(listaSockets, index, meuIP, index[0], listaNomes[index], 'null', msg)
        else: #envia mensagem diferenciada pro user que entrou
            sentence = "Voce entrou no chat como '" + nome + "' ... \n"
            msg = str(sentence)
            enviamsg(listaSockets, address, meuIP, index[0], nome, 'null', msg)
    print(nome + ' entrou no chat...' )
    ##########################
    #       FUNFA ATÉ AQ     #
    ##########################
    while 1:
        msg = str(socketClient.recv(1024))  # espera receber mensagens
        #print('entrou')
        #print(msg)
        msg = msg.split('|')
        #print(msg)
        tamMSG = msg[0].split("'")
        tamMSG = tamMSG[1]
        destNOME = msg[3]
        meuIP = msg[1]
        destIP = msg[2]
        comando = msg[4]
        dado = msg[5].split("'")
        dado = dado[0]
        #print(dado)
        aux = 0
        ##########################
        #       MUDAR NOME       #
        ##########################
        if comando == 'nome':
            for index in listaSockets:
                if listaNomes[index] == dado:
                    aux = aux+1
            if aux == 0:
                #print(aux)
                sentence = nome + ' agora eh ' + dado
                listaNomes[address] = dado #atualizando o nome na lista
                nome = dado
                #print(listaNomes)
                broad(listaSockets, sentence, nome)
            else:
                msg = 'Nome de usuario ja utilizado!'
                enviamsg(listaSockets, address, meuIP, address[0], listaNomes[address], 'null', msg)
        ##########################
        #         LISTAR         #
        ##########################
        elif comando == 'lista':
            msg = ""
            for index in listaNomes:
                auxnome = listaNomes[index]
                msg = msg + '<' + str(auxnome) + ', ' + str(index[0]) + ', ' + str(index[1]) + '>\n'  # exibe <nome, ip, porta>
            msg = str(msg)
            enviamsg(listaSockets, address, meuIP, address[0], listaNomes[address], 'null', msg)
        ##########################
        #          SAIR          #
        ##########################
        elif comando == 'sair':
            msg = 'Voce saiu do chat!'
            enviamsg(listaSockets, address, meuIP, address[0], listaNomes[address], 'null', msg)
            del listaNomes[address]
            sentence = nome + ' saiu!'
            del listaSockets[address]
            broad(listaSockets, sentence, nome)
            break
        elif comando == 'privado':
            dado = dado.split(')')
            for index in listaSockets:
                if listaNomes[index] == dado[0]:
                    aux = aux+1
            if aux >= 1:
                msg = nome + ' disse: ' + dado[1]
                #print(msg)
                for index in listaSockets:
                    if listaNomes[index] == dado[0]:
                        enviamsg(listaSockets, index, meuIP, index[0], listaNomes[index], 'null', msg)
                        break
            else:
                msg = 'Nome de usuario inexistente!'
                enviamsg(listaSockets, address, meuIP, address[0], listaNomes[address], 'null', msg)
        elif comando == 'null':
            broad(listaSockets, dado, nome)

##########################
#        MSG P TDS       #
##########################
def broad(list, msg, nome):
    meuIP = '192.168.0.17'
    print(nome + ' disse: ' + msg)
    for index in list:
        sentence = meuIP + '|' + index[0] + '|' + listaNomes[index] + '|' + 'null' + '|' + nome + ' disse: ' + msg
        aux = len(sentence)
        aux = aux + 1 + len(str(aux))
        sentence = str(aux) + '|' + sentence
        #print(sentence)
        list[index].send(bytes(sentence, 'utf-8'))

def envia():
    while 1:
        cmd = input('')
        if cmd == 'lista()':
            msg = ""
            for index in listaNomes:
                auxnome = listaNomes[index]
                msg = msg + '<' + str(auxnome) + ', ' + str(index[0]) + ', ' + str(index[1]) + '>\n'  # exibe <nome, ip, porta>
            print(msg)
##########################
#         INICIO         #
##########################
listaSockets = {} #todos que estão no geral
serverName = '' # ip do servidor (em branco)
serverPort = 12000 # porta a se conectar
serverSocket = socket(AF_INET,SOCK_STREAM) # criacao do socket TCP
serverSocket.bind((serverName,serverPort)) # bind do ip do servidor com a porta
serverSocket.listen(1) # socket pronto para 'ouvir' conexoes
print ('Chat iniciado na porta %d ...' % (serverPort))

cmd_thread = threading.Thread(target=envia)
cmd_thread.start()

while True:
    connectionSocket, addr = serverSocket.accept()
    listaSockets[addr] = connectionSocket
    cli_thread = threading.Thread(target=recebe, args=(connectionSocket, addr))
    cli_thread.start()
    '''
    connectionSocket, addr = serverSocket.accept() # aceita as conexoes dos clientes
    sentence = connectionSocket.recv(1024) # recebe dados do cliente
    sentence = sentence.decode('utf-8')
    capitalizedSentence = sentence.upper() # converte em letras maiusculas
    print ('Cliente %s enviou: %s, transformando em: %s' % (addr, sentence, capitalizedSentence))
    connectionSocket.send(capitalizedSentence.encode('utf-8')) # envia para o cliente o texto transformado
    connectionSocket.close() # encerra o socket com o cliente
    serverSocket.close() # encerra o socket do servidor
    '''