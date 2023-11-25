import functools
import sys
import os
import time

def redirect_print_to_log(log):
    def outer(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            stdout = sys.stdout
            stderr = sys.stderr

            flag = "a"

            if not os.path.exists(log):
                flag = 'w+'

            with open(log, flag) as f:
                sys.stdout = f
                sys.stderr = f

                print(f"[{time.time_ns()}]\n")

                func(*args, **kwargs)
            sys.stdout = stdout
            sys.stderr = stderr

        return inner
    return outer


        
    