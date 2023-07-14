class MyCustomException(Exception):
    def __init__(self, message="Default error message"):
        super().__init__(message)
        self.variable = variable


def example_function(num):
    try:
        if num < 0:
            raise MyCustomException()
        else:
            return num
    except MyCustomException as e:
        print(f"Caught a custom exception: {e}")


example_function(-1)
