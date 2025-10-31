# streamlit_app.py

import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
#from utility import check_password
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

    # # Do not continue if check_password is not True.  
    # if not check_password():  
    #     st.stop()

    # endregion <--------- Streamlit App Configuration --------->

    st.set_page_config(layout="wide")

    # --- Connect to Google Sheets ---
    conn = st.connection("gsheets", type=GSheetsConnection)

    # --- Read data (optional) ---
    df = conn.read(worksheet="Orders", usecols=[0, 1, 2], ttl=5)
    prices_df = conn.read(worksheet="Prices")
    price_lookup = dict(zip(prices_df["Item"], prices_df["Price"]))
    if df is None or df.empty:
        df = pd.DataFrame(columns=["Item", "Quantity", "Timestamp"])

    # --- Define your products ---
    products = [
        {"name": "Sakura Lanyard", "image": "sakura_lanyard.jpg","price": price_lookup.get("sakura_lanyard.jpg", 0.0) },
        {"name": "Pink Lanyard", "image": "pink_lanyard.jpg","price": price_lookup.get("pink_lanyard.jpg", 0.0) },
        {"name": "Pouch(S)", "image": "comestic_pouch_small.jpg","price": price_lookup.get("comestic_pouch_small.jpg", 0.0)},
        {"name": "Pouch(B)", "image": "comestic_pouch_big.jpg","price": price_lookup.get("comestic_pouch_big.jpg", 0.0)},
        {"name": "Foldable Recyclable Bag", "image": "recyclable_bag.jpg","price": price_lookup.get("recyclable_bag.jpg", 0.0)},
        {"name": "Flower Dome", "image": "flower_dome.jpg","price": price_lookup.get("flower_dome.jpg", 0.0)}
    ]
    
    # --- Display grid layout ---
    cols = st.columns(5)  # 4 items per row

    # Initialize session state for quantities
    if "quantities" not in st.session_state:
        st.session_state.quantities = {item: 1 for item in price_lookup.keys()}

    for i, product in enumerate(products):
        col = cols[i % 5]

        # Load image
        with open(product["image"], "rb") as f:
            img_data = f.read()
        img_base64 = base64.b64encode(img_data).decode("utf-8")

        # Create clickable button with image
        with col:
            st.markdown(
                f"""
                <div style="
                    width: 160px;
                    height: 160px;
                    background: white url('data:image/jpg;base64,{img_base64}') center/contain no-repeat;
                    border: 2px solid #ddd;
                    border-radius: 10px;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
                    display: flex;
                    align-items: flex-end;
                    justify-content: center;
                    margin-bottom: 8px;
                    cursor: pointer;
                ">
                    <span style="background: rgba(0,0,0,0.5); color: white; width: 100%; text-align: center; border-radius: 0 0 10px 10px;">
                        {product["name"]} - $ {product["price"]}
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            #Quantity controls
            # Text input for quantity
            qty_input = st.text_input(
                f"Quantity ({product["name"]})",
                value="1",
                key=f"qty_{product["name"]}",
                max_chars=3
            )
           
            if st.button(f"Select {product['name']}", key=product["name"]):
                new_row = pd.DataFrame(
                    [[product["name"],int(qty_input), pd.Timestamp.now()]],
                    columns=["Item", "Quantity", "Timestamp"]
                )
                updated_df = pd.concat([df, new_row], ignore_index=True)
                conn.update(worksheet="Orders", data=updated_df)
                st.success(f"Added {product['name']} to Google Sheets!")


    # # Create a connection object.
    # conn = st.connection("gsheets", type=GSheetsConnection)

    # st.write("Hello")
    # df = conn.read()
    # st.write("Raw data:")
    # st.dataframe(df)
    # singapore_img = image_base64("sakura_lanyard.jpg")
    # with st.container():
    #     # set style of the cover page
    #     st.markdown(f"""
    #     <div style="
    #         width: 300px;
    #         height: 200px;
    #         background-image: url('data:image/jpg;base64,{singapore_img}');
    #         background-size: 80%;         /* make image smaller */
    #         background-repeat: no-repeat; /* prevent tiling */
    #         background-position: center;  /* center the image */
    #         background-color: #222;       /* fallback background color */
    #         border-radius: 10px;
    #         display: flex;
    #         align-items: center;
    #         justify-content: center;
    #         color: white;
    #         text-shadow: 0 0 5px rgba(0,0,0,0.7);
    #     ">
    #     <h4>POS Display</h4>
    #     </div>

    #         <h3 style="margin: 0;">Importing and/or selling in Singapore</h3>
    #     </div>
    #     """, unsafe_allow_html=True)

    # # Print results.
    # for row in df.itertuples():
    #     st.write(f"{row.name} has a :{row.pet}:")

if __name__ == '__main__':
    main()
    