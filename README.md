# Analisis Data Kebakaran DKI Jakarta

## Deskripsi Proyek

Proyek ini bertujuan untuk menganalisis data kebakaran di DKI Jakarta menggunakan berbagai teknik analisis data dan visualisasi. Dataset yang digunakan mencakup informasi kejadian kebakaran dari berbagai sumber dan periode waktu. Analisis ini meliputi distribusi jenis kejadian bencana, kerugian berdasarkan wilayah, tren kerugian, dan berbagai visualisasi lainnya untuk memberikan wawasan mendalam tentang kebakaran di DKI Jakarta.

## Dataset

Dataset yang digunakan dalam proyek ini adalah:

- **`informum_df`**: Data kejadian bencana
  - **`tanggal`**: Tanggal kejadian
  - **`jenis_kejadian_bencana`**: Jenis bencana
  - **`keterangan_jkb`**: Keterangan tambahan

- **`inforlokpak_df`**: Data lokasi dan kerugian
  - **`sumber_informasi`**: Sumber informasi
  - **`alamat_kejadian`**: Alamat kejadian
  - **`kelurahan`**: Kelurahan
  - **`kecamatan`**: Kecamatan
  - **`wilayah`**: Wilayah
  - **`kerugian_jumlah_kk`**: Jumlah kerugian (dalam KK)
  - **`taksiran_kerugian`**: Takaran kerugian
  - **`periode_data`**: Periode data

## Fitur

- **Distribusi Jenis Kejadian Bencana**: Menampilkan distribusi berbagai jenis kejadian bencana.
- **Kerugian Berdasarkan Wilayah**: Menampilkan kerugian berdasarkan wilayah di DKI Jakarta.
- **Tren Kerugian dari Bulan ke Bulan**: Visualisasi tren kerugian per bulan.
- **Top 5 Bulan dengan Kerugian Terbanyak**: Menampilkan 5 bulan dengan kerugian terbesar.
- **Kerugian Berdasarkan Jenis Kejadian Bencana**: Kerugian berdasarkan jenis bencana.
- **Distribusi Log Taksiran Kerugian**: Distribusi taksiran kerugian dengan log.
- **Jumlah Kejadian Kebakaran per Bulan**: Menampilkan jumlah kejadian kebakaran per bulan.
- **10 Top Wilayah dengan Jumlah Kejadian Terbanyak**: Menampilkan 10 wilayah dengan kejadian terbanyak.
- **Kecamatan dengan Jumlah Kejadian Terbanyak**: Menampilkan kecamatan dengan kejadian terbanyak.

## Prerequisites

- Python 3.x
- Streamlit
- Pandas
- Matplotlib
- Seaborn

## Instalasi

1. Clone repository ini:
   ```bash
   git clone https://github.com/username/repository-name.git
   cd repository-name

2. Install dependencies:
    ```bash
    pip install -r requirements.txt

3. Jalankan aplikasi Streamlit:
    ```bash
    streamlit run app.py