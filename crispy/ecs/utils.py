import inspect

NULL = object()


def required_num_of_args(func):
    sig = inspect.signature(func)
    params = sig.parameters
    req = [p for p in params if params[p].default is params[p].empty]
    return len(req)

