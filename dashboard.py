# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import streamlit as st

# # Set style for seaborn plots
# sns.set(style='dark')

# # Helper functions for data processing
# def create_monthly_fires_df(df):
#     monthly_fires_df = df.resample(rule='M', on='tanggal').size().reset_index(name='total_fires')
#     return monthly_fires_df

# def create_fires_by_location_df(df):
#     fires_by_location_df = df['kecamatan'].value_counts().reset_index()
#     fires_by_location_df.columns = ['kecamatan', 'total_fires']
#     return fires_by_location_df

# def create_fires_by_cause_df(df):
#     fires_by_cause_df = df['jenis_kejadian_bencana'].value_counts().reset_index()
#     fires_by_cause_df.columns = ['jenis_kejadian_bencana', 'total_fires']
#     return fires_by_cause_df

# def create_fires_by_month_df(df):
#     df['bulan'] = df['tanggal'].dt.month
#     fires_by_month_df = df.groupby('bulan').size().reset_index(name='total_fires')
#     return fires_by_month_df

# # Load dataset
# df = pd.read_csv("./dataset/ready_kebakaran-jakarta2018.csv")

# # Convert columns to datetime
# df['tanggal'] = pd.to_datetime(df['tanggal'])

# # Sort values by date
# df.sort_values(by="tanggal", inplace=True)
# df.reset_index(drop=True, inplace=True)

# # Streamlit sidebar for date range filter
# min_date = df['tanggal'].min()
# max_date = df['tanggal'].max()

# with st.sidebar:
#     st.image("./asset/damkar.png")  # Replace with your company's logo URL
    
#     start_date, end_date = st.date_input(
#         label='Rentang Waktu', min_value=min_date,
#         max_value=max_date,
#         value=[min_date, max_date]
#     )

# # Filter data based on selected date range
# filtered_df = df[(df['tanggal'] >= pd.to_datetime(start_date)) & 
#                  (df['tanggal'] <= pd.to_datetime(end_date))]

# # Prepare dataframes for visualization
# monthly_fires_df = create_monthly_fires_df(filtered_df)
# fires_by_location_df = create_fires_by_location_df(filtered_df)
# fires_by_cause_df = create_fires_by_cause_df(filtered_df)
# fires_by_month_df = create_fires_by_month_df(filtered_df)

# # Dashboard content
# st.header('Dashboard Kejadian Kebakaran DKI Jakarta :fire:')

# # Plot kejadian kebakaran per bulan
# st.subheader('Kejadian Kebakaran Per Bulan')

# fig, ax = plt.subplots(figsize=(16, 8))
# ax.plot(
#     monthly_fires_df['tanggal'],
#     monthly_fires_df['total_fires'],
#     marker='o', 
#     linewidth=2,
#     color="#FF6F61"
# )
# ax.set_xlabel('Tanggal')
# ax.set_ylabel('Jumlah Kebakaran')
# ax.set_title('Jumlah Kebakaran per Bulan')
# st.pyplot(fig)

# # Plot lokasi kebakaran terbanyak
# st.subheader("Lokasi Terbanyak Terjadi Kebakaran")

# fig, ax = plt.subplots(figsize=(12, 10))
# sns.barplot(x='total_fires', y='kecamatan', data=fires_by_location_df, palette='viridis', ax=ax)
# ax.set_xlabel('Jumlah Kebakaran')
# ax.set_title('Jumlah Kebakaran berdasarkan Lokasi')
# st.pyplot(fig)

# # Plot penyebab kebakaran
# st.subheader("Jenis Kejadian Bencana")

# fig, ax = plt.subplots(figsize=(12, 10))
# sns.barplot(x='total_fires', y='jenis_kejadian_bencana', data=fires_by_cause_df, palette='magma', ax=ax)
# ax.set_xlabel('Jumlah Kebakaran')
# ax.set_title('Jumlah Kebakaran berdasarkan Penyebab')
# st.pyplot(fig)

# # Plot distribusi kebakaran per bulan
# st.subheader("Distribusi Kebakaran per Bulan")

# fig, ax = plt.subplots(figsize=(12, 8))
# sns.barplot(x='bulan', y='total_fires', data=fires_by_month_df, palette='coolwarm', ax=ax)
# ax.set_xlabel('Bulan')
# ax.set_ylabel('Jumlah Kebakaran')
# ax.set_title('Distribusi Kebakaran per Bulan')
# ax.set_xticks(range(0, 12))
# ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
# st.pyplot(fig)

# # Footer
# st.caption('Copyright © 2024 Benzodiahmad')

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set style for seaborn plots
sns.set(style='darkgrid')

# Helper functions for data processing
def create_monthly_disasters_df(df):
    df.set_index('tanggal', inplace=True)
    monthly_disasters_df = df.resample('M').size().reset_index(name='total_disasters')
    return monthly_disasters_df

def create_disasters_by_location_df(df, top_n=15):
    disasters_by_location_df = df['kecamatan'].value_counts().reset_index()
    disasters_by_location_df.columns = ['kecamatan', 'total_disasters']
    top_disasters_by_location_df = disasters_by_location_df.head(top_n)
    return top_disasters_by_location_df

def create_disasters_by_type_df(df):
    disasters_by_type_df = df['jenis_kejadian_bencana'].value_counts().reset_index()
    disasters_by_type_df.columns = ['jenis_kejadian_bencana', 'total_disasters']
    return disasters_by_type_df

def create_disasters_by_period_df(df):
    df['periode'] = pd.to_datetime(df['periode_data']).dt.to_period('M')
    disasters_by_period_df = df.groupby('periode').size().reset_index(name='total_disasters')
    return disasters_by_period_df

def calculate_aggregated_metrics(df):
    metrics_df = df.groupby(by="kelurahan").agg({
        "kerugian_jumlah_kk": ["max", "min", "mean", "std"],
        "taksiran_kerugian": ["max", "min", "mean", "std"]
    })
    return metrics_df

def filter_by_month(df, month_year):
    df['tanggal'] = df['tanggal'].astype(str)
    return df[df['tanggal'].str.startswith(month_year)]

def group_by_kecamatan(df):
    grouped = df.groupby(by=['kecamatan']).size().reset_index(name='count')
    return grouped

def calculate_statistics(df):
    rata_kerugian = df['kerugian_jumlah_kk'].mean()
    rata_korban = df['taksiran_kerugian'].mean()
    return rata_kerugian, rata_korban

def calculate_correlation(df):
    return df[['kerugian_jumlah_kk', 'taksiran_kerugian']].corr().iloc[0, 1]

# Load dataset
df = pd.read_csv("./dataset/readytouse-kebakaran-dkijakarta2018.csv")

bulan_terpilih = "Agustus 2024"  # Contoh bulan yang difilter

# Convert columns to datetime
df['tanggal'] = pd.to_datetime(df['tanggal'])
df['periode_data'] = pd.to_datetime(df['periode_data'])

# Sort values by date
df.sort_values(by="tanggal", inplace=True)
df.reset_index(drop=True, inplace=True)

# Streamlit sidebar for date range filter
min_date = df['tanggal'].min()
max_date = df['tanggal'].max()

with st.sidebar:
    st.image("./asset/damkar.png")  # Replace with your company's logo URL
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter data based on selected date range
filtered_df = df[(df['tanggal'] >= pd.to_datetime(start_date)) & 
                 (df['tanggal'] <= pd.to_datetime(end_date))]

# Prepare dataframes for visualization
monthly_disasters_df = create_monthly_disasters_df(filtered_df)
disasters_by_location_df = create_disasters_by_location_df(filtered_df)
disasters_by_type_df = create_disasters_by_type_df(filtered_df)
disasters_by_period_df = create_disasters_by_period_df(filtered_df)
metrics_df = calculate_aggregated_metrics(filtered_df)

# Filter data for January 2018
kebakaran_januari_2018 = filter_by_month(df, '2018-01')

# Mengelompokkan data berdasarkan 'bulan' dan 'kecamatan'
grouped = group_by_kecamatan(kebakaran_januari_2018)
most_common_kecamatan = grouped.loc[grouped['count'].idxmax()]

# Calculate statistics
rata_kerugian, rata_korban = calculate_statistics(df)
korelasi = calculate_correlation(df)

# Format nilai sebagai mata uang Rupiah
formatted_rata_kerugian = f"Rp {rata_kerugian:,.0f}"
formatted_rata_korban = f"Rp {rata_korban:,.0f}"

# Dashboard content
st.header('Dashboard Kejadian Bencana DKI Jakarta :fire:')

# Plot kejadian bencana per bulan
st.subheader('Kejadian Bencana Per Bulan')

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    monthly_disasters_df['tanggal'],
    monthly_disasters_df['total_disasters'],
    marker='o', 
    linewidth=2,
    color="#FF6F61"
)
ax.set_xlabel('Tanggal')
ax.set_ylabel('Jumlah Kejadian Bencana')
ax.set_title('Jumlah Kejadian Bencana per Bulan')
st.pyplot(fig)

# Plot lokasi kejadian bencana terbanyak (15 teratas)
st.subheader("Kecamatan Terbanyak Terjadi Kejadian Bencana")

fig, ax = plt.subplots(figsize=(12, 10))
top_disasters_by_location_df = create_disasters_by_location_df(filtered_df, top_n=15)
sns.barplot(x='total_disasters', y='kecamatan', data=top_disasters_by_location_df, palette='viridis', ax=ax)
ax.set_xlabel('Jumlah Kejadian Bencana')
ax.set_title('Jumlah Kejadian Bencana berdasarkan Kecamatan (15 Terbanyak)')
st.pyplot(fig)

# Plot jenis kejadian bencana
st.subheader("Jenis Kejadian Bencana")

fig, ax = plt.subplots(figsize=(12, 10))
sns.barplot(x='total_disasters', y='jenis_kejadian_bencana', data=disasters_by_type_df, palette='magma', ax=ax)
ax.set_xlabel('Jumlah Kejadian Bencana')
ax.set_title('Jumlah Kejadian Bencana berdasarkan Jenis')
st.pyplot(fig)

# Plot distribusi kejadian bencana per periode
st.subheader("Distribusi Kejadian Bencana per Periode")

fig, ax = plt.subplots(figsize=(12, 8))
sns.barplot(x='periode', y='total_disasters', data=disasters_by_period_df, palette='coolwarm', ax=ax)
ax.set_xlabel('Periode')
ax.set_ylabel('Jumlah Kejadian Bencana')
ax.set_title('Distribusi Kejadian Bencana per Periode')
ax.set_xticks(range(len(disasters_by_period_df['periode'])))
ax.set_xticklabels(disasters_by_period_df['periode'].astype(str), rotation=90)
st.pyplot(fig)

# Visualize metrics
st.subheader("Visualisasi Metrik Kerugian")
fig, ax = plt.subplots(2, 2, figsize=(20, 24))

# Maximum Kerugian per KK
sns.barplot(x=metrics_df["kerugian_jumlah_kk"]["max"].sort_values(ascending=False).head().index, 
            y=metrics_df["kerugian_jumlah_kk"]["max"].sort_values(ascending=False).head().values, ax=ax[0, 0])
ax[0, 0].set_title('Kerugian Jumlah KK Maksimum')
ax[0, 0].set_xlabel('Daerah')
ax[0, 0].set_ylabel('Kerugian')

# Minimum Kerugian per KK
sns.barplot(x=metrics_df[metrics_df["kerugian_jumlah_kk"]["min"] > 0]["kerugian_jumlah_kk"]["min"].sort_values().head().index, 
            y=metrics_df[metrics_df["kerugian_jumlah_kk"]["min"] > 0]["kerugian_jumlah_kk"]["min"].sort_values().head().values, ax=ax[0, 1])
ax[0, 1].set_title('Kerugian Jumlah KK Minimum')
ax[0, 1].set_xlabel('Daerah')
ax[0, 1].set_ylabel('Kerugian')

# Maximum Taksiran Kerugian
sns.barplot(x=metrics_df["taksiran_kerugian"]["max"].sort_values(ascending=False).head().index, 
            y=metrics_df["taksiran_kerugian"]["max"].sort_values(ascending=False).head().values, ax=ax[1, 0])
ax[1, 0].set_title('Taksiran Kerugian Maksimum')
ax[1, 0].set_xlabel('Daerah')
ax[1, 0].set_ylabel('Taksiran Kerugian')

# Minimum Taksiran Kerugian
sns.barplot(x=metrics_df[metrics_df["taksiran_kerugian"]["min"] > 0]["taksiran_kerugian"]["min"].sort_values().head().index, 
            y=metrics_df[metrics_df["taksiran_kerugian"]["min"] > 0]["taksiran_kerugian"]["min"].sort_values().head().values, ax=ax[1, 1])
ax[1, 1].set_title('Taksiran Kerugian Minimum')
ax[1, 1].set_xlabel('Daerah')
ax[1, 1].set_ylabel('Taksiran Kerugian')

st.pyplot(fig)

# Filter data for selected month
st.subheader(f"Frekuensi Kejadian Bencana di {bulan_terpilih}")

# Display the most common Kecamatan
st.write("Kecamatan dengan kejadian bencana terbanyak adalah:")
st.write(most_common_kecamatan)

# Plot jumlah kejadian kebakaran per wilayah
st.subheader("Jumlah Kejadian Kebakaran per Wilayah")

fig, ax = plt.subplots(figsize=(12, 8))
kejadian_per_wilayah = df['wilayah'].value_counts()
sns.barplot(x=kejadian_per_wilayah.index, y=kejadian_per_wilayah.values, palette='viridis', ax=ax)
ax.set_xticklabels(kejadian_per_wilayah.index, rotation=90)
ax.set_xlabel('Wilayah')
ax.set_ylabel('Jumlah Kejadian')
ax.set_title('Jumlah Kejadian Kebakaran per Wilayah')
st.pyplot(fig)

# Display average loss and victims
st.subheader("Rata-Rata Kerugian dan Jumlah Korban")
st.write(f"Rata-rata Taksiran Kerugian: {formatted_rata_korban}")
st.write(f"Rata-rata Jumlah Korban per-KK: {formatted_rata_kerugian}")

# Plot scatter plot of loss vs. victims
st.subheader("Korelasi antara Kerugian dan Jumlah Korban")

fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(x='kerugian_jumlah_kk', y='taksiran_kerugian', data=df, alpha=0.6, ax=ax)
ax.set_xlabel('Kerugian')
ax.set_ylabel('Jumlah Korban')
ax.set_title('Scatter Plot antara Kerugian dan Jumlah Korban')
st.pyplot(fig)

# Display correlation
st.write(f"Koefisien Korelasi antara Kerugian dan Jumlah Korban: {korelasi:.2f}")

