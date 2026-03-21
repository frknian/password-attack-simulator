import math

# --- Yardımcı: süre formatlama ---
def format_time(seconds):
    if seconds < 1:
        return f"{seconds:.4f} saniye"
    elif seconds < 60:
        return f"{seconds:.2f} saniye"
    elif seconds < 3600:
        return f"{seconds / 60:.2f} dakika"
    elif seconds < 86400:
        return f"{seconds / 3600:.2f} saat"
    elif seconds < 31536000:
        return f"{seconds / 86400:.2f} gün"
    elif seconds < 31536000 * 1_000:
        return f"{seconds / 31536000:.2f} yıl"
    elif seconds < 31536000 * 1_000_000:
        return f"{seconds / 31536000 / 1_000:.2f} bin yıl"
    else:
        return f"{seconds / 31536000 / 1_000_000:.2f} milyon yıl"


# --- Toplam kombinasyon sayısı: C^L ---
def calculate_combinations(charset_size, password_length):
    return charset_size ** password_length


# --- Teorik kırılma süresi (ortalama = toplam / 2 / hız) ---
def calculate_crack_time(charset_size, password_length, attempts_per_second):
    total = calculate_combinations(charset_size, password_length)
    avg_seconds = total / 2 / attempts_per_second
    return {
        "total_combinations": total,
        "avg_seconds": avg_seconds,
        "avg_formatted": format_time(avg_seconds),
        "worst_seconds": total / attempts_per_second,
        "worst_formatted": format_time(total / attempts_per_second)
    }


# --- Karakter seti karşılaştırma tablosu ---
CHARSETS = {
    "Sadece rakam":         10,
    "Küçük harf":           26,
    "Büyük + küçük harf":   52,
    "Harf + rakam":         62,
    "Tam set (semboller)":  95,
}

def comparison_table(password_length, attempts_per_second=1_000_000):
    print(f"\n{'Karakter Seti':<25} {'Boyut':>6} {'Kombinasyon':>18} {'Ort. Kırılma Süresi':>20}")
    print("-" * 72)
    for name, size in CHARSETS.items():
        result = calculate_crack_time(size, password_length, attempts_per_second)
        combos = f"{result['total_combinations']:,}"
        print(f"{name:<25} {size:>6} {combos:>18} {result['avg_formatted']:>20}")


# --- Gerçek vs Teorik karşılaştırma (brute_force.py çıktısıyla) ---
def compare_real_vs_theory(bf_result, attempts_per_second):
    charset_size    = bf_result["charset_size"]
    password_length = bf_result["password_length"]

    theory = calculate_crack_time(charset_size, password_length, attempts_per_second)

    print("\n=== Gerçek vs Teorik Karşılaştırma ===")
    print(f"Parola            : {bf_result['password']}")
    print(f"Gerçek deneme     : {bf_result['attempts']:,}")
    print(f"Teorik ort. deneme: {theory['total_combinations'] // 2:,}")
    print(f"Gerçek süre       : {format_time(bf_result['time'])}")
    print(f"Teorik ort. süre  : {theory['avg_formatted']}")
    print(f"Gerçek hız        : {bf_result['attempts_per_second']:,.0f} deneme/sn")