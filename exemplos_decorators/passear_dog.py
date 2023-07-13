class DogClass:
    """Classe só pra debugar os métodos e decoradores no Python Terminal."""

    def __init__(self, dogname):
        self.dogname = dogname
        self.authorized_users = ["Alice", "Bob", "Charlie"]

    def check_authorization(self, funcwalk_dog=None):
        """Espera uma função como argumento."""

        def funcwrapper(walkername, *args, **kwargs):
            """Envolve nossa funcao decorada `walk_dog`"""
            print("Checando permissão para o cachorro: ", self.dogname)
            print(f"Wrapper => unnamed args/argumentos posicionais: {args}")
            print(f"Wrapper => keyword args/argumentos nomeados: {kwargs}")
            print(f"Wrapper => argumento posicional normal: {walkername}")
            return funcwalk_dog(*args, **kwargs)

        # Executar a função aninhada
        if funcwalk_dog is not None:
            # Se não for fornecida uma função decorada, retornar o próprio decorator
            return funcwrapper
        else:
            return "Decorador."

    # Executar o Decorador, e dentro do Decorador, executa o wrapper....
    @check_authorization
    def walk_dog(self, walkername):
        """Expects a Dog's Walker Name as a parameter."""
        print(f"{walkername} is Walking {self.dogname}")
