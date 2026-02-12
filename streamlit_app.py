import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO

# ------------------------------------------------------------
# Page Config
# ------------------------------------------------------------

st.set_page_config(
    page_title="Arctic Voice",
    page_icon="🐋",
    layout="wide"
)

# ------------------------------------------------------------
# Page Title
# ------------------------------------------------------------

st.title("🌊 Arctic Voice Dashboard")
st.markdown("### Cetacean Interaction Events in China (2012–2019)")
st.markdown("---")

# ------------------------------------------------------------
# Load & Clean Data
# ------------------------------------------------------------

@st.cache_data
def load_data():

    data_text = """
DATE	FACILITY	SPECIES	EVENT
8/14/2019	Beijing Aquarium	Bottlenose dolphin	Dolphins used for public interactions
8/10/2019	Hefei Yaotai Ocean World	Unknown Dolphin	trainer for a day advertised
7/25/2019	Weihai Shendiaoshen Safari Park	Bottlenose dolphin	Dolphins used for photo opportunities
7/22/2019	Sanya Haichang Fantasy Town	Beluga whale	TV celebrities allowed to kiss whales
6/9/2019	Beijing Aquarium	Beluga whale	Children allowed to interact
3/27/2018	Zhuhai Chimelong Ocean Kingdom	Bottlenose dolphin	Dolphins used for photo opportunities
3/26/2018	Guangzhou Grandview Aquarium	Beluga whale	Whales used for photo opportunities
1/29/2018	Nanchang Sunac Ocean Park	Bottlenose dolphin	Close contact feeding interactions
5/21/2017	Beijing Aquarium	Beluga whale	Public interactions
4/17/2017	Shenzhen Safari Park	Pantropical spotted dolphin	Swim-with encounters
3/2/2017	Fuzhou Polar Ocean World	Beluga whale	Public photo sessions
6/27/2016	Fenjiezhou Island Aquarium	Pacific white-sided dolphin	Swim-with encounters
4/11/2015	Fushun Royal Ocean World	Beluga whale	Public interactions
1/15/2015	Dalian Laohutan Ocean Park	Beluga whale	Public interactions
3/23/2012	Dalian SunAsia Ocean World	Bottlenose dolphin	Public interactions
"""

    df = pd.read_csv(StringIO(data_text), sep="\t")
    df["DATE"] = pd.to_datetime(df["DATE"])
    df["YEAR"] = df["DATE"].dt.year
    df["MONTH"] = df["DATE"].dt.month

    return df

df = load_data()

# ------------------------------------------------------------
# Sidebar Filters
# ------------------------------------------------------------

st.sidebar.header("Filter Options")

selected_years = st.sidebar.slider(
    "Select Year Range",
    int(df["YEAR"].min()),
    int(df["YEAR"].max()),
    (int(df["YEAR"].min()), int(df["YEAR"].max()))
)

selected_species = st.sidebar.multiselect(
    "Select Species",
    df["SPECIES"].unique(),
    default=list(df["SPECIES"].unique())
)

filtered_df = df[
    (df["YEAR"] >= selected_years[0]) &
    (df["YEAR"] <= selected_years[1]) &
    (df["SPECIES"].isin(selected_species))
]

# ------------------------------------------------------------
# Summary Metrics
# ------------------------------------------------------------

st.markdown("## 📊 Summary Statistics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Events", len(filtered_df))
col2.metric("Unique Facilities", filtered_df["FACILITY"].nunique())
col3.metric("Species Involved", filtered_df["SPECIES"].nunique())

st.markdown("---")

# ------------------------------------------------------------
# Chart 1: Events by Year
# ------------------------------------------------------------

st.subheader("📅 Events by Year")

year_counts = filtered_df["YEAR"].value_counts().sort_index()

fig1, ax1 = plt.subplots()
ax1.bar(year_counts.index.astype(str), year_counts.values)
ax1.set_xlabel("Year")
ax1.set_ylabel("Number of Events")

st.pyplot(fig1)

# ------------------------------------------------------------
# Chart 2: Top Facilities
# ------------------------------------------------------------

st.subheader("🏢 Top Facilities")

facility_counts = filtered_df["FACILITY"].value_counts()

fig2, ax2 = plt.subplots()
ax2.barh(facility_counts.index, facility_counts.values)
ax2.set_xlabel("Number of Events")
ax2.invert_yaxis()

st.pyplot(fig2)

# ------------------------------------------------------------
# Chart 3: Species Distribution
# ---------------------
