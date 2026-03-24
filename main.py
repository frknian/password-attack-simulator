import string
from brute_force import brute_force
from math_analysis import comparison_table, compare_real_vs_theory
from dataset_generator import generate_dataset, load_common_passwords, estimate_dictionary_attack_time
from visualizer import plot_all

CHARSETS = {
    "1": ("Sadece rakam",        string.digits),
    "2": ("Küçük harf",          string.ascii_lowercase),
    "3": ("Büyük + küçük harf",  string.ascii_letters),
    "4": ("Harf + rakam",        string.ascii_letters + string.digits),
    "5": ("Tam set",             string.ascii_letters + string.digits + string.punctuation),
}

def main():
    print("=" * 55)
    print("   BRUTE FORCE PAROLA GÜVENLİK ANALİZİ")
    print("=" * 55)

    print("\n[1] Brute force testi başlat")
    print("[2] Teorik veri seti oluştur (dataset.csv)")
    mode = input("\nMod seçin (1/2): ").strip()

    if mode == "2":
        generate_dataset()
        return

    # --- Mod 1: Brute force testi ---
    target = input("\nTest edilecek parola: ").strip()
    if not target:
        print("Parola boş olamaz.")
        return

    # --- Dictionary attack kontrolü ---
    common_passwords = load_common_passwords()
    dict_time = estimate_dictionary_attack_time(target, common_passwords, 1_000_000)

    if dict_time is not None:
        print("\n⚠️  Bu parola yaygın bir parola!")
        print(f"Dictionary attack süresi: {dict_time:.6f} saniye\n")
        return                                        # ← yaygın parola, devam ettirme
    else:
        print("\nBu parola common listede bulunamadı.\n")

    # --- Karakter seti seç ---
    print("\nKarakter seti seçin:")
    for key, (name, _) in CHARSETS.items():
        print(f"  {key}. {name}")

    choice = input("\nSeçim (1-5): ").strip()
    if choice not in CHARSETS:
        print("Geçersiz seçim.")
        return

    charset_name, charset = CHARSETS[choice]
    print(f"\nSeçilen set : {charset_name} ({len(charset)} karakter)")

    estimated = len(charset) ** len(target)
    if estimated > 10_000_000:
        print(f"Uyarı: {estimated:,} kombinasyon — bu işlem uzun sürebilir.")
        confirm = input("Devam etmek istiyor musunuz? (e/h): ").strip().lower()
        if confirm != "e":
            print("İptal edildi.")
            return

    # --- Brute force çalıştır ---
    print(f"\nBrute force başlatılıyor: '{target}'")
    print("-" * 40)

    result = brute_force(target, charset)
    result["charset_size"]    = len(charset)
    result["password_length"] = len(target)

    print(f"\nParola bulundu  : {result['password']}")
    print(f"Toplam deneme   : {result['attempts']:,}")
    print(f"Geçen süre      : {result['time']} sn")
    print(f"Hız             : {result['attempts_per_second']:,.0f} deneme/sn")

    compare_real_vs_theory(result, result["attempts_per_second"])

    print(f"\n--- {len(target)} karakterli parola için tüm karakter setleri ---")
    comparison_table(len(target), result["attempts_per_second"])

    print("\n" + "=" * 55)

if __name__ == "__main__":
    main()

from visualizer import plot_crack_time