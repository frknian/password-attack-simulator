import pandas as pd
import matplotlib.pyplot as plt


def plot_crack_time(csv_file="dataset.csv"):
    df = pd.read_csv(csv_file)

    plt.figure(figsize=(8, 5))

    for charset in df["charset_name"].unique():
        subset = df[df["charset_name"] == charset]
        plt.plot(subset["password_length"], subset["avg_seconds"], marker='o', label=charset)

    plt.xlabel("Parola Uzunluğu")
    plt.ylabel("Kırılma Süresi (saniye)")
    plt.title("Parola Uzunluğu vs Kırılma Süresi")
    plt.yscale("log")
    plt.legend()
    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()


def plot_charset_comparison(csv_file="dataset.csv"):
    df = pd.read_csv(csv_file)

    plt.figure(figsize=(10, 6))

    for charset_name, group in df.groupby("charset_name"):
        plt.plot(
            group["password_length"],
            group["avg_seconds"],
            marker='o',
            linewidth=2,
            label=charset_name
        )

    plt.xlabel("Parola Uzunluğu")
    plt.ylabel("Ort. Kırılma Süresi (saniye)")
    plt.title("Karakter Seti Karşılaştırması")
    plt.yscale("log")
    plt.legend()
    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()


def plot_combinations_bar(csv_file="dataset.csv", password_length=8):
    df = pd.read_csv(csv_file)
    df = df[df["password_length"] == password_length]

    plt.figure(figsize=(9, 5))
    plt.bar(
        df["charset_name"],
        df["total_combinations"],
        color="steelblue",
        edgecolor="white"
    )
    plt.xlabel("Karakter Seti")
    plt.ylabel("Toplam Kombinasyon")
    plt.title(f"{password_length} Karakterli Parola — Kombinasyon Sayısı")
    plt.yscale("log")
    plt.xticks(rotation=15, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()


def plot_all(csv_file="dataset.csv"):
    print("Grafik 1: Parola uzunluğu vs kırılma süresi")
    plot_crack_time(csv_file)

    print("Grafik 2: Karakter seti karşılaştırması")
    plot_charset_comparison(csv_file)

    print("Grafik 3: Kombinasyon sayısı bar chart")
    plot_combinations_bar(csv_file)


# ← plot_all DIŞINDA, dosyanın en altında
if __name__ == "__main__":
    plot_all()