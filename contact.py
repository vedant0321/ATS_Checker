import streamlit as st

# Contact page styles
CONTACT_PAGE_STYLES = """
<style>
[data-testid="stAppViewContainer"] {
  background: linear-gradient(135deg, #000000 30%, #2e2e70 100%);
}
[data-testid="stHeader"] {
  background-color: rgba(0, 0, 0, 0) !important;
}
.contact-heading {
    font-size: 48px;
    font-weight: bold;
    margin-bottom: 30px;
    color: white;
    text-align: center;
}
.contact-form {
    background-color: #1a1a40;
    padding: 20px;
    border-radius: 10px;
    color: white;
    font-size: 16px;
}
.stButton > button {
    height: 45px;
    width: 100%;
    background-color: #6A5ACD;
    color: white;
    border-radius: 10px;
    font-size: 18px;
    margin: 10px 0;
}
.contact-details {
    background-color: #1a1a40;
    padding: 20px;
    border-radius: 10px;
    color: white;
    font-size: 16px;
    margin-top: 30px;
}
</style>
"""

def contact():
    st.markdown(CONTACT_PAGE_STYLES, unsafe_allow_html=True)
    st.markdown("<h1 class='contact-heading'>Contact Us</h1>", unsafe_allow_html=True)

    # Contact form
    with st.form(key="contact_form", clear_on_submit=True):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        message = st.text_area("Your Message", height=150)
        
        submit_button = st.form_submit_button("Submit")

    # If the form is submitted
    if submit_button:
        if name and email and message:
            st.success("Thank you for contacting us. We will get back to you soon.")
        else:
            st.warning("Please fill out all the fields before submitting.")
    
    # Developer contact details
    st.markdown("<h2 class='contact-heading'>Feel free to contact us:</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div class="contact-details">
        <p><strong>Vedant Birewar</strong><br>
        Phone: 94202777590<br>
        Email: [Your Email Here]</p>
        <p><strong>Om Wanjari</strong><br>
        Phone: 7620495883<br>
        Email: [Your Email Here]</p>
    </div>
    """, unsafe_allow_html=True)

def main():
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = "Home"

    page_functions = {
        "Home": home,  # Make sure to define home() function in the previous script
        "Student": student_page,  # student_page function from your original script
        "Admin": admin_page,  # admin_page function from your original script
        "Contact": contact_page  # Contact page
    }

    page_functions[st.session_state.selected_page]()

if __name__ == "__main__":
    main()
