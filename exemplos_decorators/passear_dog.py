class DogClass:
    """Classe só pra debugar os métodos e decoradores no Python Terminal."""

    def __init__(self, dogname):
        self.dogname = dogname
        self.authorized_users = ["Alice", "Bob", "Charlie"]

    def check_authorization(self, func=None):
        """Espera uma função como argumento."""

        # Pro método não ser considerado estático, é só referenciar um atributo da classe.
        print("Checando permissão para os usuários: ", self.dogname)

        def funcwrapper(walkername, *args, **kwargs):
            """Envolve nossa funcao decorada `walk_dog`"""
            print(f"Wrapper => unnamed args/argumentos posicionais: {args}")
            print(f"Wrapper => keyword args/argumentos nomeados: {kwargs}")
            print(f"Wrapper => argumento posicional normal: {walkername}")
            return True

        # Executar a função aninhada
        return funcwrapper if func else False

    # Executar o Decorador, e dentro do Decorador, executa o wrapper....
    @check_authorization
    def walk_dog(self, walkername):
        """Expects a Dog's Walker Name as a parameter."""
        print(f"{walkername} is Walking {self.dogname}")
