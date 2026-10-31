# Proyek Analisis Data: Bike Sharing Dataset

Proyek analisis data dan pembuatan dashboard interaktif menggunakan dataset **Capital Bikeshare** (Washington D.C., periode 2011-2012) untuk memenuhi submission tugas akhir Dicoding: Belajar Analisis Data dengan Python.


##  Cara Menjalankan Dashboard di Local

### 1. Buat dan Aktifkan Virtual Environment (Opsional tapi Direkomendasikan)

**Di Windows (PowerShell/Command Prompt):**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**Di macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Instal Seluruh Dependensi

Jalankan perintah berikut:
```bash
pip install -r requirements.txt
```

### 3. Jalankan Aplikasi Streamlit

Dari root direktori submission, jalankan:
```bash
streamlit run dashboard/dashboard.py
```
atau:
```bash
python -m streamlit run dashboard/dashboard.py
```

Dashboard akan otomatis terbuka di browser pada alamat default `http://localhost:8501`.