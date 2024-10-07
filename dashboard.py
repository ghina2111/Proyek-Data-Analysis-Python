import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Contoh membaca dari CSV
air1_df = pd.read_csv("https://raw.githubusercontent.com/marceloreis/HTI/refs/heads/master/PRSA_Data_20130301-20170228/PRSA_Data_Aotizhongxin_20130301-20170228.csv")  # Ganti dengan nama file Anda
air2_df = pd.read_csv("https://raw.githubusercontent.com/marceloreis/HTI/refs/heads/master/PRSA_Data_20130301-20170228/PRSA_Data_Changping_20130301-20170228.csv")
air3_df = pd.read_csv("https://raw.githubusercontent.com/marceloreis/HTI/refs/heads/master/PRSA_Data_20130301-20170228/PRSA_Data_Dingling_20130301-20170228.csv")
air4_df = pd.read_csv("https://raw.githubusercontent.com/marceloreis/HTI/refs/heads/master/PRSA_Data_20130301-20170228/PRSA_Data_Dongsi_20130301-20170228.csv")
air5_df = pd.read_csv("https://raw.githubusercontent.com/marceloreis/HTI/refs/heads/master/PRSA_Data_20130301-20170228/PRSA_Data_Guanyuan_20130301-20170228.csv")
air6_df = pd.read_csv("https://raw.githubusercontent.com/marceloreis/HTI/refs/heads/master/PRSA_Data_20130301-20170228/PRSA_Data_Gucheng_20130301-20170228.csv")
air7_df = pd.read_csv("https://raw.githubusercontent.com/marceloreis/HTI/refs/heads/master/PRSA_Data_20130301-20170228/PRSA_Data_Huairou_20130301-20170228.csv")
air8_df = pd.read_csv("https://raw.githubusercontent.com/marceloreis/HTI/refs/heads/master/PRSA_Data_20130301-20170228/PRSA_Data_Nongzhanguan_20130301-20170228.csv")
air9_df = pd.read_csv("https://raw.githubusercontent.com/marceloreis/HTI/refs/heads/master/PRSA_Data_20130301-20170228/PRSA_Data_Shunyi_20130301-20170228.csv")
air10_df = pd.read_csv("https://raw.githubusercontent.com/marceloreis/HTI/refs/heads/master/PRSA_Data_20130301-20170228/PRSA_Data_Tiantan_20130301-20170228.csv")
air11_df = pd.read_csv("https://raw.githubusercontent.com/marceloreis/HTI/refs/heads/master/PRSA_Data_20130301-20170228/PRSA_Data_Wanliu_20130301-20170228.csv")
air12_df = pd.read_csv("https://raw.githubusercontent.com/marceloreis/HTI/refs/heads/master/PRSA_Data_20130301-20170228/PRSA_Data_Wanshouxigong_20130301-20170228.csv")

# Fungsi untuk memuat dan memproses data
def load_and_process_data():
    # Mengganti ini dengan proses loading DataFrame Anda
    # Contoh: air1_df, air2_df, ..., air12_df adalah DataFrame yang sudah ada
    df_all = pd.concat([air1_df, air2_df, air3_df, air4_df, air5_df, air6_df, 
                        air7_df, air8_df, air9_df, air10_df, air11_df, air12_df])
    df_all['date_time'] = pd.to_datetime(df_all[['year', 'month', 'day', 'hour']])
    
    return df_all

# Fungsi untuk pertanyaan 1
def question_1(df_all):
    st.header("Kota mana saja di tahun 2017 yang kualitas udaranya paling buruk sehingga dapat meningkatkan gangguan pernapasan?")

    df_all_2017 = df_all[df_all['year'] == 2017]
    pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
    city_pollutant_avg_2017 = df_all_2017.groupby('station')[pollutants].mean().reset_index()
    city_pollutant_avg_2017['Total_PM'] = city_pollutant_avg_2017['PM2.5'] + city_pollutant_avg_2017['PM10']
    top_polluted_cities_2017 = city_pollutant_avg_2017.sort_values(by='Total_PM', ascending=False)
    
    top_5_cities = top_polluted_cities_2017[['station', 'Total_PM']].head(5)
    
    # Visualisasi Pie Chart
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(top_5_cities['Total_PM'], labels=top_5_cities['station'], autopct='%1.1f%%', startangle=90,
           colors=['lightcoral', 'orange', 'lightgreen', 'skyblue', 'yellow'],
           wedgeprops={'edgecolor': 'black'})
    ax.set_title('Persentase Kualitas Udara Buruk di Top 5 Kota pada Tahun 2017 (Berdasarkan PM2.5 + PM10)')
    st.pyplot(fig)

# Fungsi untuk pertanyaan 2
def question_2(df_all):
    st.header("Apakah ada periode atau bulan tertentu dalam setahun di mana kualitas udara lebih buruk?")
    
    all_cities_df_2013_2017 = df_all[df_all['year'].between(2013, 2017)]
    pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
    monthly_avg = all_cities_df_2013_2017.groupby(['year', 'month'])[pollutants].mean().reset_index()
    monthly_avg['Total_Pollutants'] = monthly_avg['PM2.5'] + monthly_avg['PM10'] + monthly_avg['SO2'] + monthly_avg['NO2'] + monthly_avg['CO'] + monthly_avg['O3']
    
    # Visualisasi Tren Bulanan
    fig, ax = plt.subplots(figsize=(12, 8))
    for year in range(2013, 2017 + 1):
        data_per_year = monthly_avg[monthly_avg['year'] == year]
        ax.plot(data_per_year['month'], data_per_year['Total_Pollutants'], marker='o', label=f'Total Pollutants - {year}')
    
    ax.set_title('Tren Bulanan Total Polutan (2013-2017)')
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Rata-rata Total Polutan')
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

# Main function to run the Streamlit app
def main():
    st.title("Dashboard Kualitas Udara")
    
    # Load data
    df_all = load_and_process_data()
    
    # Display questions
    question_1(df_all)
    question_2(df_all)

if __name__ == "__main__":
    main()
