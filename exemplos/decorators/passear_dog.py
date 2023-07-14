class DogClass(object):
    """Classe só pra debugar os métodos e decoradores no Python Terminal."""

    def __init__(self, dogname):
        self.dogname = dogname
        self.authorized_users = ["Alice", "Bob", "Charlie"]

    # noinspection PyMethodParameters
    def check_authorization(func):
        """Decorador: Chamado ao executar o arquivo.
        Wrapper: É executado condicionalmente pelo método decorado."""

        def funcwrapper(*args, **kwargs):
            """Envolve nossa funcao decorada, herdada do decorador."""
            print(f"Wrapper => Function do Decorador: {func} ")
            print(f"Wrapper => unnamed args/argumentos posicionais: {args}")
            print(f"Wrapper => keyword args/argumentos nomeados: {kwargs}")

            # noinspection PyCallingNonCallable
            return func(*args, **kwargs)

        # Executar a função aninhada
        return funcwrapper

    # Executar o Decorador, e dentro do Decorador, executa o wrapper....
    # noinspection PyArgumentList
    @check_authorization
    def walk_dog(self, walkersname):
        """Expects a Dog's Walker Name as a parameter."""
        print(f"{walkersname} is Walking {self.dogname}")


dog = DogClass("Max")
dog.walk_dog("Alice")
