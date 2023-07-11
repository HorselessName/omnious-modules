import json
import paramiko


class RemoteClient:
    """This class represents the client to Interact with using SSH.
    It has attributes related to the remote host being connected and the state of the SSH connection.

    Sintax:  host = RemoteClient("192.168.1.1", 'administrator', 'SuperDuperP4ss#23')
    """

    def __init__(self, remote_host: str, login: str, password: str):
        # Init my objet with the att above.
        self.remote_host = remote_host
        self.login = login
        self.password = password

        # My host will have one object of a "Paramiko SSHClient" type
        self.ssh_client = None  # Fix Variable Before Assignment Warning.
        self.transport_ssh = None  # The Transport of SSH for Lower Level stuff.

    def __str__(self):
        return f"Host => {self.remote_host} \nSessão SSH => {self.ssh_client}"

    def establishssh(self):
        try:
            if not self.isconnected():
                # Try to connect and handle errors - Instantiating an object of the class, not a local object.
                self.ssh_client = paramiko.SSHClient()  # Self instantiates the object, not local.

                # Known_host Policy
                self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                # Try for 1 second.
                self.ssh_client.connect(self.remote_host, username=self.login, password=self.password, timeout=1)

                # Save Transport reference for later use when doing low level stuff.
                self.transport_ssh = self.ssh_client.get_transport()

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
            return "SSH disconnected"
        else:
            return "SSH was alredy disconnected"

    @property
    def atributos(self):
        if self.isconnected():
            ssh_connection = "SSH session is active"
        else:
            ssh_connection = "No active SSH connection"

        classe_dict = {
            "remote_host": f"{self.remote_host}",
            "login": f"{self.login}",
            "ssh_connection": f"{ssh_connection}",
            # Outros atributos relevantes...
        }

        return json.dumps(classe_dict)

