from functools import wraps, partial
import time


def sleep(func=None, *, seconds=None, msg=None):
    if func is None:
        return partial(sleep, seconds=seconds, msg=msg)

    seconds = seconds if seconds else 1
    msg = msg if msg else 'Sleeping for {} seconds'.format(seconds)

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(msg)
        time.sleep(seconds)
        return func(*args, **kwargs)
    return wrapper


if __name__ == '__main__':
    @sleep
    def hello():
        print('hello world')

    for _ in range(3):
        hello()
