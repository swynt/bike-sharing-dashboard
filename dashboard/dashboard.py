import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    layout="wide"
)

sns.set_style("whitegrid")


# =====================================================
# LOAD CLEAN DATA (HASIL NOTEBOOK)
# =====================================================
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/all_data.csv")   # <-- dari notebook
    df['date'] = pd.to_datetime(df['date'])
    return df


df = load_data()


# =====================================================
# TITLE
# =====================================================
st.title("🚴 Bike Sharing Dashboard")
st.caption("Analisis tren penyewaan sepeda dan faktor lingkungan (2011–2012)")


# =====================================================
# SIDEBAR FILTER
# =====================================================
st.sidebar.header("Filter Date")

start, end = st.sidebar.date_input(
    "Rentang Waktu",
    [df['date'].min(), df['date'].max()]
)

df = df[(df['date'] >= pd.to_datetime(start)) &
        (df['date'] <= pd.to_datetime(end))]


# =====================================================
# METRICS
# =====================================================
c1, c2, c3 = st.columns(3)

c1.metric("Total Rentals", f"{df['total_rentals'].sum():,}")
c2.metric("Avg Daily", f"{int(df['total_rentals'].mean()):,}")
c3.metric("Max Daily", f"{df['total_rentals'].max():,}")


# =====================================================
# ==================== Q1 =============================
# Trend waktu
# =====================================================
st.header("📈 Tren Penyewaan Sepeda Harian")

st.line_chart(df.set_index('date')['total_rentals'])


# =====================================================
# ==================== Q2 =============================
# Faktor lingkungan
# =====================================================
st.header("🌦 Pengaruh Faktor Lingkungan")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Season vs Rentals")
    fig1, ax1 = plt.subplots()
    sns.boxplot(
        x='season_label',
        y='total_rentals',
        data=df,
        order=['Spring','Summer','Fall','Winter'],
        ax=ax1
    )
    st.pyplot(fig1)


with col2:
    st.subheader("Working Day vs Rentals")
    fig2, ax2 = plt.subplots()
    sns.boxplot(
        x='workingday_label',
        y='total_rentals',
        data=df,
        order=['Weekend/Holiday','Working Day'],
        ax=ax2
    )
    st.pyplot(fig2)


# =====================================================
# ================= ANALISIS LANJUTAN ==================
# =====================================================
st.header("🔥 Analisis Lanjutan")

col3, col4 = st.columns(2)


# ---- Temperature binning ----
with col3:
    st.subheader("Rental berdasarkan Suhu")

    df['temp_group'] = pd.cut(df['temp'], bins=3, labels=['Cold','Warm','Hot'])
    temp_avg = df.groupby('temp_group')['total_rentals'].mean()

    st.bar_chart(temp_avg)


# ---- Demand clustering ----
with col4:
    st.subheader("Segmentasi Level Permintaan")

    df['demand_level'] = pd.qcut(
        df['total_rentals'],
        q=3,
        labels=['Low','Medium','High']
    )

    demand_avg = df.groupby('demand_level')['total_rentals'].mean()

    st.bar_chart(demand_avg)


# =====================================================
# FOOTER
# =====================================================
st.caption("Created with Streamlit • Dicoding Data Analysis Project")
st.caption("Dataset: Bike Sharing Dataset (UCI Repository)")
st.caption("By Cornelius")