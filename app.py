import streamlit as st
import requests
import os
import base64
from pathlib import Path
from streamlit_login_auth_ui.widgets import __login__
import warnings
warnings.filterwarnings("ignore")

feedback_dict = {}
feedback_dict['positive'] = {}
feedback_dict['positive']['neutral'] = 'Your neutral expressions maintained a professional tone, keep going on!.'
feedback_dict['positive']['happy'] = 'Your happy demeanor added a positive energy to your presentation. Keep it up!'
feedback_dict['positive']['Confident'] = 'Your confidence shone through in your presentation, making it compelling and convincing.'
feedback_dict['positive']['hand collab'] = 'Your hand collaboration gestures were effective in emphasizing your points and keeping the audience\'s attention.'
feedback_dict['positive']['open palms'] = 'Your use of open palms was excellent, making you appear more approachable and trustworthy.'
feedback_dict['positive']['No eye contact'] = 'Work on making more eye contact to connect better with your audience and hold their attention.'
feedback_dict['negative'] = {}
feedback_dict['negative']['neutral'] = 'Incorporate neutral expressions at times to balance out your emotions and maintain professionalism.'
feedback_dict['negative']['happy'] = 'Try incorporating a happy expression to make your presentation more engaging and relatable.'
feedback_dict['negative']['Confident'] = ' Focus on building your confidence to deliver your presentation more convincingly and effectively.'
feedback_dict['negative']['hand collab'] = 'Consider using more hand collaboration gestures to emphasize key points and keep the audience engaged.'
feedback_dict['negative']['open palms'] = 'Try using open palms to appear more approachable and to foster a sense of trust with your audience.'
feedback_dict['negative']['No eye contact'] = ' Your eye contact was great and helped in maintaining a connection with the audience. Well done!'

# suggestions_dict = {}
# suggestions_dict['positive'] = {}
# suggestions_dict['positive']['neutral'] = 'Your neutral expressions maintained a professional tone, but try adding more variation to keep the audience engaged.'
# suggestions_dict['positive']['happy'] = 'Your happy demeanor added a positive energy to your presentation. Keep it up!'
# suggestions_dict['positive']['Confident'] = 'Your confidence shone through in your presentation, making it compelling and convincing.'
# suggestions_dict['positive']['hand collab'] = 'Your hand collaboration gestures were effective in emphasizing your points and keeping the audience\'s attention.'
# suggestions_dict['positive']['open palms'] = 'Your use of open palms was excellent, making you appear more approachable and trustworthy.'
# suggestions_dict['positive']['No eye contact'] = 'Work on making more eye contact to connect better with your audience and hold their attention.'
# suggestions_dict['negative'] = {}
# suggestions_dict['negative']['neutral'] = 'Incorporate neutral expressions at times to balance out your emotions and maintain professionalism.'
# suggestions_dict['negative']['happy'] = 'Try incorporating a happy expression to make your presentation more engaging and relatable.'
# suggestions_dict['negative']['Confident'] = ' Focus on building your confidence to deliver your presentation more convincingly and effectively.'
# suggestions_dict['negative']['hand collab'] = 'Consider using more hand collaboration gestures to emphasize key points and keep the audience engaged.'
# suggestions_dict['negative']['open palms'] = 'Try using open palms to appear more approachable and to foster a sense of trust with your audience.'
# suggestions_dict['negative']['No eye contact'] = ' Your eye contact was great and helped in maintaining a connection with the audience. Well done!'


def set_bg_hack(main_bg):
    file_extension = os.path.splitext(main_bg)[-1].lower().replace(".", "")
    with open(main_bg, "rb") as f:
        image_data = f.read()
    base64_image = base64.b64encode(image_data).decode()
    
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url(data:image/{file_extension};base64,{base64_image});
            background-size: cover
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Function to save uploaded file
def save_uploaded_file(uploaded_file):
    try:
        save_path = Path.cwd() / uploaded_file.name
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return save_path
    except Exception as e:
        st.error(f"Error saving file: {e}")
        return None

__login__obj = __login__(auth_token = "dk_prod_VB5X9TJFW54WBYNZXKADVK3S42R3", 
                    company_name = "Shims",
                    width = 200, height = 250, 
                    logout_button_name = 'Logout', hide_menu_bool = False, 
                    hide_footer_bool = False, 
                    lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

st.header("PresentPro")



LOGGED_IN = __login__obj.build_login_ui()

if LOGGED_IN == True:
    # set_bg_hack('logo.jpeg')
    st.sidebar.header("PresentPro")
    st.sidebar.image("logo.jpeg", use_column_width=True)
    upload_tab,Practice_tab = st.tabs(["Upload","Practice"])

    with Practice_tab:
        with st.expander('Preview 1'):
            video_url = "https://youtu.be/wU0aFi5avsc?si=o4_N0K_zEWbE_f6H" 
            st.video(video_url)
                
        
        with st.expander('Preview 2'):
            video_url = "https://youtu.be/3xbdyXALMKw?si=AS5b8w_v-SgU2vI0" 
            st.video(video_url)
                
    
    with upload_tab:
        st.header("Welcome....!")
        st.subheader('Receive valuable feedback and suggestions to excel in every presentation', divider='rainbow')
        age = st.text_input("Age", max_chars=3)
        gender = st.selectbox("Gender", ["Select", "Male", "Female", "Other"])
        uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov", "mkv"])
        # conf = st.slider("Confidence parameter", min_value=0.0, max_value=1.0, value=0.25)
        conf = 0.25

        if st.button("Predict"):
            if uploaded_file is not None:
                st.write('Input video:')
                st.video(uploaded_file)
                input_video_file_path = save_uploaded_file(uploaded_file)
                st.write('Output video:')
                if input_video_file_path:
                    with st.spinner('Video prediction...'):
                        api_url = "http://localhost:8000/process_video/"  # Replace with your actual API endpoint
                        payload = {
                            "input_video_file_path": str(input_video_file_path),
                            "conf": conf
                        }
                        
                        response = requests.post(api_url, json=payload)
                        response.raise_for_status()  # Raise an exception for HTTP errors
                    data = response.json()
                    output_video_file_path = data['output_file_path']
                    with open(output_video_file_path, "rb") as video_file:
                        st.video(video_file.read())
                    print(data)

                    with st.expander('Feedback and Suggestions', expanded=True):  # Expanded by default
                        st.markdown(
                            """
                            <style>
                            .stExpander {
                                background-color: white;  /* Set background color to white */
                                font-size: 24px;       /* Adjust font size as needed */
                                font-weight: bold;      /* Make the heading bold */
                                padding: 10px 15px;     /* Add padding for better spacing */
                            }
                            </style>
                            """,
                            unsafe_allow_html=True
                        )

                        for i,j in data['labels'].items():
                            if j >= 0.75:
                                sugg = feedback_dict['positive'][i]
                                # st.write(f'{sugg}')
                            else:
                                sugg = feedback_dict['negative'][i]
                                # st.write(f'{sugg}')
                            st.markdown(f"<h6 style='font-size:22px;'>{sugg}</h6>", unsafe_allow_html=True)

                    st.markdown(
                    """
                    <h6 style='color:red;font-weight:bold;'>
                    <br>
                    <br>
                    <br>
                    <br>
                    <br>
                    <br>
                    <br>
                    DISCLAIMER</h6>
                    <p style='color:red;'>
                    Disclaimer: The feedback and suggestions provided is based on the current capabilities of our model. While we strive to offer accurate and helpful insights, 
                    please note that the model is continually being improved.
                    </p>
                    """, unsafe_allow_html=True)
                    # Accepting feedback from users
                    user_feedback = st.text_area("AI may be smart, but it's not perfect. Help us improve!")

                    if st.button("Submit Feedback"):
                        if user_feedback:
                            # You can save or send this feedback to a backend or a file
                            st.success("Thank you for your feedback!")
                        else:
                            st.error("Please enter your feedback before submitting.")
                    
                    # with st.expander('Suggestions'):
                    #     for i,j in data['labels'].items():
                    #         if j >= 0.75:
                    #             sugg = suggestions_dict['positive'][i]
                    #             st.write(f'{sugg}')
                    #         else:
                    #             sugg = suggestions_dict['negative'][i]
                    #             st.write(f'{sugg}')
            else:
                st.error('No input file found')
