import streamlit as st
import streamlit.components.v1 as components

# Function to load the CSS file
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Function to create a slideshow of AI healthcare-related images
def image_slideshow():
    images = [
        "https://img.freepik.com/premium-photo/doctor-using-technology-provide-healthcare_14117-1060619.jpg?w=900",
        "https://img.freepik.com/premium-photo/doctor-analyzes-medical-data-visualizations-modern-hospital_926058-8953.jpg?w=900",
        "https://radiologybusiness.com/sites/default/files/styles/top_stories/public/2018-07/istock-914327272_super.jpg.webp?itok=ErL-cFbb",
        "https://www.knowledgenile.com/wp-content/uploads/brizy/imgs/The-Use-of-AI-in-Healthcare-Opportunities-and-Challenges-789x614x0x106x789x402x1713971981.jpg"
    ]
    
    slideshow_html = """
    <div id="slideshow" class="slideshow-container">
    """
    for img in images:
        slideshow_html += f"""
        <div class="mySlides fade">
            <img src="{img}" style="width:100%">
        </div>
        """

    slideshow_html += """
        </div>
        <style>
            .slideshow-container {
                max-width: 1000px;
                position: relative;
                margin: auto;
            }
            .mySlides {
                display: none;
            }
            .fade {
                animation-name: fade;
                animation-duration: 2s;
            }
            @keyframes fade {
                from {opacity: .4}
                to {opacity: 1}
            }
        </style>
        <script>
            var slideIndex = 0;
            showSlides();
            function showSlides() {
                var i;
                var slides = document.getElementsByClassName("mySlides");
                for (i = 0; i < slides.length; i++) {
                    slides[i].style.display = "none";
                }
                slideIndex++;
                if (slideIndex > slides.length) {
                    slideIndex = 1;
                }
                slides[slideIndex-1].style.display = "block";
                setTimeout(showSlides, 5000); // Change image every 5 seconds
            }
        </script>
    """

    components.html(slideshow_html, height=400)

# Function to create a slideshow of daily health tips
def health_tips_slideshow():
    tips = [
        "Stay hydrated by drinking at least 8 glasses of water a day.",
        "Incorporate more fruits and vegetables into your meals for better nutrition.",
        "Exercise for at least 30 minutes daily to maintain a healthy lifestyle.",
        "Get enough sleep (7-9 hours) to improve your overall health.",
        "Practice mindfulness or meditation to reduce stress."
    ]
    
    tips_html = """
    <div id="tips_slideshow" class="tips-slideshow-container">
    """
    for tip in tips:
        tips_html += f"""
        <div class="tip mySlides fade">
            <p>{tip}</p>
        </div>
        """

    tips_html += """
        </div>
        <style>
            .tips-slideshow-container {
                max-width: 800px;
                margin: auto;
                text-align: center;
            }
            .tip {
                display: none;
                font-size: 1.2em;
                color: #004d40;
                padding: 20px;
                border: 1px solid #00796b;
                border-radius: 8px;
                background-color: #e0f2f1;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }
        </style>
        <script>
            var tipIndex = 0;
            showTips();
            function showTips() {
                var i;
                var tips = document.getElementsByClassName("tip");
                for (i = 0; i < tips.length; i++) {
                    tips[i].style.display = "none";
                }
                tipIndex++;
                if (tipIndex > tips.length) {
                    tipIndex = 1;
                }
                tips[tipIndex-1].style.display = "block";
                setTimeout(showTips, 5000); // Change tip every 5 seconds
            }
        </script>
    """

    components.html(tips_html, height=120)

    # Add a clickable link to an external health tips website
    st.markdown("""
    <div style="text-align: center; margin-top: 5px;"> <!-- Reduced margin-top -->
        <a href="https://www.thehealthsite.com/" target="_blank" style="background-color: #00796b; 
        color: white; padding: 10px 20px; border-radius: 5px; text-decoration: none; font-weight: bold;">
        More Health Tips</a>
    </div>
    """, unsafe_allow_html=True)

# Main function to build the Streamlit app
def main():
    # Load custom CSS
    local_css("app_style.css")

    # Set up the page title and subtitle
    st.title("🌟 Welcome to the Disease Prediction App")
    st.write("""
    Our app uses advanced machine learning models to predict diseases based on your symptoms. 
    Enter your symptoms, and we'll provide you with the most accurate prediction using four powerful models: XGBoost, LightGBM, SVM, and CatBoost.
    """)

    st.sidebar.title("Welcome")
    st.sidebar.write("Select a page above.")

    # Display the slideshow above the "Explore the App" section
    image_slideshow()

    # Display the daily health tips section
    st.write("### 📝 Daily Health Tips")
    st.write("Here are some health tips to help you stay in great shape!")

    # Display the health tips slideshow
    health_tips_slideshow()

    # Add a description for the app
    st.write("### Explore the App")

    # Use a 2-column layout for a more engaging homepage
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔍 Predict Your Disease")
        st.write("""
        Enter your symptoms in the "Predict Disease" section to get predictions from our advanced models. 
        Experience how our ensemble of machine learning models can provide insights into potential health issues based on your symptoms.
        """)
        st.write("👈🏻 **Check the sidebar to start predicting!**")

    with col2:
        st.subheader("📖 About the Models")
        st.write("""
        Discover more about the powerful models that drive our predictions. 
        Learn about XGBoost, LightGBM, SVM, and CatBoost, and understand how they work together to provide accurate disease predictions.
        """)
        st.write("👈🏻 **Check the sidebar for more information!**")

    # Add a creative section for user engagement
    st.write("### 💡 Empowering Your Health Journey")
    st.write("""
    We believe in empowering you with the knowledge to make informed health decisions. 
    Our app is designed to be user-friendly and informative, helping you navigate your health journey with confidence. 
    Feel free to explore and utilize the tools we provide for better health insights!
    """)

if __name__ == "__main__":
    main()
