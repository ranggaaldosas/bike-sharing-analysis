import streamlit as st

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use("dark_background")

bike_df = pd.read_csv("./bike.csv")
hour_df = pd.read_csv("./hour.csv")

bike_df.rename(
    columns={
        "dteday": "tanggal",
        "yr": "tahun",
        "mnth": "month",
        "weathersit": "kondisi_cuaca",
        "hum": "humidity",
        "casual": "jumlah_pengguna_casual",
        "cnt": "jumlah_total",
    },
    inplace=True,
)


mapping_dict = {0: "2011", 1: "2012"}
season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
month_mapping = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec",
}
weathersit_mapping = {1: "Clear", 2: "Misty", 3: "Light_rainsnow"}
weekday_mapping = {
    0: "Sunday",
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday",
}

bike_df["tahun"] = bike_df["tahun"].map(mapping_dict)
bike_df["season"] = bike_df["season"].map(season_mapping)
bike_df["month"] = bike_df["month"].map(month_mapping)
bike_df["kondisi_cuaca"] = bike_df["kondisi_cuaca"].map(weathersit_mapping)
bike_df["weekday"] = bike_df["weekday"].map(weekday_mapping)

st.title("Share-Bike - Dashboard Analysis 📈")

min_date = pd.to_datetime(bike_df["tanggal"]).dt.date.min()
max_date = pd.to_datetime(bike_df["tanggal"]).dt.date.max()

with st.sidebar:
    st.image("logo.jpg", caption="Share-Bike", use_column_width=True)

    start_date, end_date = st.date_input(
        label="Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date],
    )

    st.markdown("---")

    add_selectbox = st.sidebar.selectbox(
        "Butuh bantuan? Bagaimana Anda ingin dihubungi?",
        ("Email", "Telepon Rumah", "Telepon Seluler"),
    )

    # Jika Anda ingin melakukan sesuatu dengan pilihan pengguna setelah mereka menekan tombol submit
    if st.sidebar.button("Submit"):
        st.sidebar.write(f"Pilihan Anda: {add_selectbox}")

    url = "https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset/"

    st.link_button("Link Dataset", url)


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Casual Usage", value=bike_df["jumlah_pengguna_casual"].sum())
with col2:
    st.metric(label="Total Usage", value=bike_df["jumlah_total"].sum())
with col3:
    st.metric(label="Registered Account", value=bike_df["registered"].sum())

st.markdown("---")

with st.container():
    bike_df["tanggal"] = pd.to_datetime(bike_df.tanggal)
    bike_df["month_year"] = bike_df["tanggal"].dt.to_period("M")
    monthly_rentals = (
        bike_df.groupby(["month_year", "tahun"])["jumlah_total"].sum().reset_index()
    )
    monthly_rentals_pivot = monthly_rentals.pivot(
        index="month_year", columns="tahun", values="jumlah_total"
    )
    monthly_rentals_pivot.index = monthly_rentals_pivot.index.to_timestamp()

    st.title("Perkembangan User Share-Bike Tahun 2011 vs 2012")

    # Create the plot inside the container
    plt.figure(figsize=(15, 8))
    for column in monthly_rentals_pivot.columns:
        plt.plot(
            monthly_rentals_pivot.index, monthly_rentals_pivot[column], label=column
        )

    plt.title("Tren Jumlah Total Penyewaan Sepeda per Bulan (2011 vs 2012)")
    plt.xlabel("Bulan dan Tahun")
    plt.ylabel("Jumlah Total Penyewaan")
    plt.xticks(rotation=45)
    plt.legend(title="Tahun")
    plt.tight_layout()

    st.pyplot(plt)

    with st.expander("Lihat penjelasan"):
        st.write(
            """
            Grafik garis ini menampilkan tren jumlah total penyewaan sepeda per bulan untuk tahun 2011 dan 2012. 
            Pada tahun 2011, jumlah penyewaan dimulai dengan nilai yang rendah, mencapai puncak di pertengahan tahun, 
            kemudian menurun menjelang akhir tahun. Sebaliknya, tahun 2012 menunjukkan peningkatan signifikan dalam 
            penyewaan dari awal tahun, dengan puncaknya terjadi menjelang akhir tahun. Tren ini menandakan peningkatan 
            permintaan untuk layanan bike-sharing pada tahun 2012 dibandingkan dengan tahun 2011.
            """
        )

st.markdown("---")

with st.container():
    rental_jam = hour_df.groupby("hr")["cnt"].mean()
    rental_day = bike_df.groupby("weekday")["jumlah_total"].mean()
    rental_month = bike_df.groupby("month")["jumlah_total"].mean()

    fig, axs = plt.subplots(3, 1, figsize=(10, 15))  # Adjust the figure size as needed

    # Plot 1: Rata-Rata Penyewaan per Jam
    axs[0].bar(rental_jam.index, rental_jam.values, color="#6420AA")
    axs[0].set_title("Rata - Rata Penyewaan per Jam")
    axs[0].set_xlabel("Jam")
    axs[0].set_ylabel("Rata - Rata Penyewaan")

    # Plot 2: Rata-Rata Penyewaan per Hari
    axs[1].bar(rental_day.index, rental_day.values, color="#ff7f0e")
    axs[1].set_title("Rata-Rata Penyewaan per Hari")
    axs[1].set_xlabel("Hari")
    axs[1].set_ylabel("Rata-Rata Penyewaan")
    axs[1].set_xticks(range(len(rental_day.index)))
    axs[1].set_xticklabels(rental_day.index, rotation=45)

    # Plot 3: Rata-Rata Penyewaan per Bulan
    axs[2].bar(rental_month.index, rental_month.values, color="#2ca02c")
    axs[2].set_title("Rata-Rata Penyewaan per Bulan")
    axs[2].set_xlabel("Bulan")
    axs[2].set_ylabel("Rata-Rata Penyewaan")
    axs[2].set_xticks(rental_month.index)
    axs[2].set_xticklabels(
        [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "Mei",
            "Jun",
            "Jul",
            "Agu",
            "Sep",
            "Okt",
            "Nov",
            "Des",
        ]
    )

    plt.tight_layout()

    st.pyplot(plt)

    with st.expander("Penjelasan Plot 1 - Rata-Rata Penyewaan per Jam:"):
        st.write(
            """
            Visualisasi ini menunjukkan tren penyewaan sepeda sepanjang hari, dengan puncak penyewaan terjadi selama jam-jam sibuk pagi dan sore hari. Ini menunjukkan bahwa sepeda sering digunakan untuk perjalanan ke dan dari tempat kerja atau sekolah. Kita juga melihat adanya penurunan yang signifikan selama jam-jam siang hari, yang mungkin karena pengguna bekerja atau tidak memilih untuk beraktivitas di luar selama jam tersebut.
            """
        )

    with st.expander("Penjelasan Plot 2 - Rata-Rata Penyewaan per Hari:"):
        st.write(
            """
            Grafik ini menggambarkan rata-rata penyewaan sepeda untuk setiap hari dalam seminggu, yang menunjukkan konsistensi dalam penggunaan dengan sedikit variasi. Hal ini bisa menandakan bahwa layanan penyewaan sepeda merupakan bagian dari rutinitas harian yang stabil, tidak terpengaruh secara signifikan oleh perubahan hari dalam seminggu.
            """
        )

    with st.expander("Penjelasan Plot 3 Rata-Rata Penyewaan per Bulan:"):
        st.write(
            """
            Dari visualisasi ini, kita dapat melihat bahwa penyewaan sepeda cenderung meningkat selama bulan-bulan hangat, dengan puncak pada bulan-bulan musim panas. Ini menegaskan pola umum bahwa cuaca yang lebih hangat dan kondisi siang hari yang lebih panjang mendorong lebih banyak aktivitas di luar ruangan dan penggunaan sepeda.
            """
        )

st.markdown("---")

with st.container():

    def summary_categorical_columns(dataframe, col_names):
        col1, col2 = st.columns(2)
        with col1:
            st.subheader(f"Summary for {col_names[0]}:")
            summary_df1 = pd.DataFrame(
                {
                    col_names[0]: dataframe[col_names[0]].value_counts(),
                    "Ratio": round(
                        100 * dataframe[col_names[0]].value_counts() / len(dataframe), 2
                    ),
                }
            )
            st.dataframe(summary_df1.style.format({"Ratio": "{:.2f}%"}))

        with col2:
            st.subheader(f"Summary for {col_names[1]}:")
            summary_df2 = pd.DataFrame(
                {
                    col_names[1]: dataframe[col_names[1]].value_counts(),
                    "Ratio": round(
                        100 * dataframe[col_names[1]].value_counts() / len(dataframe), 2
                    ),
                }
            )
            st.dataframe(summary_df2.style.format({"Ratio": "{:.2f}%"}))

    # List of columns to summarize
    col_names_to_summarize = ["kondisi_cuaca", "season"]
    summary_categorical_columns(bike_df, col_names_to_summarize)

st.markdown("---")

with st.container():
    st.title("Analisis RFM (Recency, Frequency, Monetary)")

    bike_df.rename(
        columns={"tanggal": "date", "weekday": "day", "jumlah_total": "total_user"},
        inplace=True,
    )

    bike_df["day"] = bike_df["date"].dt.day_name()

    rfm_df = bike_df.groupby(by="day", as_index=False).agg(
        {"date": "max", "instant": "nunique", "total_user": "sum"}
    )

    rfm_df.columns = ["day", "max_order_timestamp", "frequency", "monetary"]

    rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
    recent_date = bike_df["date"].dt.date.max()
    rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(
        lambda x: (recent_date - x).days
    )

    rfm_df.drop("max_order_timestamp", axis=1, inplace=True)

    ordered_days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    rfm_df["day"] = pd.Categorical(rfm_df["day"], categories=ordered_days, ordered=True)
    rfm_df.sort_values("day", inplace=True)

    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 6))
    colors = ["#72BCD4"] * 5  # Maintain the same color for all bars

    # By Recency
    sns.barplot(y="recency", x="day", data=rfm_df, palette=colors, ax=ax[0])
    ax[0].set_ylabel(None)
    ax[0].set_xlabel(None)
    ax[0].set_title("By Recency (days)", loc="center", fontsize=18)
    ax[0].tick_params(axis="x", labelsize=15)

    # By Frequency
    sns.barplot(y="frequency", x="day", data=rfm_df, palette=colors, ax=ax[1])
    ax[1].set_ylabel(None)
    ax[1].set_xlabel(None)
    ax[1].set_title("By Frequency", loc="center", fontsize=18)
    ax[1].tick_params(axis="x", labelsize=15)

    # By Monetary
    sns.barplot(y="monetary", x="day", data=rfm_df, palette=colors, ax=ax[2])
    ax[2].set_ylabel(None)
    ax[2].set_xlabel(None)
    ax[2].set_title("By Monetary", loc="center", fontsize=18)
    ax[2].tick_params(axis="x", labelsize=15)

    plt.tight_layout()

    # Streamlit function to display the plot
    st.pyplot(fig)

    with st.expander("Pemahaman Diagram Analisis RFM"):
        st.write(
            """
            Diagram analisis RFM menampilkan metrik keterlibatan pelanggan utama berdasarkan interaksi mereka seiring waktu, dikategorikan berdasarkan hari dalam seminggu.

            - **Berdasarkan Recency (hari)**: Diagram ini menunjukkan seberapa baru pelanggan berinteraksi dengan layanan, dengan Senin yang tidak ada data nya, dan Tuesday merupakan hari dimana data sangat dominan. Recency yang lebih singkat umumnya menunjukkan kemungkinan interaksi baru-baru ini yang lebih tinggi.

            - **Berdasarkan Frequency**: Diagram frekuensi menyoroti jumlah interaksi yang dilakukan pelanggan dengan layanan selama seminggu. Hari dengan batang yang lebih tinggi menunjukkan penggunaan yang lebih sering, menyarankan hari-hari tersebut adalah yang paling populer atau menjadi rutin untuk keterlibatan.

            - **Berdasarkan Monetary**: Diagram nilai moneter menggambarkan total nilai yang dihasilkan oleh pelanggan pada setiap hari dalam seminggu. Nilai moneter yang lebih tinggi menunjukkan pengeluaran atau penggunaan pelanggan yang lebih besar, memberikan wawasan tentang hari-hari yang paling berharga bagi bisnis.
            
            Secara keseluruhan, diagram-diagram ini menawarkan gambaran tentang perilaku pelanggan, menunjukkan kapan pelanggan paling mungkin untuk terlibat, seberapa sering mereka melakukannya, dan nilai yang mereka bawa. Wawasan seperti ini sangat penting untuk perencanaan strategis, alokasi sumber daya, dan upaya pemasaran yang ditargetkan.
        """
        )
