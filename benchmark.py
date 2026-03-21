import time

def measure_attempt_speed():
    
    attempts = 1000000

    start_time = time.time()
    
    for i in range(attempts):
        pass

    end_time = time.time()

    elapsed_time = end_time - start_time

    attempts_per_second = attempts / elapsed_time if elapsed_time > 0 else float('inf') 
    
    return attempts_per_second