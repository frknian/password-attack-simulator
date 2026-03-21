import itertools
import time

def brute_force(target_password, charset):
    password_length = len(target_password)
    start_time = time.time()
    attempts = 0

    for guess_tuple in itertools.product(charset, repeat=password_length):
        guess = ''.join(guess_tuple)
        attempts += 1

        if attempts % 10000 == 0:
         print(f"Deneme: {attempts:,} | Geçen süre: {time.time() - start_time:.2f}s")


        if guess == target_password:
            break 

    end_time = time.time()
    elapsed_time = end_time - start_time

    attempts_per_second = attempts / elapsed_time if elapsed_time > 0 else float('inf')

    return {
         "password": target_password,
         "attempts": attempts,
         "time": round(elapsed_time, 4),
         "attempts_per_second": round(attempts_per_second, 2),
         "charset_size": len(charset),       # ← math_analysis için
         "password_length": password_length  # ← math_analysis için}
    }