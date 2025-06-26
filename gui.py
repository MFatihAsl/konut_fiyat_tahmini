import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Model ve veri yükleniyor
model = joblib.load("XGBoost_model.pkl")
df = pd.read_excel("temizVeri_Bursa.xlsx")

# İlçe - Mahalle sözlüğü
ilce_mahalle_dict = df.groupby("İlçe")["Mahalle"].unique().apply(list).to_dict()

# Sayfa ayarları
st.set_page_config(page_title="🏡 Konut Fiyat Tahmini", layout="centered")
st.title("🏡 Konut Fiyat Tahmin Uygulaması")

# İlçe seçimi
ilce = st.selectbox("İlçe", sorted(ilce_mahalle_dict.keys()), key="ilce_secimi")

# Dinamik mahalle listesi
mahalle_secenekleri = sorted(ilce_mahalle_dict.get(ilce, []))
mahalle = st.selectbox("Mahalle", mahalle_secenekleri, key="mahalle_secimi")

# --- GİRİŞ FORMU ---
with st.form("tahmin_form"):
    col1, col2 = st.columns(2)

    with col1:
        net_m2 = st.number_input("Net m²", min_value=10, max_value=1000, value=100)
        brut_m2 = st.number_input("Brüt m²", min_value=10, max_value=1200, value=120)
        kat_sayisi = st.number_input("Kat (Sayı)", min_value=0, max_value=50, value=3)
        toplam_kat = st.number_input("Toplam Kat", min_value=1, max_value=50, value=5)
        bina_yasi = st.number_input("Bina Yaşı", min_value=0, max_value=100, value=10)

    with col2:
        oda = st.selectbox("Oda Sayısı", options=[0, 1, 2, 3, 4, 5, 6], index=2)
        salon = st.selectbox("Salon Sayısı", options=[0, 1, 2, 3], index=1)
        isitma = st.selectbox("Isıtma Tipi", options=sorted(df["Isıtma Tipi"].unique()))
        site = st.selectbox("Site İçinde mi?", options=sorted(df["Site İçinde mi?"].unique()))

    submitted = st.form_submit_button("Tahmini Hesapla")

# --- TAHMİN ---
if submitted:
    kullanici_verisi = pd.DataFrame({
        "Isıtma Tipi": [isitma],
        "İlçe": [ilce],
        "Mahalle": [mahalle],
        "Site İçinde mi?": [site],
        "Net m2": [net_m2],
        "Brüt m2": [brut_m2],
        "Toplam Kat": [toplam_kat],
        "Kat (Sayı)": [kat_sayisi],
        "Oda": [oda],
        "Salon": [salon],
        "Bina Yaşı": [bina_yasi],
        "Kullanim_Orani": [net_m2 / brut_m2],
        "Bina_Yasi_Log": [np.log1p(bina_yasi)],
        "Kat_Orani": [kat_sayisi / toplam_kat if toplam_kat else 0],
        "Toplam_Oda_Salon": [oda + salon],
        "m2_basi_fiyat": [35581.88]  # Ortalama değer
    })

    fiyat_log_tahmin = model.predict(kullanici_verisi)[0]
    fiyat_tahmin = np.expm1(fiyat_log_tahmin)

    if fiyat_tahmin < 1_000_000:
        st.warning("⚠️ Tahmin edilen fiyat düşük olabilir.")

    st.success(f"🏷️ Tahmini Satış Fiyatı: {fiyat_tahmin:,.0f} TL")
    st.caption("Not: Bu tahmin, eğitim verisiyle sınırlı istatistiksel bir öngörüdür.")
