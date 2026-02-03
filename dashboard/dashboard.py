import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ======================
# Page Config
# ======================
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

st.title("🚲 Bike Sharing Dashboard")
st.write("Analisis tren penyewaan sepeda berdasarkan waktu dan faktor lingkungan")

# ======================
# Load Data
# ======================
@st.cache_data
def load_data():
    df = pd.read_csv("day.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

df = load_data()

# ======================
# Mapping label biar human readable
# ======================
season_map = {
    1: 'Spring',
    2: 'Summer',
    3: 'Fall',
    4: 'Winter'
}

workingday_map = {
    0: 'Weekend/Holiday',
    1: 'Working Day'
}

df['season_label'] = df['season'].map(season_map)
df['workingday_label'] = df['workingday'].map(workingday_map)

# ======================
# Sidebar Filter
# ======================
st.sidebar.header("Filter Data")

selected_year = st.sidebar.multiselect(
    "Pilih Tahun",
    options=df['yr'].unique(),
    default=df['yr'].unique()
)

selected_season = st.sidebar.multiselect(
    "Pilih Musim",
    options=df['season_label'].unique(),
    default=df['season_label'].unique()
)

filtered_df = df[
    (df['yr'].isin(selected_year)) &
    (df['season_label'].isin(selected_season))
]

# ======================
# Metrics
# ======================
total_rentals = int(filtered_df['cnt'].sum())
avg_daily = int(filtered_df['cnt'].mean())
max_day = int(filtered_df['cnt'].max())

col1, col2, col3 = st.columns(3)

col1.metric("Total Rentals", f"{total_rentals:,}")
col2.metric("Avg Daily Rentals", avg_daily)
col3.metric("Peak Daily Rentals", max_day)

# ======================
# Line Chart Trend
# ======================
st.subheader("📈 Daily Rental Trend")

fig, ax = plt.subplots(figsize=(12,4))
ax.plot(filtered_df['dteday'], filtered_df['cnt'])
ax.set_xlabel("Date")
ax.set_ylabel("Rentals")

st.pyplot(fig)

# ======================
# Season Chart
# ======================
st.subheader("🌿 Rentals by Season")

season_data = filtered_df.groupby('season_label', observed=True)['cnt'].mean()

st.bar_chart(season_data)

# ======================
# Working Day Chart
# ======================
st.subheader("🏢 Working Day vs Weekend")

workingday_data = filtered_df.groupby('workingday_label', observed=True)['cnt'].mean()

st.bar_chart(workingday_data)

# ======================
# Footer Insight
# ======================
st.markdown("---")
st.markdown("""
### Insight:
- Permintaan meningkat saat musim hangat (Summer/Fall)
- Hari kerja memiliki rental lebih tinggi (commuting)
- Musim dingin menunjukkan penurunan signifikan
""")
