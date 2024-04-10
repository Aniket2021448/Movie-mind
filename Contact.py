import streamlit as st


def main():
    st.title("CONTACT ME")
    st.markdown("Github: https://github.com/Aniket2021448", unsafe_allow_html=True)
    st.markdown("Linked IN: https://www.linkedin.com/in/aniket-panchal-0a7b3a233/", unsafe_allow_html=True)
    st.markdown("Email: aniketpanchal1257@gmail.com", unsafe_allow_html=True)

    st.markdown("Github repository: https://github.com/Aniket2021448/Movie-recommender-system", unsafe_allow_html=True)
    st.write("THANK YOU FOR CONNECTING")


    
    with st.form("app_selection_form"):
        st.write("Feel free to explore my other apps")
        app_links = {
            "find-the-fake": "https://find-fake-news.streamlit.app/",
            "Comment-Feel": "https://huggingface.co/spaces/GoodML/Comment-Feel"
        }
        selected_app = st.selectbox("Choose an App", list(app_links.keys()))

        submitted_button = st.form_submit_button("Go to App")

    # Handle form submission
    if submitted_button:
        selected_app_url = app_links.get(selected_app)
        if selected_app_url:
            st.success("Redirected successfully!")
            st.markdown(f'<meta http-equiv="refresh" content="0;URL={selected_app_url}">', unsafe_allow_html=True)

    
    # Dropdown menu for other app links

    st.write("In case the apps are down, because of less usage")
    st.write("Kindly reach out to me @ aniketpanchal1257@gmail.com")
    
