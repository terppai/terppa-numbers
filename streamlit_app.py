import altair as alt
import pandas as pd
import streamlit as st
import numpy as np

# Show the page title and description.
st.set_page_config(page_title="Terppa-dataa", page_icon="")
st.title("Terppa-dataa")
st.write(
    """
    Täällä on Terppaan liittyvää dataa. 
    Kuten kokonaiskuvasta kertovat KPIt ja yrityskohtaista tietoa.
    """
)


# Load the data from a CSV. We're caching this so it doesn't reload every time the app
# reruns (e.g. if the user interacts with the widgets). 
# Note to self, it's Pandas dateframe, because NumPy's one doesnt' have column names.
@st.cache_data
def load_data():
    df = pd.read_csv("/Users/jussikorhonen/terppa-numbers-main/data/Terppa-figures.csv")
    return df

df = load_data()

# Checks if there are values with 0 in the column and replaces it with 9.90 which is the minimun monthly fee
column_name = 'Hinta yht tt-asiakkaat'
if column_name in df.columns:
    # Replace 0 with 9.90 in the target column
    df.loc[df[column_name] == 0.00, column_name] = 9.90
else:
    st.write(f"Column '{column_name}' does not exist in the DataFrame.")


st.title("KPIs")
col1, col2, col3 = st.columns(3)

# Calculate MRR and show it in col1
with col1:
    MRR = df['Hinta yht tt-asiakkaat'].sum()
    st.subheader("MRR")
    st.subheader(f"{MRR:.2f} €")
    MRR_lastmonth = 27262.4

    # Perform the decrement operation
    MRR_ero = MRR - MRR_lastmonth

    # Perform the division operation
    MRR_kasvu = MRR_ero / MRR_lastmonth * 100
    st.write(f"{MRR_kasvu:.2f} % MoM kasvu")


# Calculate number of customer companies and show it in col2
with col2:
    yritykset_maara = len(df['ID'])
    st.subheader("Asiakasyritykset")
    st.subheader(f"{yritykset_maara} kpl")
    yritykset_maara_lastmonth = 699

    # Perform the decrement operation
    yr_maara_ero = yritykset_maara - yritykset_maara_lastmonth

    # Perform the division operation
    yritysten_kasvu = yr_maara_ero / yritykset_maara_lastmonth * 100
    st.write(f"{yritysten_kasvu:.2f} % MoM kasvu")

# Calculate number of customer companies and show it in col3
with col3:
    tt_maara = df['Työterveysasiakkaita'].sum()
    st.subheader("TT-määrä")
    st.subheader(f"{tt_maara} kpl")
    tt_maara_lastmonth = 1851

    # Perform the decrement operation
    tt_maara_ero = tt_maara - tt_maara_lastmonth

    # Perform the division operation
    tt_kasvu = tt_maara_ero / tt_maara_lastmonth * 100
    st.write(f"{tt_kasvu:.2f} % MoM kasvu")


# KPIs ENNUSTE!
st.title("KPIs forecast")
st.write("HUOM! Ennuste perustuu nykyiseen KPI-kohtaiseen prosentuaaliseen kasvuvauhtiin.")

#Valitse ennusteen aikaikkuna
ennuste_kk = ['3', '6', '12', '18', '24', '36']
valittu_ennuste = st.selectbox("Valitse ennusteen aikajänne kuukausissa", ennuste_kk)

st.write(f"KPI:t: {valittu_ennuste} kuukauden päästä nykyisellä kasvuvauhdilla.")
valittu_ennuste_int = int(valittu_ennuste)


col1, col2, col3 = st.columns(3)

# Calculate MRR forecast based on the timeframe given and show it in col1

with col1:
    MRR_ennuste = MRR * (1 + MRR_kasvu/100) ** valittu_ennuste_int
    MRR_ennuste_rounded = round(MRR_ennuste)
    st.subheader("MRR ennuste")
    st.subheader(f"{MRR_ennuste_rounded} €")

# Calculate number of customer companies forecast based on the timeframe given and show it in col2
with col2:
    yritykset_ennuste = yritykset_maara * (1 + yritysten_kasvu/100) ** valittu_ennuste_int
    yritykset_ennuste_rounded = round(yritykset_ennuste)
    st.subheader("Asiakasyritykset ennuste")
    st.subheader(f"{yritykset_ennuste_rounded} kpl")

# Calculate number of customer employees forecast based on the timeframe given and show it in col3
with col3:
    tt_maara_ennuste = tt_maara * (1 + tt_kasvu/100) ** valittu_ennuste_int
    tt_maara_ennuste_rounded = round(tt_maara_ennuste)
    st.subheader("TT-määrä ennuste")
    st.subheader(f"{tt_maara_ennuste_rounded} kpl")


st.title("Yrityskohtaista tietoa")
# Show a multiselect widget with the columns using `st.multiselect`.
columns = df.columns.tolist()
default_columns = ['Y-tunnus', 'Nimi']
selected_columns = st.multiselect(
    "Mitä yrityskohtaista tietoa haluat näytettävän?",
    columns,
    default=default_columns,
)


# Check if any columns are selected
if selected_columns:
    # Filter the DataFrame based on selected columns
    df_filtered = df[selected_columns]
    # Display the filtered DataFrame
    st.write("Tässä valitsemasi tiedot:")
    st.write(df_filtered)
else:
    st.write("Valitse edes yksi sarake.")



# # Show a slider widget with the years using `st.slider`.
# years = st.slider("Years", 1986, 2006, (2000, 2016))

# Filter the dataframe based on the widget input and reshape it.
#df_filtered = df[(df["selected_columns"].isin(columns)))]]
# df_reshaped = df_filtered.pivot_table(
#     index="year", columns="genre", values="gross", aggfunc="sum", fill_value=0
# )
# df_reshaped = df_reshaped.sort_values(by="year", ascending=False)

# # Display the data as a table using `st.dataframe`.
# st.dataframe(
#     df_reshaped,
#     use_container_width=True,
#     column_config={"year": st.column_config.TextColumn("Year")},
# )

# # Display the data as an Altair chart using `st.altair_chart`.
# df_chart = pd.melt(
#     df_reshaped.reset_index(), id_vars="year", var_name="genre", value_name="gross"
# )
# chart = (
#     alt.Chart(df_chart)
#     .mark_line()
#     .encode(
#         x=alt.X("year:N", title="Year"),
#         y=alt.Y("gross:Q", title="Gross earnings ($)"),
#         color="genre:N",
#     )
#     .properties(height=320)
# )
# st.altair_chart(chart, use_container_width=True)
