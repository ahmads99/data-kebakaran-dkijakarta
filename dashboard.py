# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

# Load dataset
# @st.cache
def load_data():
    return pd.read_csv('readytouse_alldata.csv')

df = load_data()

# Sidebar
st.sidebar.title('Dashboard Kebakaran DKI Jakarta')
st.sidebar.header('Filter Data')

# Convert 'tanggal' to datetime
df['tanggal'] = pd.to_datetime(df['tanggal'])

# Get min and max dates for default date input values
min_date = df['tanggal'].min().date()
max_date = df['tanggal'].max().date()

# Date filter
start_date = st.sidebar.date_input('Tanggal Mulai', min_date)
end_date = st.sidebar.date_input('Tanggal Selesai', max_date)

# Filter data based on selected date range
df_filtered = df[(df['tanggal'] >= pd.Timestamp(start_date)) & (df['tanggal'] <= pd.Timestamp(end_date))]

# Visual options
option = st.sidebar.selectbox('Pilih Visualisasi:', 
                              ['Jenis Kejadian per Bulan',
                                'Distribusi Jenis Kejadian Bencana', 
                               'Kerugian Berdasarkan Wilayah', 
                               'Tren Kerugian dari Bulan ke Bulan', 
                               'Top 5 Bulan dengan Kerugian Terbanyak', 
                               'Kerugian Berdasarkan Jenis Kejadian Bencana', 
                               'Jumlah Kejadian Kebakaran per Bulan', 
                               '10 Top Wilayah dengan Jumlah Kejadian Terbanyak', 
                               'Kecamatan dengan Jumlah Kejadian Terbanyak'
                               ])

# Title
st.title('Dashboard Kebakaran DKI Jakarta')

# Function to create and display plots
def display_plot(plot_func):
    plt.figure(figsize=(12, 6))
    plot_func()
    plt.tight_layout()
    st.pyplot(plt)
    
if option == 'Distribusi Jenis Kejadian Bencana':
    st.subheader('Distribusi Jenis Kejadian Bencana')

    # Hitung kejadian setiap jenis bencana
    jenis_bencana_counts = df_filtered['jenis_kejadian_bencana'].value_counts()

    # Tampilkan hasil sebagai tabel
    st.write("Jenis-jenis kejadian bencana yang paling sering terjadi:")
    st.dataframe(jenis_bencana_counts.reset_index().rename(columns={'index': 'Jenis Kejadian Bencana', 'jenis_kejadian_bencana': 'Jumlah Kejadian'}))

    # Plot hasil
    plt.figure(figsize=(12, 8))
    sns.barplot(x=jenis_bencana_counts.index, y=jenis_bencana_counts.values, palette='viridis')
    plt.title('Distribusi Jenis Kejadian Bencana')
    plt.xlabel('Jenis Kejadian Bencana')
    plt.ylabel('Jumlah Kejadian')
    plt.xticks(rotation=90)
    plt.grid(axis='y')

    st.pyplot(plt)

elif option == 'Jenis Kejadian per Bulan':
    st.subheader('Jenis Kejadian per Bulan')

    # Extract month and year for grouping
    df_filtered['bulan'] = df_filtered['tanggal'].dt.to_period('M').astype(str)
    
    # Group by month and jenis_kejadian_bencana and aggregate
    kejadian_per_bulan = df_filtered.groupby(['bulan', 'jenis_kejadian_bencana']).size().reset_index(name='jumlah_kejadian')

    # Find max and min values per jenis kejadian bencana
    max_values = kejadian_per_bulan.groupby('jenis_kejadian_bencana')['jumlah_kejadian'].idxmax()
    min_values = kejadian_per_bulan.groupby('jenis_kejadian_bencana')['jumlah_kejadian'].idxmin()
    
    # Highlight rows for max and min
    max_rows = kejadian_per_bulan.loc[max_values]
    min_rows = kejadian_per_bulan.loc[min_values]

    def plot():
        plt.figure(figsize=(14, 8))
        sns.lineplot(data=kejadian_per_bulan, x='bulan', y='jumlah_kejadian', hue='jenis_kejadian_bencana', marker='o')

        # Plot max and min points
        plt.scatter(max_rows['bulan'], max_rows['jumlah_kejadian'], color='red', s=100, label='Max', edgecolor='black')
        plt.scatter(min_rows['bulan'], min_rows['jumlah_kejadian'], color='blue', s=100, label='Min', edgecolor='black')

        plt.title('Jenis Kejadian per Bulan (Max dan Min)')
        plt.xlabel('Bulan')
        plt.ylabel('Jumlah Kejadian')
        plt.xticks(rotation=90)
        plt.legend()
        plt.grid(True)
    
    display_plot(plot)

elif option == 'Kerugian Berdasarkan Wilayah':
    st.subheader('Kerugian Berdasarkan Wilayah')
    def plot():
        sns.barplot(x='kerugian_jumlah_kk', y='wilayah', data=df_filtered, palette='magma')
        plt.title('Kerugian Berdasarkan Wilayah')
        plt.xlabel('Jumlah Kerugian')
        plt.ylabel('Wilayah')
    display_plot(plot)

elif option == 'Tren Kerugian dari Bulan ke Bulan':
    st.subheader('Tren Kerugian dari Bulan ke Bulan')
    df_filtered['bulan'] = df_filtered['tanggal'].dt.to_period('M').astype(str)
    kerugian_per_bulan = df_filtered.groupby('bulan')['kerugian_jumlah_kk'].sum().reset_index()
    kerugian_per_bulan = kerugian_per_bulan.sort_values(by='kerugian_jumlah_kk', ascending=False)
    def plot():
        sns.lineplot(x='bulan', y='kerugian_jumlah_kk', data=kerugian_per_bulan, marker='o', color='blue')
        plt.title('Tren Kerugian dari Bulan ke Bulan')
        plt.xlabel('Bulan')
        plt.ylabel('Jumlah Kerugian')
        plt.xticks(rotation=45)
        plt.grid(True)
    display_plot(plot)

elif option == 'Top 5 Bulan dengan Kerugian Terbanyak':
    st.subheader('Top 5 Bulan dengan Kerugian Terbanyak')
    df_filtered['bulan'] = df_filtered['tanggal'].dt.to_period('M').astype(str)
    kerugian_per_bulan = df_filtered.groupby('bulan')['kerugian_jumlah_kk'].sum().reset_index()
    kerugian_per_bulan = kerugian_per_bulan.sort_values(by='kerugian_jumlah_kk', ascending=False)
    top_5_bulan = kerugian_per_bulan.head(5)
    def plot():
        sns.barplot(x='kerugian_jumlah_kk', y='bulan', data=top_5_bulan, palette='magma')
        plt.title('Top 5 Bulan dengan Kerugian Terbanyak')
        plt.xlabel('Jumlah Kerugian')
        plt.ylabel('Bulan')
    display_plot(plot)

elif option == 'Kerugian Berdasarkan Jenis Kejadian Bencana':
    st.subheader('Kerugian Berdasarkan Jenis Kejadian Bencana')
    def plot():
        sns.barplot(x='kerugian_jumlah_kk', y='jenis_kejadian_bencana', data=df_filtered, palette='cividis')
        plt.title('Kerugian Berdasarkan Jenis Kejadian Bencana')
        plt.xlabel('Jumlah Kerugian')
        plt.ylabel('Jenis Kejadian Bencana')
    display_plot(plot)

elif option == 'Jumlah Kejadian Kebakaran per Bulan':
    st.subheader('Jumlah Kejadian Kebakaran per Bulan')
    df_filtered['bulan'] = df_filtered['tanggal'].dt.month_name()
    def plot():
        sns.countplot(x='bulan', data=df_filtered, palette='Set2')
        plt.title('Jumlah Kejadian Kebakaran per Bulan')
        plt.xlabel('Bulan')
        plt.ylabel('Jumlah Kejadian')
        plt.xticks(rotation=90)
    display_plot(plot)

elif option == '10 Top Wilayah dengan Jumlah Kejadian Terbanyak':
    st.subheader('10 Top Wilayah dengan Jumlah Kejadian Terbanyak')
    top_10_wilayah = df_filtered['wilayah'].value_counts().head(10).reset_index()
    top_10_wilayah.columns = ['Wilayah', 'Jumlah Kejadian']
    def plot():
        sns.barplot(x='Jumlah Kejadian', y='Wilayah', data=top_10_wilayah, palette='viridis')
        plt.title('10 Top Wilayah dengan Jumlah Kejadian Terbanyak')
        plt.xlabel('Jumlah Kejadian')
        plt.ylabel('Wilayah')
    display_plot(plot)

elif option == 'Kecamatan dengan Jumlah Kejadian Terbanyak':
    st.subheader('Kecamatan dengan Jumlah Kejadian Terbanyak')
    kecamatan_counts = df_filtered['kecamatan'].value_counts().reset_index()
    kecamatan_counts.columns = ['Kecamatan', 'Jumlah Kejadian']
    def plot():
        plt.figure(figsize=(20, 12))
        sns.barplot(x='Jumlah Kejadian', y='Kecamatan', data=kecamatan_counts, palette='magma', width=0.6)
        plt.title('Kecamatan dengan Jumlah Kejadian Terbanyak')
        plt.xlabel('Jumlah Kejadian')
        plt.ylabel('Kecamatan')
    display_plot(plot)

# Menambahkan teks hak cipta di footer
footer = """
<style>
footer {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background-color: #f1f1f1;
    text-align: center;
    padding: 10px;
    font-size: 14px;
    color: #555;
}
</style>
<footer>
    <p>&copy; 2024 Benzodiahmads. All rights reserved.</p>
</footer>
"""

# Render footer
st.markdown(footer, unsafe_allow_html=True)