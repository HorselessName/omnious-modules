import json
import paramiko
from typing import Dict

# Time pra esperar e simular um await.
import time


# Define Python user-defined exceptions
class InvalidIPAddress(Exception):
    """Raised when the IPv4 is invalid."""
    def __init__(self, message="IPv4 Inválido."):
        # Call the base class constructor with the custom message
        super().__init__(message)


class ValidateIpAddress:
    @staticmethod
    def validipaddress(ipv4):
        """
        :param ipv4:
        :type ipv4: str
        :rtype: bool
        """

        def isipv4(number):
            try:
                return str(int(number)) == number and 0 <= int(number) <= 255
            except Exception:
                raise InvalidIPAddress

        if ipv4.count(".") == 3 and all(isipv4(i) for i in ipv4.split(".")):
            return True

        raise InvalidIPAddress


class RemoteClient:
    """This class represents the client to Interact with using SSH.
    It has attributes related to the remote host being connected and the state of the SSH connection.

    RFC: https://datatracker.ietf.org/doc/html/rfc4251
    RFC Explica sobre a estrutura do SSH, que é formado por três componentes principais:

    => User Authentication Protocol (Client)
    => Transport Layer Protocol (Transport)
    => Connection Protocol (Channel)

    Sintax:  host = RemoteClient("192.168.1.1", 'administrator', 'SuperDuperP4ss#23')

    The client is responsible for establishing the connection, authenticating, and interacting with the server.
    The transport is the intermediary that creates and do some management of the channels for data transport.
    The channel multiplexes and manages the encrypted tunnels and  logical channels.
    """

    def __init__(self, remote_host: str, login: str, password: str):
        try:
            if ValidateIpAddress.validipaddress(remote_host):
                self.remote_host = remote_host
            else:
                raise InvalidIPAddress()
        except InvalidIPAddress as e:
            print(f"Erro: {str(e)}")

        # Init my object with the atributes above.
        self.login = login
        self.password = password

        # My host will have one object of a "Paramiko SSHClient" type
        self.ssh_client = None  # Fix Variable Before Assignment Warning.

        # Ref. https://docs.paramiko.org/en/stable/api/transport.html
        self.ssh_transport = None  # The Transport of SSH for Lower Level stuff.
        self.ssh_channel = None

    def __str__(self):
        return f"Host => {self.remote_host} " \
               f"\nSessão SSH => {self.ssh_client}" \
               f"\nTransporte => {self.ssh_transport}" \
               f"\nChannel => {self.ssh_channel}"

    @staticmethod
    def esperar(segundos):
        t_end = time.time() + segundos
        while time.time() < t_end:
            pass

    # Check if SSH Connection is open before calling it.
    # noinspection PyMethodParameters
    def _decorator_isconnected(function):
        """Decorator must be applied on functiononly.
        It will only return the function if it is connected, otherwise will do nothing."""

        # The decorator is the wrapper that
        # noinspection PyCallingNonCallable
        def decowrapper(*args, **kwargs):
            # If there's not connection establish... Using recursive without args.
            if not args[0].isconnected():  # This checks the object method.
                # Handle the case when not connected to SSH
                print("Not connected to SSH. Connecting...")

                # Importante: Decoradores não recebem kwargs não especificados no método decorado!
                # Lista de Referencias:
                # "Data Science do Zero" => Página "34."
                # https://towardsdatascience.com/a-primer-on-args-kwargs-decorators-for-data-scientists-bb8129e756a7
                # https://www.pythontutorial.net/advanced-python/python-decorators
                return function(*args, **kwargs)  # Call the decorated function in the arguments
            else:
                return "We're connected to SSH already. Cool."

        return decowrapper

    def isconnected(self):
        """Check if it is connected."""
        # "Client" method get_transport() returns object "Transport".
        # Ref. https://docs.paramiko.org/en/stable/api/client.html
        if self.ssh_client is None or self.ssh_client.get_transport() is None:
            return False

        if self.ssh_client.get_transport().is_active():
            # The method is available in Transport docs => https://docs.paramiko.org/en/stable/api/transport.html
            # Double check for False Positives from is_active() method
            try:
                # Get Transport object status.
                transport = self.ssh_client.get_transport()
                transport.send_ignore()
                return True
            except EOFError as e:
                # If it hits here, there's been a false positive.
                return False

    # noinspection PyArgumentList
    @_decorator_isconnected
    def establishssh(self):
        try:
            # Try to connect and handle errors - Instantiating an object of the class, not a local object.
            self.ssh_client = paramiko.SSHClient()  # Self instantiates the object, not local.

            # Known_host Policy
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # Try for 1 second - Doc: https://docs.paramiko.org/en/stable/api/client.html
            self.ssh_client.connect(self.remote_host, username=self.login, password=self.password, timeout=1)

            # Save Transport reference for later use when doing low level stuff.
            self.ssh_transport = self.ssh_client.get_transport()

            print(f"Sessão do SSH adicionada com sucesso ao Host. " \
                  f"\n{self}")

            return f"Sessão do SSH adicionada com sucesso ao Host. " \
                   f"\n{self}"

        except paramiko.ssh_exception.SSHException as ssh_exception:
            return f"SSHException - Failed to connect to the host: {ssh_exception}"
        except TimeoutError as timeout_error:
            return f"TimeoutError - Host unavailable: {timeout_error}"

    def disconnect(self):
        # Use the object attribute that represents the connection state to disconnect.
        if self.ssh_client is not None:
            self.ssh_client.close()
            print("SSH disconnected")
            return "SSH disconnected"
        else:
            print("SSH was alredy disconnected")
            return "SSH was alredy disconnected"

    def createsession(self):
        """This will create a new Channel on Transport layer, in order for sending commands.
        Made this method for debugging and using on Python Terminal."""

        print("Creating Session... ", end="")
        if self.isconnected():
            self.ssh_channel = self.ssh_transport.open_session()
            print("Session created!")
            return "Session created!."
        else:
            print("No SSH Connection. Connecting...")
            self.establishssh()  # Estabeleço o SSH
            self.createsession()  # Tento criar a session novamente.
            return "No SSH Connection. Connecting..."

    def enviarcomandos(self, comandos: list):
        """ This will send commands to a session, and after completed, will end the current session.
            According to Channel docs at Ref. below, when executing a command, it closes the channel,
            so you must use stdin, stdout and stderr approach to use multiple commands.

            Sintaxe:    1. Criar a lista com os comandos.
                        2. Enviar com remoteclient.enviarcomandos(comandos)

            Ref. https://docs.paramiko.org/en/stable/api/channel.html#paramiko.channel.Channel.get_name"""
        contagem = 0
        try:
            # Crio a sessao pra enviar meus comandos.
            self.createsession()

            # Ref. https://docs.paramiko.org/en/stable/api/channel.html#paramiko.channel.Channel.settimeout
            self.ssh_channel.settimeout(1)  # Timeout for writing/sending bytes.

            # Espero um pouco antes de conectar conectar.
            while True:
                print(".", end="")
                self.esperar(100 / 1000)  # 100 Milisegundos
                contagem += 1

                if contagem == 5:
                    break

            print()

            # Entro no Channel que criamos anteriormente e envio os comandos.
            outputcomandos = []
            for command in comandos:
                print(f"{'#' * 5} Executing command : {command} {'#' * 5}")
                self.ssh_channel = self.ssh_transport.open_session()
                self.ssh_channel.exec_command(command)

                # https://docs.paramiko.org/en/stable/api/channel.html#paramiko.channel.Channel.recv_exit_status
                return_code = self.ssh_channel.recv_exit_status()  # Exit code from SSH Server.

                stdout = self.ssh_channel.makefile('rb').read()
                stderr = self.ssh_channel.makefile_stderr('rb').read()

                # Adicionar as informacoes do comando ao meu dict.
                comandoatual = {
                    "Comando": command,
                    "Codigo de Retorno": return_code,
                    "Output": stdout.decode(),
                    "Erro": stderr.decode()
                }

                outputcomandos.append(comandoatual)

            # Depois de executar meus comandos, fecho tudo
            self.ssh_client.close()

            print(f"Output: {outputcomandos}")
            return outputcomandos

        except Exception as e:
            print(f"Channel Send Commands Error => {e}")
            # If something bad happens.
            return False

    @property
    def atributos(self):
        if self.isconnected():
            ssh_connection = "SSH session is active"
            object_id = id(self)
            object_ref = hex(id(self))
        else:
            ssh_connection = "No active SSH connection"
            object_id = id(self)
            object_ref = hex(id(self))

        classe_dict = {
            "remote_host": f"{self.remote_host}",
            "login": f"{self.login}",
            "ssh_connection": f"{ssh_connection}",
            "object_id": f"{object_id}",
            "object_ref": f"{object_ref}"
            # Outros atributos relevantes...
        }

        return json.dumps(classe_dict)


# Importante: Se for usar a classe, precisa fazer o comando abaixo.
# remoteclients: Dict[str, RemoteClient] = {}
