import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from math_analysis import calculate_crack_time, format_time
from dataset_generator import load_common_passwords, estimate_dictionary_attack_time

st.set_page_config(
    page_title="Brute Force Analizi",
    page_icon="🔐",
    layout="centered"
)

st.title("🔐 Brute Force Parola Güvenlik Analizi")
st.markdown("---")

# ============================================================
# Kullanıcı girişi
# ============================================================
charset_options = {
    "Sadece rakam":        10,
    "Küçük harf":          26,
    "Büyük + küçük harf":  52,
    "Harf + rakam":        62,
    "Tam set (semboller)": 95,
}

charset_name = st.selectbox("Karakter seti seç", options=list(charset_options.keys()))
charset_size = charset_options[charset_name]

password_input = st.text_input("Parolayı gir", placeholder="örn: abc123")

attempts_per_second = st.selectbox(
    "Saldırı hızı",
    options=[1_000, 1_000_000, 1_000_000_000, 1_000_000_000_000],
    format_func=lambda x: f"{x:,} deneme/sn",
    index=1
)

analiz_btn = st.button("Analiz Et")

# ============================================================
# Sonuçlar — sadece butona basınca göster
# ============================================================
if analiz_btn and password_input:

    password_length = len(password_input)
    result = calculate_crack_time(charset_size, password_length, attempts_per_second)

    st.markdown("---")

    # Metrik kartları
    col1, col2, col3 = st.columns(3)
    col1.metric("Kombinasyon",      f"{result['total_combinations']:,}")
    col2.metric("Ort. Kırılma",     result["avg_formatted"])
    col3.metric("En Kötü Durum",    result["worst_formatted"])

    st.markdown("---")

    # Dictionary attack kontrolü
    try:
        common_passwords = load_common_passwords()
        dict_time = estimate_dictionary_attack_time(
            password_input, common_passwords, attempts_per_second
        )
        if dict_time is not None:
            st.error(f"⚠️ Yaygın parola listesinde! Kırılma: {dict_time:.6f} saniye")
        else:
            st.success("✅ Yaygın listede bulunamadı.")
    except FileNotFoundError:
        st.warning("common_passwords.txt bulunamadı.")

    st.markdown("---")

    # Grafik
    df = pd.read_csv("dataset.csv")
    df_filtered = df[df["charset_name"] == charset_name]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(
        df_filtered["password_length"],
        df_filtered["avg_seconds"],
        marker='o',
        linewidth=2,
        color="steelblue",
        label=charset_name
    )
    ax.axvline(
        x=password_length,
        color="red",
        linestyle="--",
        linewidth=1.5,
        label=f"Girilen uzunluk: {password_length}"
    )
    ax.set_xlabel("Parola Uzunluğu")
    ax.set_ylabel("Kırılma Süresi (saniye)")
    ax.set_yscale("log")
    ax.legend()
    ax.grid(True, which="both", linestyle="--", alpha=0.4)
    plt.tight_layout()
    st.pyplot(fig)

elif analiz_btn and not password_input:
    st.warning("Lütfen bir parola gir.")