import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

air1_df = pd.read_csv("https://raw.githubusercontent.com/marceloreis/HTI/refs/heads/master/PRSA_Data_20130301-20170228/PRSA_Data_Aotizhongxin_20130301-20170228.csv") 
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

def load_and_process_data():
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
    
    st.write('\n \n Kualitas udara yang buruk terutama dipengaruhi oleh tingginya konsentrasi PM2.5 dan PM10 (Particulate Matter dengan ukuran partikel ≤2.5 µm dan ≤10 µm).')
    st.write('\n1. Pengaruh PM2.5 dan PM10 terhadap Kesehatan Pernapasan')
    st.write('\nPM2.5 dapat menembus hingga alveoli paru-paru, menyebabkan inflamasi paru-paru, memperburuk asma, serta meningkatkan risiko penyakit kardiovaskular. PM10 dapat menyebabkan iritasi pada sistem pernapasan bagian atas (hidung, tenggorokan), serta meningkatkan risiko bronkitis kronis.')
    st.write('\n2. Sumber Pencemaran di Kota-Kota Tersebut')
    st.write('\nDongsi dan Wanshouxigong memiliki kepadatan lalu lintas tinggi, menghasilkan banyak polutan dari kendaraan bermotor. Gucheng dan Tiantan dipengaruhi oleh kombinasi polusi industri dan urbanisasi pesat. Nongzhanguan mengalami akumulasi polutan dari sumber domestik dan transportasi.')
    st.write('\n3. Dampak Jangka Panjang')
    st.write('\nPolusi udara kronis dapat menyebabkan penurunan fungsi paru-paru, meningkatkan resiko kanker paru-paru, dan mempercepat penuaan sistem pernapasan. Kelompok rentan seperti anak-anak, lansia, dan penderita penyakit paru obstruktif kronis (PPOK) lebih berisiko mengalami dampak serius. Dengan demikian, lima kota ini memang memiliki kualitas udara yang buruk dan berpotensi meningkatkan gangguan pernapasan, terutama bagi kelompok rentan.')

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
    
    st.write('\n \n Berdasarkan tren bulanan total polutan dari tahun 2013 hingga 2017, terlihat adanya pola peningkatan konsentrasi polutan yang signifikan mulai bulan September hingga November, dengan nilai tertinggi pada bulan Desember. Peningkatan ini dapat dikaitkan dengan faktor musiman seperti perubahan pola atmosfer, penurunan curah hujan yang menyebabkan akumulasi partikel polutan di udara, serta peningkatan emisi dari sumber industri dan kendaraan bermotor akibat peningkatan aktivitas manusia menjelang akhir tahun. Fenomena ini sejalan dengan tren global di mana musim gugur hingga awal musim dingin sering dikaitkan dengan kualitas udara yang lebih buruk akibat inversi suhu, yang menjebak polutan di lapisan udara yang lebih rendah dan mengurangi dispersi alami.')
# Main function to run the Streamlit app
def main():
    st.title("Dashboard Kualitas Udara")
    df_all = load_and_process_data()
    
    question_1(df_all)
    question_2(df_all)

if __name__ == "__main__":
    main()
