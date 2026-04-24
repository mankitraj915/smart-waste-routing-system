import time

def time_it(func, *args, **kwargs):
    """
    Executes a function and measures its execution time.

    Args:
        func (callable): The function to execute.
        *args: Variable length argument list for the function.
        **kwargs: Arbitrary keyword arguments for the function.

    Returns:
        tuple: A tuple containing:
            - Any: The precise return value of the executed function.
            - float: The total execution time in seconds.
    """
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    return result, end_time - start_time
