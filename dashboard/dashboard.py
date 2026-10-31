import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)

# Pengaturan gaya Seaborn & Matplotlib
sns.set_theme(style="whitegrid")
plt.rcParams["font.sans-serif"] = "DejaVu Sans"

# Fungsi untuk memuat data
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    main_csv_path = os.path.join(current_dir, "main_data.csv")
    
    # Fallback jika dijalankan dari root direktori
    if not os.path.exists(main_csv_path):
        main_csv_path = "dashboard/main_data.csv"
        
    df = pd.read_csv(main_csv_path)
    df["dteday"] = pd.to_datetime(df["dteday"])
    return df

df = load_data()

# ----------------- SIDEBAR: FILTER -----------------
st.sidebar.header("🚲 Filter Analisis")

# 1. Filter Rentang Tanggal
min_date = df["dteday"].min().date()
max_date = df["dteday"].max().date()

date_range = st.sidebar.date_input(
    label="Pilih Rentang Tanggal",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date)
)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

# 2. Filter Musim
all_seasons = sorted(df["season_label"].unique().tolist())
selected_seasons = st.sidebar.multiselect(
    label="Pilih Musim",
    options=all_seasons,
    default=all_seasons
)

# 3. Filter Kondisi Cuaca
all_weathers = sorted(df["weather_label"].unique().tolist())
selected_weathers = st.sidebar.multiselect(
    label="Pilih Kondisi Cuaca",
    options=all_weathers,
    default=all_weathers
)

# 4. Filter Tipe Hari
day_type_options = ["Semua", "Working Day", "Weekend / Holiday"]
selected_day_type = st.sidebar.selectbox(
    label="Tipe Hari",
    options=day_type_options,
    index=0
)

# Penerapan Filter ke DataFrame
filtered_df = df[
    (df["dteday"].dt.date >= start_date) &
    (df["dteday"].dt.date <= end_date) &
    (df["season_label"].isin(selected_seasons)) &
    (df["weather_label"].isin(selected_weathers))
]

if selected_day_type != "Semua":
    filtered_df = filtered_df[filtered_df["day_type"] == selected_day_type]

# ----------------- HEADER DASHBOARD -----------------
st.title("🚲 Bike Sharing Analytics Dashboard")
st.markdown("Visualisasi interaktif analisis data peminjaman sepeda (*Capital Bikeshare System*, Washington D.C., 2011-2012) untuk mendukung pengambilan keputusan bisnis operasional.")

with st.expander("📌 Lihat Rumusan Pertanyaan Bisnis (SMART Framework)"):
    st.markdown("""
    1. **Pertanyaan 1:** Bagaimana variasi rata-rata jumlah penyewaan sepeda per hari berdasarkan kondisi cuaca (*weathersit*) dan musim (*season*) sepanjang tahun 2011 hingga 2012, sebagai dasar perencanaan alokasi unit sepeda dan jadwal pemeliharaan rutin armada?
    2. **Pertanyaan 2:** Bagaimana perbandingan rata-rata jumlah peminjaman sepeda per jam (*hourly*) antara hari kerja (*working day*) dan hari libur/akhir pekan (*weekend/holiday*) untuk pengguna kasual (*casual*) vs pengguna terdaftar (*registered*) sepanjang tahun 2011 hingga 2012, sebagai dasar pengaturan jadwal *re-balancing* armada dan strategi promosi keanggotaan?
    """)

if filtered_df.empty:
    st.warning("⚠️ Tidak ada data yang sesuai dengan filter yang dipilih. Silakan sesuaikan filter pada sidebar.")
    st.stop()

# ----------------- RINGKASAN METRIK UTAMA -----------------
total_rentals = filtered_df["cnt"].sum()
total_registered = filtered_df["registered"].sum()
total_casual = filtered_df["casual"].sum()
pct_registered = (total_registered / total_rentals * 100) if total_rentals > 0 else 0
pct_casual = (total_casual / total_rentals * 100) if total_rentals > 0 else 0

daily_df = filtered_df.groupby("dteday")[["cnt", "casual", "registered", "temp_celsius"]].agg({
    "cnt": "sum",
    "casual": "sum",
    "registered": "sum",
    "temp_celsius": "mean"
}).reset_index()

avg_daily_rentals = int(daily_df["cnt"].mean()) if not daily_df.empty else 0

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Total Peminjaman", value=f"{total_rentals:,} unit")
with col2:
    st.metric(label="Pengguna Terdaftar", value=f"{total_registered:,} ({pct_registered:.1f}%)")
with col3:
    st.metric(label="Pengguna Kasual", value=f"{total_casual:,} ({pct_casual:.1f}%)")
with col4:
    st.metric(label="Rata-rata Harian", value=f"{avg_daily_rentals:,} unit/hari")

st.markdown("---")

# ----------------- TAB TAMPILAN -----------------
tab1, tab2, tab3 = st.tabs([
    "🌦️ Musim & Cuaca (Pertanyaan 1)",
    "⏰ Pola Jam & Hari Kerja (Pertanyaan 2)",
    "📊 Analisis Lanjutan (Klaster Permintaan)"
])

# ----- TAB 1: PENGARUH MUSIM & CUACA -----
with tab1:
    st.subheader("Variasi Rata-rata Peminjaman per Hari Berdasarkan Cuaca & Musim (2011-2012)")
    st.caption("Dasar analisis untuk perencanaan alokasi unit sepeda dan penjadwalan pemeliharaan armada.")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("**Rata-rata Peminjaman Harian Berdasarkan Musim**")
        daily_season = filtered_df.groupby(["dteday", "season_label"], observed=True)["cnt"].sum().reset_index()
        season_avg = daily_season.groupby("season_label", observed=True)["cnt"].mean().reset_index()
        
        if not season_avg.empty:
            max_val = season_avg["cnt"].max()
            colors = ["#1565C0" if val == max_val else "#90CAF9" for val in season_avg["cnt"]]
            
            fig, ax = plt.subplots(figsize=(7, 4.5))
            bars = ax.bar(season_avg["season_label"], season_avg["cnt"], color=colors, edgecolor="black", linewidth=0.8)
            ax.set_ylabel("Rata-rata Rental (Unit/Hari)")
            ax.set_ylim(0, max_val * 1.25)
            for bar in bars:
                h = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2, h + (max_val * 0.02), f"{int(h):,}", ha="center", va="bottom", fontweight="bold")
            st.pyplot(fig)
            plt.close(fig)
        else:
            st.info("Data musim tidak tersedia.")

    with col_b:
        st.markdown("**Rata-rata Peminjaman Harian Berdasarkan Kondisi Cuaca**")
        daily_weather = filtered_df.groupby(["dteday", "weather_label"], observed=True)["cnt"].sum().reset_index()
        weather_avg = daily_weather.groupby("weather_label", observed=True)["cnt"].mean().reset_index()
        
        if not weather_avg.empty:
            fig, ax = plt.subplots(figsize=(7, 4.5))
            colors = ["#2E7D32", "#81C784", "#E57373", "#D32F2F"][:len(weather_avg)]
            bars = ax.bar(weather_avg["weather_label"], weather_avg["cnt"], color=colors, edgecolor="black", linewidth=0.8)
            ax.set_ylabel("Rata-rata Rental (Unit/Hari)")
            max_w = weather_avg["cnt"].max()
            ax.set_ylim(0, max_w * 1.25)
            plt.xticks(rotation=15, ha="right")
            for bar in bars:
                h = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2, h + (max_w * 0.02), f"{int(h):,}", ha="center", va="bottom", fontweight="bold")
            st.pyplot(fig)
            plt.close(fig)
        else:
            st.info("Data cuaca tidak tersedia.")
            
    st.info("💡 **Keputusan Bisnis & Insight:** Peminjaman sepeda tertinggi terjadi pada Musim Gugur (*Fall*: 5.644 unit/hari) dan kondisi cuaca cerah (*Clear*: 4.877 unit/hari). Cuaca buruk hujan/salju menurunkan sewa hingga tersisa 1.803 unit/hari. **Rekomendasi:** Alokasikan 100% armada pada musim gugur/panas cerah, dan jadwalkan perawatan unit berkala pada musim semi atau saat cuaca hujan/salju.")

# ----- TAB 2: POLA JAM & TIPE PENGGUNA -----
with tab2:
    st.subheader("Perbandingan Rata-rata Peminjaman per Jam: Hari Kerja vs Libur (2011-2012)")
    st.caption("Dasar analisis untuk pengaturan jadwal re-balancing armada dan strategi promosi keanggotaan.")
    
    hourly_agg = filtered_df.groupby(["day_type", "hr"], observed=True)[["casual", "registered", "cnt"]].mean().reset_index()
    
    col_w1, col_w2 = st.columns(2)
    
    # Plot Hari Kerja
    with col_w1:
        st.markdown("**Hari Kerja (Working Day)**")
        wd_data = hourly_agg[hourly_agg["day_type"] == "Working Day"]
        if not wd_data.empty:
            fig, ax = plt.subplots(figsize=(7.5, 4.5))
            ax.plot(wd_data["hr"], wd_data["registered"], marker="o", color="#1565C0", label="Registered (Komuter)", linewidth=2)
            ax.plot(wd_data["hr"], wd_data["casual"], marker="s", color="#FF8F00", label="Casual (Kasual)", linewidth=2)
            ax.set_title("Pola Jam di Hari Kerja", fontsize=11, fontweight="bold")
            ax.set_xlabel("Jam (0 - 23)")
            ax.set_ylabel("Rata-rata Rental (Unit/Jam)")
            ax.set_xticks(range(0, 24, 2))
            ax.axvspan(7, 9, color="#BBDEFB", alpha=0.3, label="Rush Hour Pagi")
            ax.axvspan(16, 19, color="#BBDEFB", alpha=0.5, label="Rush Hour Sore")
            ax.legend(loc="upper left")
            st.pyplot(fig)
            plt.close(fig)
        else:
            st.info("Data Hari Kerja tidak ada pada filter saat ini.")

    # Plot Akhir Pekan / Libur
    with col_w2:
        st.markdown("**Akhir Pekan / Hari Libur (Weekend / Holiday)**")
        nwd_data = hourly_agg[hourly_agg["day_type"] == "Weekend / Holiday"]
        if not nwd_data.empty:
            fig, ax = plt.subplots(figsize=(7.5, 4.5))
            ax.plot(nwd_data["hr"], nwd_data["registered"], marker="o", color="#1565C0", label="Registered (Komuter)", linewidth=2)
            ax.plot(nwd_data["hr"], nwd_data["casual"], marker="s", color="#FF8F00", label="Casual (Kasual)", linewidth=2)
            ax.set_title("Pola Jam di Akhir Pekan / Libur", fontsize=11, fontweight="bold")
            ax.set_xlabel("Jam (0 - 23)")
            ax.set_ylabel("Rata-rata Rental (Unit/Jam)")
            ax.set_xticks(range(0, 24, 2))
            ax.axvspan(11, 16, color="#FFE082", alpha=0.35, label="Peak Rekreasi Siang")
            ax.legend(loc="upper left")
            st.pyplot(fig)
            plt.close(fig)
        else:
            st.info("Data Akhir Pekan tidak ada pada filter saat ini.")
            
    st.info("💡 **Keputusan Bisnis & Insight:** Hari kerja memiliki dua jam sibuk komuter tajam (pukul 08:00 dan 17:00-18:00) yang didominasi pengguna terdaftar (>85%). Akhir pekan didominasi aktivitas santai siang-sore (12:00-16:00) dengan lonjakan sewa kasual (>300%). **Rekomendasi:** Lakukan re-balancing armada sebelum pukul 07:30 dan 16:30 di hari kerja, serta jalankan promosi paket keanggotaan bagi pengguna kasual di taman rekreasi saat akhir pekan.")

# ----- TAB 3: ANALISIS LANJUTAN (KLASTERING) -----
with tab3:
    st.subheader("Analisis Lanjutan: Klastering Tingkat Permintaan Rental Harian")
    st.caption("Pengelompokan hari operasional ke dalam klaster Low, Medium, dan High Demand berdasarkan kuartil rental harian.")
    
    daily_cluster = filtered_df.groupby(["dteday", "demand_category"], observed=True).agg({
        "cnt": "sum",
        "registered": "sum",
        "casual": "sum",
        "temp_celsius": "mean"
    }).reset_index()
    
    cluster_summary = daily_cluster.groupby("demand_category", observed=True).agg(
        Jumlah_Hari=("cnt", "count"),
        Rata_rata_Rental=("cnt", "mean"),
        Rata_rata_Suhu=("temp_celsius", "mean"),
        Total_Registered=("registered", "sum"),
        Total_Rental=("cnt", "sum")
    ).reset_index()
    
    cluster_summary["Pct_Registered"] = (cluster_summary["Total_Registered"] / cluster_summary["Total_Rental"] * 100).round(1)
    
    col_c1, col_c2 = st.columns(2)
    
    with col_c1:
        st.markdown("**Distribusi Frekuensi Hari per Klaster Permintaan**")
        fig, ax = plt.subplots(figsize=(6, 4))
        colors_pie = ["#90CAF9", "#42A5F5", "#1565C0"]
        ax.pie(
            cluster_summary["Jumlah_Hari"],
            labels=cluster_summary["demand_category"],
            autopct="%1.1f%%",
            startangle=140,
            colors=colors_pie,
            wedgeprops={"edgecolor": "white", "linewidth": 1.5}
        )
        ax.axis("equal")
        st.pyplot(fig)
        plt.close(fig)
        
    with col_c2:
        st.markdown("**Karakteristik Suhu Rata-rata per Klaster**")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(
            data=cluster_summary,
            x="demand_category",
            y="Rata_rata_Suhu",
            hue="demand_category",
            palette="Blues_d",
            legend=False,
            ax=ax
        )
        ax.set_ylabel("Suhu Rata-rata (°C)")
        ax.set_xlabel("Klaster Permintaan")
        for p in ax.patches:
            ax.annotate(f"{p.get_height():.1f} °C", (p.get_x() + p.get_width() / 2., p.get_height() / 2), ha="center", va="center", color="white", fontweight="bold")
        st.pyplot(fig)
        plt.close(fig)
        
    st.markdown("##### Tabel Rangkuman Klaster")
    st.dataframe(
        cluster_summary[["demand_category", "Jumlah_Hari", "Rata_rata_Rental", "Rata_rata_Suhu", "Pct_Registered"]].rename(
            columns={
                "demand_category": "Kategori Permintaan",
                "Jumlah_Hari": "Jumlah Hari",
                "Rata_rata_Rental": "Rata-rata Rental (Unit)",
                "Rata_rata_Suhu": "Suhu Rata-rata (°C)",
                "Pct_Registered": "Proporsi Registered (%)"
            }
        ),
        use_container_width=True
    )
    
    st.info("💡 **Insight Operasional:** Hari-hari klaster High Demand memiliki suhu hangat (~23.5°C) dengan rata-rata peminjaman > 6.800 unit/hari. Ketika suhu turun di bawah 15°C atau saat cuaca buruk, permintaan turun ke kategori Low Demand.")

# ----------------- FOOTER -----------------
st.markdown("---")
st.caption("Proyek Analisis Data Dicoding | Dataset: Capital Bikeshare System (2011-2012)")
