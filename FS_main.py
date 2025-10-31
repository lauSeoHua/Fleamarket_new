# streamlit_app.py

import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
#from utility import check_password
import base64
import datetime
import pytz
import time
# Set your timezone, e.g., Singapore
time_zone = pytz.timezone('Asia/Singapore')
my_time = datetime.utcnow()
# get the standard UTC time
UTC = pytz.utc

# it will get the time zone
# of the specified location
IST = pytz.timezone('Asia/Singapore')
datetime_utc = datetime.now(IST)
current_time = datetime_utc.strftime('%Y:%m:%d %H:%M:%S %Z %z'))


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
    df = conn.read(worksheet="Orders", usecols=[0, 1, 2,3], ttl=5)
    prices_df = conn.read(worksheet="Prices")
    price_lookup = dict(zip(prices_df["Item"], prices_df["Price"]))
    if df is None or df.empty:
        df = pd.DataFrame(columns=["Item", "Quantity", "Timestamp","Price Sold for"])

    # --- Define your products ---
    products = [
        {"name": "Sakura Lanyard", "image": "sakura_lanyard.jpg","price": price_lookup.get("sakura_lanyard.jpg", 0.0) },
        {"name": "Pink Lanyard", "image": "pink_lanyard.jpg","price": price_lookup.get("pink_lanyard.jpg", 0.0) },
        {"name": "Pouch(S)", "image": "comestic_pouch_small.jpg","price": price_lookup.get("comestic_pouch_small.jpg", 0.0)},
        {"name": "Pouch(B)", "image": "comestic_pouch_big.jpg","price": price_lookup.get("comestic_pouch_big.jpg", 0.0)},
        {"name": "Recyclable Bag", "image": "recyclable_bag.jpg","price": price_lookup.get("recyclable_bag.jpg", 0.0)},
        {"name": "Flower Dome", "image": "flower_dome.jpg","price": price_lookup.get("flower_dome.jpg", 0.0)},
        {"name": "Hair Clip", "image": "hairclip.jpg","price": price_lookup.get("hairclip.jpg", 0.0)},
        {"name": "Wallet(Long)", "image": "wallet_long.jpg","price": price_lookup.get("wallet_long.jpg", 0.0)},
        {"name": "Wallet(Short)", "image": "wallet_short.jpg","price": price_lookup.get("wallet_short.jpg", 0.0)},
        {"name": "Earrings", "image": "earrings.jpg","price": price_lookup.get("earrings.jpg", 0.0)},
        {"name": "Taobao T-shirts", "image": "taobao_tshirt.jpg","price": price_lookup.get("taobao_tshirt.jpg", 0.0)},
        {"name": "Dresses", "image": "dresses.jpg","price": price_lookup.get("dresses.jpg", 0.0)}
    
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

            # Quantity input
            qty_input = st.text_input(
                f"Quantity ({product['name']})",
                value="1",
                key=f"qty_{product['name']}",
                max_chars=3
            )

            # Validate quantity
            try:
                qty = int(qty_input)
                if qty <= 0:
                    st.warning("Quantity must be at least 1.")
                    continue
            except ValueError:
                st.error("Please enter a valid integer for quantity.")
                continue

            # Button to add order
            if st.button(f"Select {product['name']}", key=f"btn_{product['name']}"):
                price_at_order = price_lookup[product["image"]]
                new_row = pd.DataFrame(
                    [[product["name"], qty, current_time , price_at_order]],
                    columns=["Item", "Quantity", "Timestamp", "Price Sold for"]
                )
                # Combine old + new rows
                updated_df = pd.concat([df, new_row], ignore_index=True)
                #updated_df = pd.concat([df, new_row], ignore_index=True)
                conn.update(worksheet="Orders", data=updated_df)  # uncomment in real app

                # Flash message (non-blocking)
                msg_placeholder = st.empty()
                msg_placeholder.success(f"Added {qty} × {product['name']} (${price_at_order*qty:.2f}) to Google Sheets!")

                #Wait 10 seconds
                time.sleep(1)
                #Clear the message
                msg_placeholder.empty()
                # # Optional: auto-clear after 10 seconds using JS (better than time.sleep)
                # st.markdown(
                #     """
                #     <script>
                #     setTimeout(function() {
                #         const messages = window.parent.document.querySelectorAll(".stAlert");
                #         messages.forEach(msg => msg.remove());
                #     }, 1000);
                #     </script>
                #     """,
                #     unsafe_allow_html=True
                # )
            # #Quantity controls
            # # Text input for quantity
            # qty_input = st.text_input(
            #     f"Quantity ({product["name"]})",
            #     value="1",
            #     key=f"qty_{product["name"]}",
            #     max_chars=3
            # )
            # # --- Data validation ---
            # try:
            #     qty = int(qty_input)
            #     if qty <= 0:
            #         st.warning("Quantity must be at least 1.")
            #     else:
                    
            #         if st.button(f"Select {product['name']}", key=product["name"]):
            #             # --- Record the price at the time of order ---
            #             name_product = product['image']
            #             price_at_order = price_lookup[name_product]
            #             new_row = pd.DataFrame(
            #                 [[product["name"],int(qty_input), pd.Timestamp.now(), price_at_order]],
            #                 columns=["Item", "Quantity", "Timestamp", "Price Sold for"]
            #             )
            #             updated_df = pd.concat([df, new_row], ignore_index=True)
            #             conn.update(worksheet="Orders", data=updated_df)
            #             # Create a placeholder container
            #             message_placeholder = st.empty()

            #             # Show success message
            #             message_placeholder.success(f"Added {product['name']} to Google Sheets!")

            #             # Wait 10 seconds
            #             time.sleep(1)

            #             # Clear the message
            #             message_placeholder.empty()
            #             #st.success(f"Added {product['name']} to Google Sheets!")
            # except ValueError:
            #     st.error("Please enter a valid integer for quantity.")
            #     qty = None  # prevent adding invalid input
            

if __name__ == '__main__':
    main()
    