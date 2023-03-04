import numpy as np
import time
import streamlit as st

st.set_page_config(page_title="tabeltabel")
st.title('tabel')

data = np.random.randn(10, 2)
chart = st.line_chart(data)
time.sleep(1)
data2= np.random.randn(10,2)
chart.add_rows(data2)