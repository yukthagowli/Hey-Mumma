import streamlit as st
from streamlit_option_menu import option_menu
import pickle
import warnings
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import calendar
from database.database import verify_user, add_user, get_user_info, update_user_info, check_profile_completed
from utils.pregnancy_tracker import calculate_pregnancy_info, get_trimester_milestones
from utils.pregnancy_diet import get_dietary_recommendations, get_pregnancy_data_by_week, get_diet_plan
from utils.fetal_development import (get_fetal_development_info, get_development_milestones,
                                   get_weekly_exercises, get_nutrition_tips, get_image_path,
                                   get_placeholder_html)
import folium
from streamlit_folium import folium_static
import os

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'page' not in st.session_state:
    st.session_state.page = 'main'  # main, signup, login, profile_setup
if 'signup_success' not in st.session_state:
    st.session_state.signup_success = False

# Load models
maternal_model = pickle.load(open("model/finalized_maternal_model.sav",'rb'))
fetal_model = pickle.load(open("model/fetal_health_classifier.sav",'rb'))

# Custom CSS for modern UI and 3D effects
st.markdown("""
<style>
    /* Modern color scheme and gradients */
    .stApp {
        background: linear-gradient(135deg, #1A1A1A 0%, #000000 100%);
    }
    
    /* Text color for all elements */
    .stMarkdown, .stText, p, span, label, div {
        color: #FFFFFF !important;
    }
    
    /* 3D Card effect for sections */
    div.css-1r6slb0.e1tzin5v2 {
        background: linear-gradient(135deg, #2C2C2C 0%, #1A1A1A 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2), 0 6px 6px rgba(0,0,0,0.2);
        transform: perspective(1000px) rotateX(2deg);
        transition: all 0.3s ease;
    }
    
    div.css-1r6slb0.e1tzin5v2:hover {
        transform: perspective(1000px) rotateX(0deg);
        box-shadow: 0 15px 30px rgba(0,0,0,0.25), 0 8px 8px rgba(0,0,0,0.22);
    }
    
    /* Modern buttons */
    .stButton > button {
        background: linear-gradient(45deg, #2C2C2C, #1A1A1A);
        color: #FFFFFF;
        border-radius: 10px;
        padding: 0.5rem 2rem;
        border: none;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        background: linear-gradient(45deg, #1A1A1A, #000000);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1A1A1A 0%, #000000 100%);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        font-weight: bold;
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        background: linear-gradient(135deg, #2C2C2C 0%, #1A1A1A 100%) !important;
        border-radius: 10px;
        border: 2px solid #1A1A1A;
        padding: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        color: #FFFFFF !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #FFFFFF;
        box-shadow: 0 2px 15px rgba(255,255,255,0.2);
    }
    
    /* Images */
    img {
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
    }
    
    img:hover {
        transform: scale(1.02);
    }

    /* Select box text color */
    .stSelectbox label, .stSelectbox div {
        color: #FFFFFF !important;
    }

    /* Radio button text color */
    .stRadio label {
        color: #FFFFFF !important;
    }

    /* Option menu background */
    .stSelectbox > div > div {
        background: linear-gradient(135deg, #2C2C2C 0%, #1A1A1A 100%) !important;
        color: #FFFFFF !important;
    }

    /* Make sure text is visible on backgrounds */
    .css-1r6slb0.e1tzin5v2 {
        background: rgba(26, 26, 26, 0.9) !important;
    }

    .stTextInput > div > div > input {
        background: rgba(26, 26, 26, 0.9) !important;
    }

    .stButton > button {
        background: rgba(26, 26, 26, 0.9) !important;
    }

    .stSelectbox > div > div {
        background: rgba(26, 26, 26, 0.9) !important;
    }

    /* Additional styles for better visibility */
    .stTextInput > div > div > input::placeholder {
        color: #CCCCCC !important;
    }

    .stSelectbox > div > div > div {
        color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)

class MaternalHealthDashboard:
    def __init__(self, api_endpoint):
        self.api_endpoint = api_endpoint
        try:
            self.df = pd.read_csv(api_endpoint)
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            self.df = pd.DataFrame()  # Empty DataFrame as fallback
    
    def create_bubble_chart(self):
        if self.df.empty:
            st.warning("No data available for visualization")
            return
        
        # Create bubble chart
        fig = px.scatter(
            self.df,
            x='State/UT',
            y='Achievement during April to June - Total Institutional Deliveries - (2019-20) - (B)',
            size='Achievement during April to June - Total Institutional Deliveries - (2019-20) - (B)',
            color='Achievement during April to June - Total Institutional Deliveries - (2019-20) - (B)',
            hover_name='State/UT',
            title='Institutional Deliveries by State (2019-20)',
            labels={
                'State/UT': 'State',
                'Achievement during April to June - Total Institutional Deliveries - (2019-20) - (B)': 'Number of Institutional Deliveries'
            }
        )
        
        # Customize layout
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            showlegend=True,
            height=600
        )
        
        # Display the chart
        st.plotly_chart(fig, use_container_width=True)
    
    def create_pie_chart(self):
        if self.df.empty:
            st.warning("No data available for visualization")
            return
        
        # Calculate total deliveries by state
        state_totals = self.df.groupby('State/UT')['Achievement during April to June - Total Institutional Deliveries - (2019-20) - (B)'].sum().reset_index()
        
        # Create pie chart
        fig = px.pie(
            state_totals,
            values='Achievement during April to June - Total Institutional Deliveries - (2019-20) - (B)',
            names='State/UT',
            title='Distribution of Institutional Deliveries by State (2019-20)',
            hole=0.3
        )
        
        # Customize layout
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            showlegend=True,
            height=600
        )
        
        # Display the chart
        st.plotly_chart(fig, use_container_width=True)
    
    def get_bubble_chart_data(self):
        if self.df.empty:
            return "No data available"
        
        # Get top 5 states by number of deliveries
        top_states = self.df.nlargest(5, 'Achievement during April to June - Total Institutional Deliveries - (2019-20) - (B)')
        return f"""Top 5 States by Institutional Deliveries:
{top_states[['State/UT', 'Achievement during April to June - Total Institutional Deliveries - (2019-20) - (B)']].to_string(index=False)}"""
    
    def get_pie_graph_data(self):
        if self.df.empty:
            return "No data available"
        
        # Calculate percentages by state
        state_totals = self.df.groupby('State/UT')['Achievement during April to June - Total Institutional Deliveries - (2019-20) - (B)'].sum()
        total = state_totals.sum()
        percentages = (state_totals / total * 100).round(2)
        
        return f"""Distribution of Institutional Deliveries (%):\n
{percentages.to_string()}"""

def show_main_page():
    st.title("Welcome to Hey Mumma!")
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0; background: rgba(26, 26, 26, 0.9); border-radius: 10px;'>
            <h1 style='color: #FFFFFF; margin-bottom: 2rem;'>Your Pregnancy Journey Starts Here</h1>
            <p style='color: #FFFFFF; font-size: 1.2em;'>Track your pregnancy journey with our comprehensive tools and predictions</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login", use_container_width=True):
            st.session_state.page = 'login'
            st.rerun()
    
    with col2:
        if st.button("Sign Up", use_container_width=True):
            st.session_state.page = 'signup'
            st.rerun()

def show_signup_page():
    st.title("Create Your Account")
    
    with st.form("signup_form"):
        email = st.text_input("Email")
        name = st.text_input("Full Name")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        submitted = st.form_submit_button("Sign Up")
        
        if submitted:
            if password != confirm_password:
                st.error("Passwords don't match!")
            elif not email or not name or not password:
                st.error("Please fill in all fields!")
            else:
                # Create user with minimal info first
                success = add_user(email, name, password)
                if success:
                    st.session_state.user_email = email
                    st.session_state.signup_success = True
                    st.success("Account created successfully! Please complete your profile.")
                    st.session_state.page = 'profile_setup'
                    st.rerun()
                else:
                    st.error("Email already exists!")
    
    if st.button("Back to Main"):
        st.session_state.page = 'main'
        st.rerun()

def show_login_page():
    st.title("Login to Your Account")
    
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        submitted = st.form_submit_button("Login")
        
        if submitted:
            user = verify_user(email, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.user_email = email
                
                # Check if profile is completed
                if not check_profile_completed(email):
                    st.session_state.page = 'profile_setup'
                else:
                    st.session_state.page = 'home'
                st.rerun()
            else:
                st.error("Invalid email or password")
    
    if st.button("Back to Main"):
        st.session_state.page = 'main'
        st.rerun()

def show_profile_setup():
    st.title("Complete Your Profile")
    st.markdown("Please provide some information to help us personalize your experience")
    
    with st.form("profile_form"):
        age = st.number_input("Age", min_value=18, max_value=50)
        height = st.number_input("Height (cm)", min_value=100, max_value=200)
        weight = st.number_input("Weight (kg)", min_value=30, max_value=150)
        pregnancies = st.number_input("Number of Pregnancies", min_value=0, max_value=10)
        due_date = st.date_input("Expected Due Date")
        
        submitted = st.form_submit_button("Complete Profile")
        
        if submitted:
            update_user_info(
                st.session_state.user_email,
                age=age,
                height=height,
                weight=weight,
                pregnancies=pregnancies,
                due_date=due_date.strftime('%Y-%m-%d')
            )
            st.success("Profile completed successfully!")
            st.session_state.page = 'home'
            st.rerun()

def show_home_page():
    user_info = get_user_info(st.session_state.user_email)
    if not user_info:
        st.error("User information not found")
        return
    
    st.title(f"Welcome, {user_info['name']}!")
    
    # Display welcome image
    st.image("images/image1.webp", use_container_width=True)
    
    # Check if profile is completed
    if not check_profile_completed(st.session_state.user_email):
        st.warning("Please complete your profile to access all features")
        show_profile_setup()
        return
    
    # Calculate pregnancy information only if due date is available
    if user_info['due_date']:
        pregnancy_info = calculate_pregnancy_info(user_info['due_date'])
        
        # Display pregnancy progress
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Weeks Pregnant", f"{pregnancy_info['weeks_pregnant']} weeks")
        with col2:
            st.metric("Days Until Due Date", f"{pregnancy_info['days_remaining']} days")
        with col3:
            st.metric("Current Trimester", f"{pregnancy_info['current_trimester']}")
        
        # Pregnancy Timeline
        st.subheader("Your Pregnancy Timeline")
        trimester_dates = pregnancy_info['trimester_dates']
        
        # Create a calendar view
        current_date = datetime.now()
        due_date = datetime.strptime(user_info['due_date'], '%Y-%m-%d')
        
        # Display calendar for the next few months until due date
        months_to_show = (due_date.year - current_date.year) * 12 + due_date.month - current_date.month + 1
        
        for i in range(months_to_show):
            display_date = current_date + timedelta(days=i*30)
            st.write(f"### {display_date.strftime('%B %Y')}")
            
            # Create calendar grid
            month_calendar = calendar.monthcalendar(display_date.year, display_date.month)
            
            # Display calendar with colored backgrounds for trimesters
            cal_html = '<table style="width: 100%; border-collapse: collapse;">'
            cal_html += '<tr><th>Mon</th><th>Tue</th><th>Wed</th><th>Thu</th><th>Fri</th><th>Sat</th><th>Sun</th></tr>'
            
            for week in month_calendar:
                cal_html += '<tr>'
                for day in week:
                    if day == 0:
                        cal_html += '<td style="padding: 10px; border: 1px solid #444;"></td>'
                    else:
                        current_cell_date = datetime(display_date.year, display_date.month, day)
                        cell_date_str = current_cell_date.strftime('%Y-%m-%d')
                        
                        # Determine cell color based on trimester
                        if cell_date_str <= trimester_dates['first']['end']:
                            bg_color = 'rgba(135, 206, 235, 0.3)'  # Light blue for first trimester
                        elif cell_date_str <= trimester_dates['second']['end']:
                            bg_color = 'rgba(221, 160, 221, 0.3)'  # Light purple for second trimester
                        else:
                            bg_color = 'rgba(255, 182, 193, 0.3)'  # Light pink for third trimester
                        
                        # Highlight current day
                        if current_cell_date.date() == current_date.date():
                            border_style = '3px solid #FF69B4'
                        else:
                            border_style = '1px solid #444'
                        
                        cal_html += f'<td style="padding: 10px; border: {border_style}; background-color: {bg_color};">{day}</td>'
                cal_html += '</tr>'
            cal_html += '</table>'
            
            st.markdown(cal_html, unsafe_allow_html=True)
        
        # Display trimester milestones
        st.subheader(f"Current Trimester {pregnancy_info['current_trimester']} Milestones")
        milestones = get_trimester_milestones(pregnancy_info['current_trimester'])
        for milestone in milestones:
            st.write(f"• {milestone}")
    else:
        st.warning("Please complete your profile to view pregnancy timeline")

# Main app logic
if not st.session_state.logged_in:
    if st.session_state.page == 'main':
        show_main_page()
    elif st.session_state.page == 'signup':
        show_signup_page()
    elif st.session_state.page == 'login':
        show_login_page()
    elif st.session_state.page == 'profile_setup':
        show_profile_setup()
else:
    with st.sidebar:
        selected = option_menu('Hey Mumma!',
                             ['Home',
                              'Pregnancy Risk Prediction',
                              'Fetal Health Prediction',
                              'Pregnancy Guide',
                              'Fetal Development',
                              'Dashboard',
                              'Nearest Hospitals',
                              'Logout'],
                             icons=['house','hospital','capsule-pill', 'book', 'baby-carriage', 'clipboard-data', 'map', 'box-arrow-right'],
                             default_index=0)
        
        if selected == 'Logout':
            st.session_state.logged_in = False
            st.session_state.user_email = None
            st.session_state.page = 'main'
            st.rerun()
    
    if selected == 'Home':
        show_home_page()
    elif selected == 'Pregnancy Risk Prediction':
        st.title('Pregnancy Risk Prediction')
        content = "Predicting the risk in pregnancy involves analyzing several parameters, including age, blood sugar levels, blood pressure, and other relevant factors. By evaluating these parameters, we can assess potential risks and make informed predictions regarding the pregnancy's health"
        st.markdown(f"<div style='white-space: pre-wrap;'><b>{content}</b></div></br>", unsafe_allow_html=True)
        
        # getting the input data from the user
        col1, col2, col3 = st.columns(3)
        
        with col1:
            age = st.text_input('Age of the Person', key = "age")
            
        with col2:
            diastolicBP = st.text_input('diastolicBP in mmHg')
        
        with col3:
            BS = st.text_input('Blood glucose in mmol/L')
        
        with col1:
            bodyTemp = st.text_input('Body Temperature in Fahrenheit')

        with col2:
            heartRate = st.text_input('Heart rate in beats per minute')
        
        riskLevel=""
        predicted_risk = [0] 
        # creating a button for Prediction
        with col1:
            if st.button('Predict Pregnancy Risk'):
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    predicted_risk = maternal_model.predict([[age, diastolicBP, BS, bodyTemp, heartRate]])
                # st
                st.subheader("Risk Level:")
                if predicted_risk[0] == 0:
                    st.markdown('<bold><p style="font-weight: bold; font-size: 20px; color: green;">Low Risk</p></bold>', unsafe_allow_html=True)
                elif predicted_risk[0] == 1:
                    st.markdown('<bold><p style="font-weight: bold; font-size: 20px; color: orange;">Medium Risk</p></Bold>', unsafe_allow_html=True)
                else:
                    st.markdown('<bold><p style="font-weight: bold; font-size: 20px; color: red;">High Risk</p><bold>', unsafe_allow_html=True)
        with col2:
            if st.button("Clear"): 
                st.rerun()

    elif selected == 'Fetal Health Prediction':
        st.title('Fetal Health Prediction')
        content = "Cardiotocograms (CTGs) are a simple and cost accessible option to assess fetal health, allowing healthcare professionals to take action in order to prevent child and maternal mortality"
        st.markdown(f"<div style='white-space: pre-wrap;'><b>{content}</b></div></br>", unsafe_allow_html=True)
        # getting the input data from the user
        col1, col2, col3 = st.columns(3)
        
        with col1:
            BaselineValue = st.text_input('Baseline Value')
            
        with col2:
            Accelerations = st.text_input('Accelerations')
        
        with col3:
            fetal_movement = st.text_input('Fetal Movement')
        
        with col1:
            uterine_contractions = st.text_input('Uterine Contractions')

        with col2:
            light_decelerations = st.text_input('Light Decelerations')
        
        with col3:
            severe_decelerations = st.text_input('Severe Decelerations')

        with col1:
            prolongued_decelerations = st.text_input('Prolongued Decelerations')
            
        with col2:
            abnormal_short_term_variability = st.text_input('Abnormal Short Term Variability')
        
        with col3:
            mean_value_of_short_term_variability = st.text_input('Mean Value Of Short Term Variability')
        
        with col1:
            percentage_of_time_with_abnormal_long_term_variability = st.text_input('Percentage Of Time With ALTV')

        with col2:
            mean_value_of_long_term_variability = st.text_input('Mean Value Long Term Variability')
        
        with col3:
            histogram_width = st.text_input('Histogram Width')

        with col1:
            histogram_min = st.text_input('Histogram Min')
            
        with col2:
            histogram_max = st.text_input('Histogram Max')
        
        with col3:
            histogram_number_of_peaks = st.text_input('Histogram Number Of Peaks')
        
        with col1:
            histogram_number_of_zeroes = st.text_input('Histogram Number Of Zeroes')

        with col2:
            histogram_mode = st.text_input('Histogram Mode')
        
        with col3:
            histogram_mean = st.text_input('Histogram Mean')
        
        with col1:
            histogram_median = st.text_input('Histogram Median')

        with col2:
            histogram_variance = st.text_input('Histogram Variance')
        
        with col3:
            histogram_tendency = st.text_input('Histogram Tendency')
        
        # creating a button for Prediction
        st.markdown('</br>', unsafe_allow_html=True)
        with col1:
            if st.button('Predict Pregnancy Risk'):
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    predicted_risk = fetal_model.predict([[BaselineValue, Accelerations, fetal_movement,
       uterine_contractions, light_decelerations, severe_decelerations,
       prolongued_decelerations, abnormal_short_term_variability,
       mean_value_of_short_term_variability,
       percentage_of_time_with_abnormal_long_term_variability,
       mean_value_of_long_term_variability, histogram_width,
       histogram_min, histogram_max, histogram_number_of_peaks,
       histogram_number_of_zeroes, histogram_mode, histogram_mean,
       histogram_median, histogram_variance, histogram_tendency]])
                # st.subheader("Risk Level:")
                st.markdown('</br>', unsafe_allow_html=True)
                if predicted_risk[0] == 0:
                    st.markdown('<bold><p style="font-weight: bold; font-size: 20px; color: green;">Result  Comes to be  Normal</p></bold>', unsafe_allow_html=True)
                elif predicted_risk[0] == 1:
                    st.markdown('<bold><p style="font-weight: bold; font-size: 20px; color: orange;">Result  Comes to be  Suspect</p></Bold>', unsafe_allow_html=True)
                else:
                    st.markdown('<bold><p style="font-weight: bold; font-size: 20px; color: red;">Result  Comes to be  Pathological</p><bold>', unsafe_allow_html=True)
        with col2:
            if st.button("Clear"): 
                st.rerun()

    elif selected == 'Pregnancy Guide':
        st.title('Pregnancy Guide & Dietary Recommendations')
        
        # Get user's pregnancy information
        user_info = get_user_info(st.session_state.user_email)
        if not user_info or not user_info['due_date']:
            st.warning("Please complete your profile with due date information to view personalized recommendations")
        else:
            pregnancy_info = calculate_pregnancy_info(user_info['due_date'])
            current_week = pregnancy_info['weeks_pregnant']
            
            # Display current pregnancy week
            st.header(f"Week {current_week} of Pregnancy")
            
            # Get recommendations and pregnancy data
            diet_recommendations = get_dietary_recommendations(current_week)
            pregnancy_data = get_pregnancy_data_by_week(current_week)
            
            # Create two columns for layout
            col1, col2 = st.columns(2)
            
            with col1:
                # Pregnancy Development Section
                st.subheader("Baby's Development")
                st.markdown(f"""
                **Size:** {pregnancy_data['baby_size']}
                
                **Development:** {pregnancy_data['baby_development']}
                
                **Your Changes:** {pregnancy_data['mother_changes']}
                
                **Important Notes:** {pregnancy_data['important_notes']}
                """)
            
            with col2:
                # Dietary Recommendations Section
                st.subheader("Dietary Recommendations")
                
                with st.expander("Foods to Eat", expanded=True):
                    for food in diet_recommendations['foods_to_eat']:
                        st.markdown(f"• {food}")
                
                with st.expander("Foods to Avoid"):
                    for food in diet_recommendations['foods_to_avoid']:
                        st.markdown(f"• {food}")
                
                with st.expander("Essential Nutrients"):
                    for nutrient in diet_recommendations['nutrients_needed']:
                        st.markdown(f"• {nutrient}")
                
                with st.expander("Helpful Tips"):
                    for tip in diet_recommendations['tips']:
                        st.markdown(f"• {tip}")
            
            # Timeline visualization
            st.subheader("Pregnancy Timeline")
            total_weeks = 40
            progress = (current_week / total_weeks) * 100
            
            # Create a progress bar with custom styling
            st.markdown(f"""
            <style>
            .stProgress > div > div > div > div {{
                background-image: linear-gradient(to right, pink, purple);
            }}
            </style>
            """, unsafe_allow_html=True)
            
            st.progress(min(progress/100, 1.0))
            st.markdown(f"**{progress:.1f}% Complete** ({40-current_week} weeks remaining)")
            
            # Weekly weight gain chart
            st.subheader("Recommended Weight Gain")
            
            # Calculate recommended weight gain based on current week
            if current_week <= 13:
                recommended_gain = "1-4.5 pounds total"
            elif current_week <= 26:
                recommended_gain = "1-2 pounds per week"
            else:
                recommended_gain = "0.5-1 pound per week"
            
            st.info(f"Recommended weight gain for week {current_week}: {recommended_gain}")
            
            # Additional resources
            st.subheader("Additional Resources")
            st.markdown("""
            * 🏥 Schedule regular check-ups with your healthcare provider
            * 📝 Keep a food diary to track your nutrition
            * 💪 Consider pregnancy-safe exercises
            * 🧘‍♀️ Practice relaxation techniques
            * 📚 Join childbirth education classes
            """)
            
            # Daily Diet Plan
            st.subheader("📋 Your Daily Diet Plan")
            diet_plan = get_diet_plan(current_week)
            
            # Create tabs for different meal times
            meal_tabs = st.tabs(["Breakfast", "Morning Snack", "Lunch", "Evening Snack", "Dinner", "Bedtime"])
            
            # Breakfast
            with meal_tabs[0]:
                st.markdown("### 🌅 Breakfast")
                for item in diet_plan["breakfast"]:
                    st.markdown(f"• {item}")
                st.info("Best time: Within 1 hour of waking up")
            
            # Morning Snack
            with meal_tabs[1]:
                st.markdown("### 🥪 Morning Snack")
                for item in diet_plan["morning_snack"]:
                    st.markdown(f"• {item}")
                st.info("Best time: 2-3 hours after breakfast")
            
            # Lunch
            with meal_tabs[2]:
                st.markdown("### 🍽️ Lunch")
                for item in diet_plan["lunch"]:
                    st.markdown(f"• {item}")
                st.info("Best time: 2-3 hours after morning snack")
            
            # Evening Snack
            with meal_tabs[3]:
                st.markdown("### 🥗 Evening Snack")
                for item in diet_plan["evening_snack"]:
                    st.markdown(f"• {item}")
                st.info("Best time: 2-3 hours after lunch")
            
            # Dinner
            with meal_tabs[4]:
                st.markdown("### 🍲 Dinner")
                for item in diet_plan["dinner"]:
                    st.markdown(f"• {item}")
                st.info("Best time: 2-3 hours after evening snack")
            
            # Bedtime Snack
            with meal_tabs[5]:
                st.markdown("### 🌙 Bedtime Snack")
                for item in diet_plan["bedtime_snack"]:
                    st.markdown(f"• {item}")
                st.info("Best time: 30 minutes before bed")
            
            # Diet Tips
            st.markdown("""
            ---
            ### 💡 Important Diet Tips
            1. **Stay Hydrated**: Drink 8-10 glasses of water daily
            2. **Eat Frequently**: Have small meals every 2-3 hours
            3. **Listen to Your Body**: Eat when hungry, rest when tired
            4. **Food Safety**: Ensure all foods are well-cooked and fresh
            5. **Balanced Nutrition**: Include proteins, carbs, healthy fats, vitamins, and minerals
            """)

    elif selected == 'Fetal Development':
        st.title('Fetal Development Week by Week')
        st.markdown("""
        Track your baby's growth and development throughout your pregnancy journey.
        Learn about the amazing changes happening each week.
        """)
        
        # Get user's pregnancy information
        user_info = get_user_info(st.session_state.user_email)
        
        if not user_info or 'due_date' not in user_info:
            st.warning("Please complete your profile with your due date to see personalized information.")
        else:
            pregnancy_info = calculate_pregnancy_info(user_info['due_date'])
            current_week = pregnancy_info['weeks_pregnant']
            
            # Display current week prominently
            st.subheader(f"You are currently in Week {current_week}")
            
            # Week selector
            selected_week = st.slider("Select a week to view details:", 1, 40, current_week)
            
            # Get development information for selected week
            week_info = get_fetal_development_info(selected_week)
            
            # Create tabs for different aspects of development
            main_tabs = st.tabs(["Development", "Exercise & Nutrition", "Tips & Guidelines"])
            
            with main_tabs[0]:  # Development Tab
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"### {week_info['title']}")
                    
                    # Size information with comparison
                    st.markdown("#### Baby's Size")
                    size_col1, size_col2 = st.columns(2)
                    with size_col1:
                        st.markdown(f"**Measurement:** {week_info['size']}")
                        if week_info['weight'] != "N/A":
                            st.markdown(f"**Weight:** {week_info['weight']}")
                    with size_col2:
                        if week_info['size_comparison'] != "N/A":
                            st.markdown(f"**Size comparison:** About the size of a {week_info['size_comparison']}")
                    
                    st.markdown("### Key Developments")
                    for highlight in week_info['highlights']:
                        st.markdown(f"• {highlight}")
                    
                    st.markdown("### What to Expect")
                    for expectation in week_info['what_to_expect']:
                        st.markdown(f"• {expectation}")
                    
                    st.markdown("### Detailed Information")
                    st.write(week_info['details'])
                
                with col2:
                    # Display fetal development image or placeholder
                    image_path = get_image_path(selected_week)
                    if image_path and os.path.exists(image_path):
                        try:
                            st.image(image_path, 
                                   caption=f"Week {selected_week} Development",
                                   use_container_width=True)
                        except Exception:
                            st.markdown(get_placeholder_html(selected_week), unsafe_allow_html=True)
                    else:
                        st.markdown(get_placeholder_html(selected_week), unsafe_allow_html=True)
            
            with main_tabs[1]:  # Exercise & Nutrition Tab
                exercise_col, nutrition_col = st.columns(2)
                
                with exercise_col:
                    st.markdown("### Recommended Exercises")
                    exercises = get_weekly_exercises(selected_week)
                    for exercise in exercises:
                        st.markdown(f"• {exercise}")
                
                with nutrition_col:
                    st.markdown("### Nutrition Guidelines")
                    nutrition = get_nutrition_tips(selected_week)
                    
                    st.markdown("#### Key Nutrients to Focus On")
                    for nutrient in nutrition['focus_nutrients']:
                        st.markdown(f"• {nutrient}")
                    
                    st.markdown("#### Recommended Foods")
                    for food in nutrition['recommended_foods']:
                        st.markdown(f"• {food}")
                    
                    with st.expander("Foods to Avoid"):
                        for food in nutrition['foods_to_avoid']:
                            st.markdown(f"• {food}")
            
            with main_tabs[2]:  # Tips & Guidelines Tab
                st.markdown("### Weekly Tips")
                for tip in week_info['tips']:
                    st.markdown(f"• {tip}")
                
                # Display development milestones
                st.markdown("### Development Milestones")
                milestone_tabs = st.tabs(["First Trimester", "Second Trimester", "Third Trimester"])
                milestones = get_development_milestones()
                
                for i, (trimester, milestone_tab) in enumerate(zip(milestones.keys(), milestone_tabs)):
                    with milestone_tab:
                        for milestone in milestones[trimester]:
                            st.markdown(f"• {milestone}")
                
                # Additional resources
                st.markdown("### Additional Resources")
                st.markdown("""
                - 📚 [Pregnancy Books and Reading Materials](https://www.acog.org/womens-health/resources-for-patients)
                - 🏥 [Find a Healthcare Provider](https://www.acog.org/womens-health/find-an-ob-gyn)
                - 🎓 [Childbirth Classes](https://www.lamaze.org/find-a-lamaze-class)
                - 🤰 [Pregnancy Support Groups](https://www.postpartum.net/get-help/support-groups/)
                """)
                
    elif selected == 'Dashboard':
        api_key = "579b464db66ec23bdd00000139b0d95a6ee4441c5f37eeae13f3a0b2"
        api_endpoint = api_endpoint= f"https://api.data.gov.in/resource/6d6a373a-4529-43e0-9cff-f39aa8aa5957?api-key={api_key}&format=csv"
        st.header("Dashboard")
        content = "Our interactive dashboard offers a comprehensive visual representation of maternal health achievements across diverse regions. The featured chart provides insights into the performance of each region concerning institutional deliveries compared to their assessed needs. It serves as a dynamic tool for assessing healthcare effectiveness, allowing users to quickly gauge the success of maternal health initiatives."
        st.markdown(f"<div style='white-space: pre-wrap;'><b>{content}</b></div></br>", unsafe_allow_html=True)

        dashboard = MaternalHealthDashboard(api_endpoint)
        dashboard.create_bubble_chart()
        with st.expander("Show More"):
        # Display a portion of the data
            content = dashboard.get_bubble_chart_data()
            st.markdown(f"<div style='white-space: pre-wrap;'><b>{content}</b></div>", unsafe_allow_html=True)

        dashboard.create_pie_chart()
        with st.expander("Show More"):
        # Display a portion of the data
            content = dashboard.get_pie_graph_data()
            st.markdown(f"<div style='white-space: pre-wrap;'><b>{content}</b></div>", unsafe_allow_html=True)

    elif selected == 'Nearest Hospitals':
        st.title('Find Nearest Hospitals')
        st.markdown("""
        ### Search for hospitals near your location
        Use this interactive map to find hospitals in your area. The map will open in Google Maps where you can:
        - View detailed information about each hospital
        - Get directions
        - Read reviews
        - Contact the hospital directly
        """)
        
        # Create a button that opens Google Maps search for hospitals
        if st.button('Search Nearby Hospitals on Google Maps'):
            # Open Google Maps search for hospitals
            maps_url = "https://www.google.com/maps/search/hospitals+near+me"
            st.markdown(f'<a href="{maps_url}" target="_blank">Click here if the map doesn\'t open automatically</a>', unsafe_allow_html=True)
            st.markdown(f'<script>window.open("{maps_url}", "_blank");</script>', unsafe_allow_html=True)
        
        # Create a default map centered at a location (can be customized based on user's location)
        m = folium.Map(location=[20.5937, 78.9629], zoom_start=4)  # Centered at India
        folium_static(m)
        
        st.info("""
        💡 Tips:
        - Click the button above to search for hospitals near your current location
        - The map will open in a new tab in Google Maps
        - You can filter results by ratings, distance, and currently open facilities
        - Save important hospital contacts for emergency situations
        """)
