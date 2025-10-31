# streamlit_app.py

import streamlit as st
from streamlit_gsheets import GSheetsConnection
from utility import check_password


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

    # Print results.
    for row in df.itertuples():
        st.write(f"{row.name} has a :{row.pet}:")

if __name__ == '__main__':
    main()
    