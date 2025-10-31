# streamlit_app.py

import streamlit as st
from streamlit_gsheets import GSheetsConnection
from utility import check_password
import base64

# Encode images into base 64 for streamlit's visuals
def image_base64(file):
    with open(file,"rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def main():
    # region <--------- Streamlit App Configuration --------->
    st.set_page_config(
        layout="centered",
        page_title="AI Champions Bootcamp Proof Of Concept",
        initial_sidebar_state="collapsed" 
    )

    # Do not continue if check_password is not True.  
    if not check_password():  
        st.stop()

    # endregion <--------- Streamlit App Configuration --------->

    # Create a connection object.
    conn = st.connection("gsheets", type=GSheetsConnection)

    st.write("Hello")
    df = conn.read()
    st.write("Raw data:")
    st.dataframe(df)
    singapore_img = image_base64("singapore.jpg")
    with st.container():
        # set style of the cover page
        st.markdown(f"""
        <div style="
            background-image: url('data:image/jpg;base64,{singapore_img}');
            background-size: cover;
            background-position: top;
            padding: 120px 20px;
            border-radius: 10px;
            color: white;
            text-shadow: 0 0 5px rgba(0, 0, 0, 0.7);
        ">
            <h3 style="margin: 0;">Importing and/or selling in Singapore</h3>
        </div>
        """, unsafe_allow_html=True)

    # Print results.
    for row in df.itertuples():
        st.write(f"{row.name} has a :{row.pet}:")

if __name__ == '__main__':
    main()
    