# import streamlit as st

# # Set the page configuration
# st.set_page_config(page_title="My Streamlit App", layout="wide")

# # Introductory code block
# st.title("Welcome to My Streamlit App!")
# st.write("This app demonstrates the use of Streamlit for building interactive applications.")
# st.write("Use the sidebar to navigate between different pages.")

# # Define the page titles and import the corresponding modules
# pages = {
#     "Home": "01_homepage",
#     "Health Data": "02_health_data",
#     "Model About": "03_model_about",
#     "Predict Disease": "04_predict_disease"
# }

# # Create a sidebar with a title
# st.sidebar.title("Navigation")

# # Create a radio button for navigation
# selected_page = st.sidebar.radio("Go to", list(pages.keys()))

# # Import and run the selected page function
# if selected_page:
#     module = __import__(f'pages.{pages[selected_page]}', fromlist=['run'])
#     module.run()