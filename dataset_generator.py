import string
import csv
import os
from math_analysis import calculate_crack_time
 
CHARSETS = {
    "Sadece rakam":        string.digits,
    "Küçük harf":          string.ascii_lowercase,
    "Büyük + küçük harf":  string.ascii_letters,
    "Harf + rakam":        string.ascii_letters + string.digits,
    "Tam set":             string.ascii_letters + string.digits + string.punctuation,
}
 
PASSWORD_LENGTHS = [4, 6, 8, 10, 12, 16]
ATTEMPTS_PER_SEC = 1_000_000
 
 
def load_common_passwords(file_path="common_passwords.txt"):
    with open(file_path, "r", encoding="utf-8") as f:
        passwords = [line.strip() for line in f]
    return passwords
 
 
def estimate_dictionary_attack_time(target, common_passwords, attempts_per_second):
    if target in common_passwords:
        index = common_passwords.index(target) + 1      # kaçıncı sırada
        time_seconds = index / attempts_per_second
        return time_seconds
    return None
 
 
def generate_dataset(output_file="dataset.csv"):
    common_passwords = load_common_passwords()
    rows = []
 
    for length in PASSWORD_LENGTHS:
        for charset_name, charset in CHARSETS.items():
            result = calculate_crack_time(
                charset_size=len(charset),
                password_length=length,
                attempts_per_second=ATTEMPTS_PER_SEC
            )
 
            # demo için örnek parola
            test_password = "password"
 
            dict_time = estimate_dictionary_attack_time(
                test_password,
                common_passwords,
                ATTEMPTS_PER_SEC
            )
 
            rows.append({
                "password_length":        length,
                "charset_name":           charset_name,
                "charset_size":           len(charset),
                "total_combinations":     result["total_combinations"],
                "avg_seconds":            result["avg_seconds"],
                "avg_formatted":          result["avg_formatted"],
                "worst_seconds":          result["worst_seconds"],
                "worst_formatted":        result["worst_formatted"],
                "attempts_per_second":    ATTEMPTS_PER_SEC,
                "is_common_password":     test_password in common_passwords,   # ← YENİ
                "dictionary_attack_time": dict_time,                           # ← YENİ
            })
 
    output_path = os.path.join(os.path.dirname(__file__), output_file)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
 
    print(f"{len(rows)} satır oluşturuldu → {output_file}")
    return rows