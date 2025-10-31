import streamlit as st
import base64
# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="Methodology Page 1"
)
# endregion <--------- Streamlit App Configuration --------->

st.title("Methodology - Traders Tab Chatbot")


# Encode images into base 64 for streamlit's visuals
def image_base64(file):
    with open(file,"rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


methodology_traders_tab_img = image_base64("Methodology_Traders_Tab.jpg") 

with st.container():
    # set style of the methodology page
    st.markdown(f"""
    <div style="
        background-image: url('data:image/jpg;base64,{methodology_traders_tab_img }');
        background-size: cover;
        background-position: top;
        padding: 120px 400px;
        color: white;
        text-shadow: 0 0 5px rgba(0, 0, 0, 0.7);
    "> 
    <div style="height: 100px; width: 1000px"></div> <!-- dummy content -->
    </div>
    """, unsafe_allow_html=True)
    st.write("References:\n 1. Python's Icon: Python Logo PNG Vector (SVG) Free Download. (2025). Seeklogo. https://seeklogo.com/vector-logo/332789/python \n 2. Neural Network's Icon: https://www.facebook.com/flaticon. (2019, September 3). Neural Icon - 2103633. Flaticon. https://www.flaticon.com/free-icon/neural_2103633 \n 3. Robot's Icon : https://www.facebook.com/flaticon. (2022, June 6). Robot Icon - 7717267. Flaticon. https://www.flaticon.com/free-icon/robot_7717267")
    st.header("Sample User queries", divider=True)
    st.write("Hello")
    st.write("I want to import chinese medicine")
    st.write("where can i get testing from")
    st.write("oh my company is based in australia. can i conduct testing at a lab in australia?")
    st.write("btw, what are the procedures required for import?")
    st.write("what is voluntary notification? is it mandatory?")
    st.write("how do i know whether my product has androgenic steroids?")