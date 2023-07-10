import paramiko

from time import sleep
from rich import inspect  # https://rich.readthedocs.io/en/stable/reference/init.html#rich.inspect


class RemoteClient:
    """This class represents the client to Interact with using SSH.
    It has attributes related to the remote host being connected and the state of the SSH connection."""

    def __init__(self, remote_host: str, login: str, password: str):
        # Init my objet with the att above.
        self.remote_host = remote_host
        self.login = login
        self.password = password

        # My host will have one object of a "Paramiko SSHClient" type
        self.ssh_client = None  # Fix Variable Before Assignment Warning.

    def __str__(self):
        return f"Host => {self.remote_host} \nSessão SSH => {self.ssh_client}"

    @property
    def conexaossh(self):
        try:
            # Try to connect and handle errors - Instantiating an object of the class, not a local object.
            self.ssh_client = paramiko.SSHClient()  # Self instantiates the object, not local.

            # Known_host Policy
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # Try for 1 second.
            self.ssh_client.connect(self.remote_host, username=self.login, password=self.password, timeout=1)

            return f"Sessão do SSH adicionada com sucesso ao Host. \n{self}"
        except paramiko.ssh_exception.SSHException as ssh_exception:
            return f"SSHException - Failed to connect to the host: {ssh_exception}"
        except TimeoutError as timeout_error:
            return f"TimeoutError - Host unavailable: {timeout_error}"

    # Check if SSH Connection is open
    def isconnected(self):
        """This method will return False if it is not connected, True otherwise."""
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

    def disconnect(self):
        # Use the object attribute that represents the connection state to disconnect.
        if self.ssh_client is not None:
            self.ssh_client.close()
            return "Disconnected from SSH!"
        else:
            return "No active SSH connection."

    def to_dict(self):
        ssh_info = "No active SSH connection"
        if self.isconnected():
            ssh_info = "SSH session is active"

        return {
            'remote_host': self.remote_host,
            'login': self.login,
            'ssh_connection': ssh_info,
            # Outros atributos relevantes...
        }


# This is Commented out for Logging/Debugging and Testing Part
# print("Testing SSH Connection.")
#
# # Connect
host = RemoteClient("172.16.107.9", 'administrator', '200JJ@#Admin1984')
host.connect()
host.connect()

#
# # Check if it remains connected
# print(host.isconnected())
#
# sleep(3)

# Disconnects and see if it remains connected
# host.disconnect()
# print(host.isconnected())

# Python Terminal - Debug Example.
# import paramiko
# ssh_client = paramiko.SSHClient()
# ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh_client.connect("172.16.107.9", username="administrator", password="200JJ@#Admin1984")
# inspect(ssh_client, methods=True)
