import socket
from time import sleep
from typing import Dict
from rich import print

from flask import Flask, jsonify
from acessossh.host import RemoteClient

app = Flask(__name__)

# My Dict will contain a list of Objects of RemoteClient type - Something like ArrayList<RemoteClient>
remoteclients: Dict[str, RemoteClient] = {}

"""
Usando o Flask e nossa classe que representa uma conexão ao host pelo SSH, conseguimos instanciar e abrir
várias conexões de SSH no Host Remoto definido no objeto ao instanciar ele...

Conseguimos ter várias. Então, após abrir uma conexão pelo SSH, queremos enviar comandos remotos à esta
sessão, então, precisamos de uma forma de identificar para qual a sessão de SSH, ou seja, qual objeto que foi
instanciado, que representa essa conexão, que iremos chamar o método que envia o comando, exec_command.

Vídeo importante: https://youtu.be/AkcxJWbHV0w
Tem vários comentários que precisam ser corrigidos com relação ao Paramiko.

Outros videos:
https://www.youtube.com/playlist?list=PLOocymQm7YWYc73phqzbZ1S3ANrVVpUFN
Esse fala sobre enviar múltiplos comandos pra mesma sessão depois de já ter executado.

https://www.youtube.com/watch?v=xd1kI1eq5uw
Este fala sobre invocar uma shell e usar o send para enviar vários comandos.

"""


@app.route('/')
def conexaossh():
    """Rota que vai gerar nossa conexão SSH no cliente remoto."""
    try:
        hostname = "172.16.107.9"
        login = "administrator"
        password = "200JJ@#Admin1984"

        # Instanciar o objeto que é cliente remoto e adicionar à lista de objetos.
        remoteclients[hostname] = RemoteClient(hostname, login, password)

        # This is Commented out for Logging/Debugging and Testing Part
        print("Testing SSH Connection.")

        # Establish the SSH session on the host.
        response = remoteclients[hostname].conexaossh

        # Check if it remains connected - True if Connected.
        print(remoteclients[hostname].conexaossh)
        return f'Response [Request] => {response}'

    except socket.gaierror as erro_noresolveip:
        """Esse Except trata o erro [Errno 11001] getaddrinfo que ocorre quando o app não consegue resolver o
        IP do host informado. """
        print(f'Erro na resolução do IP [Console] => {erro_noresolveip}')
        return f'Erro na resolução do IP [Request] => {erro_noresolveip}'


@app.route("/listarobjetos")
def listarobjetos():
    # Converter cada objeto RemoteClient em um dicionário
    remoteclients_dict = {hostname: client.to_dict() for hostname, client in remoteclients.items()}

    # Retornar o dicionário de objetos como uma resposta JSON
    return jsonify(remoteclients_dict)


if __name__ == '__main__':
    # Por padrão o Flask vem com Threaded True, mas colocamos aqui pra melhor visibilidade.
    app.run(threaded=True)
