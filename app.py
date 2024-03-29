import streamlit as st
import pandas as pd
import plotly.express as px
import base64
from io import StringIO, BytesIO

def generate_excel_download_link(df):
    towrite = BytesIO()
    df.to_excel(towrite, encoding="utf-8", index=False, header=True) #write to BytesIO
    towrite.seek(0) #reset pointer
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="data_download.xlsx">Download Excel File</a>'
    return  st.markdown(href, unsafe_allow_html=True)

def generate_html_download_link(fig):
    towrite = StringIO()
    fig.write_html(towrite, include_plotlyjs="cdn")
    towrite = BytesIO(towrite.getvalue().encode())
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:text/html;charset=utf-8;base64, {b64}" download="plot.html.">Download Plot</a>'
    return st.markdown(href, unsafe_allow_html=True)

st.set_page_config(page_title="Excel Plotter")
st.title('Excel Plotter')
st.subheader('Feed me')

uploaded_file = st.file_uploader('Kies een excel', type='xlsx') #door het type te definiëren zorg je ervoor dat hij alleen maar xlsx kan uploaden
if uploaded_file:
    st.markdown('---')
    df = pd.read_excel(uploaded_file, engine='openpyxl')
    st.dataframe(df)
    groupby_colomn = st.selectbox(
        'Wat wil je zien?',
        ('Ship Mode', 'Segment', 'Category', 'Sub-Category'),
    )

    # --- groepeer dataframe
    output_columns = ['Sales', 'Profit']
    df_grouped = df.groupby(by=[groupby_colomn], as_index=False)[output_columns].sum()
    #st.dataframe(df_grouped)

    # -- PLOT DATAFRAME
    fig = px.bar(
        df_grouped,
        x= groupby_colomn,
        y='Sales',
        color='Profit',
        color_continuous_scale=['red', 'yellow', 'green'],
        template='plotly_white',
        title=f'<b>Sales & Profit by {groupby_colomn}</b>'
    )
    st.plotly_chart(fig)

    #--- DOWNLOAD SECTION
    st.subheader('Downloads:')
    generate_excel_download_link(df_grouped)
    generate_html_download_link(fig)



