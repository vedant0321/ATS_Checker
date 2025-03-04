import streamlit as st
import requests
from PIL import Image

def contact():
    st.title("Contact Us")
    # Developer Cards Section
    st.subheader("Meet Our Team")
    col1,col2,col3= st.columns(3,gap='medium',border=True)
    with col1:
        st.image(r"image\om.png")
        st.write("Om Wanjari")
    with col2:
        st.image(r"image\vedant.png")
        st.write("Vedant Birewar")
    with col3:
        st.image(r"image\shreya.png")
        st.write("Shreya Yadawar")
    
    col1,col2,col3= st.columns(3,gap='medium',border=True)
    with col1:
        st.image(r"image\shivam.png")
        st.write("Shivam Durbule")
    with col2:
        st.image(r"image\vivek.png")
        st.write("Vivek Togarvar")
        
    with col3:
        st.title("")
    st.components.v1.html("""
        <div style="margin: 20px 0;">
            <script src="https://sheetdb.io/s/f/i0t89k3ew8b6q.js"></script>
        </div>
    """, height=500)
    # st.write("For any queries, please contact us at: ")

if __name__ == "__main__":
    contact()