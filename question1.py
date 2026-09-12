# 	i. Bug 1: Unbound Local Error
# The error is cause by this line inside wrapper: 
# Calls = [t for t in calls if now – t < period] 

# This line gives unbound local error because Python treats calls as a local variable inside wrapper because the function assigns to calls. Python therefore interprets the code as: 

# def wrapper(*args, **kwargs): 
# 	# calls is considered local here 
# 	Calls = [t for t in calls if …]

# The right hand side calls is therefore being accessed before the local variable has been assigned, producing: 

# UnboundLocalError: local variable ‘calls’ refrenced before assignment 

# ii. Bug 2: State persistence across class instances 
# When the decorator is used on a class method, the rate-limit state should generally be associated with the decorated function, rather than with an individual object instance (self).
# Example: 
# class UserService: 
#        @rate_limit(3,10)
#         def fetch_user_data(self, user_id):
#         …

# If the implementation stores the state incorrectly on the instance, each object could get its own counter: 
# Service1.fetch_user_data(…)
# Service2.fetch_user_data(…)

# This allows more than the intended 3 calls per 10 seconds across the service as a whole. 

# The timestamp list should be maintained in the decorator`s closure, so all instances calling that decorated method share the same rate-limit state.
# Access to the shared list should be protected with a threading.Lock because the the decorator must also be thread safe.  

# iii. Refactored code: 

import time
import threading
from functools import wraps
from typing import Callable

def rate_limit(max_calls: int, period: int):
    if max_calls <= 0:
        raise ValueError("max_calls must be greater than 0")

    if period <= 0:
        raise ValueError("period must be greater than 0")

    def decorator(func):
        calls = []
        lock = threading.Lock()

        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.monotonic()

            with lock:
                # Remove timestamps outside the current window
                calls[:] = [
                    timestamp
                    for timestamp in calls
                    if now - timestamp < period
                ]

                if len(calls) >= max_calls:
                    raise Exception("Rate limit exceeded")

                calls.append(now)

            return func(*args, **kwargs)

        return wrapper

    return decorator






