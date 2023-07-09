import socket
from time import sleep

from flask import Flask
from acessossh.host import Host

app = Flask(__name__)

# Toda vez que iniciar o Flask, minha lista de objetos do tipo Host, inicia vazia.
hosts = {}

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
def conectarnohost():
    try:
        hostname = "172.16.107.9"
        login = "administrator"
        password = "200JJ@#Admin1984"

        # Instanciar o objeto da conexão SSH
        ssh_client = Host(hostname, login, password)

        # This is Commented out for Logging/Debugging and Testing Part
        print("Testing SSH Connection.")

        # Connect
        response = ssh_client.connect()

        # Check if it remains connected - True if Connected.
        print(ssh_client.isconnected())
        return f'Response [Request] => {response}'

    except socket.gaierror as erro_noresolveip:
        """Esse Except trata o erro [Errno 11001] getaddrinfo que ocorre quando o app não consegue resolver o
        IP do host informado. """
        print(f'Erro na resolução do IP [Console] => {erro_noresolveip}')
        return f'Erro na resolução do IP [Request] => {erro_noresolveip}'


if __name__ == '__main__':
    # Por padrão o Flask vem com Threaded True, mas colocamos aqui pra melhor visibilidade.
    app.run(threaded=True)
