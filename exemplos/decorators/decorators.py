import inspect


def decorador(funcaodecorada):
    """Espera uma função como argumento."""

    def wrapper(*args, **kwargs):
        """O Wrapper pega os argumentos passados na Funcao Decorada ao decorador.
        O Wrapper, pode levar argumentos arbitrários e nomeados, após isto, descompactá-los e usá-los.

        Exemplo:
            def exemplo(*args, **kwargs):
                print(f"Argumentos sem nome: {args}");
                print(f"Argumentos com nome: {kwargs}");

            exemplo(1, 2, nome="Raul", sobrenome="Chiarella")

        Ao executar esta funcao que aplica args e kwargs, o output vai ser:
        # Argumentos sem nome: (1, 2)
        # Argumentos com nome: {'nome': 'Raul', 'sobrenome': 'Chiarella'}

        """

        # Unnamed Args => Argumentos arbitrários, que não foram nomeados e que não foram especificados.
        print(f"Wrapper => unnamed args: {args}")

        # Keyword Args => Argumentos que tem nome
        print(f"Wrapper => keyword args: {kwargs}")
        print(f"Wrapper => Variáveis Individuais passadas explicitamente como argumentos: {'Nenhuma'}")

        # Executa a função decorada e encaminha os argumentos recebidos originalmente por ela.
        return funcaodecorada(*args, **kwargs)

        # Mind Tip: Pego a folha com os dados, e ao invés de apagar os dados eu só encaminho para a pessoa
        # que me enviou estes dados, do jeito que está, sem alterar nada.

    # Executa a função aninhada "wrapper" que por sua vez executa a função decorada.
    return wrapper


# O decorador não recebe parâmetros opcionais.
@decorador
def printar(nome, mensagem="Olá"):
    """Espera uma palavra como argumento."""
    print(f"{mensagem} {nome}")


def metodoexemplo(a, b, *args, c=10, d=20, **kwargs):
    print("Parâmetros obrigatórios:")
    print("a:", a)
    print("b:", b)
    print("Argumentos posicionais:")
    print("args:", args)
    print("Parâmetros opcionais:")
    print("c:", c)
    print("d:", d)
    print("Argumentos nomeados:")
    print("kwargs:", kwargs)


print(30 * "-")
printar("Raul Chiarella")
print(30 * "-")

metodoexemplo(1, 2, 3, 4, 5, c=30, e=40)
sig = inspect.signature(metodoexemplo)

print(30 * "-", 5 * "\n")

for name, param in sig.parameters.items():
    print(30 * "-")
    print(f"Nome do parâmetro: {name}")
    print(f"Padrão: {param.default}")
    print(f"É um parâmetro posicional? {param.kind == param.POSITIONAL_OR_KEYWORD}")
    print(f"É um parâmetro obrigatório? {param.default == param.empty}")
    print(30 * "-")
