import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. ඇප් එකේ මුහුණත සහ මාතෘකා සැකසීම
st.set_page_config(page_title="AI Paddy Surveyor", page_icon="🌾")
st.title("🌾 AI වී අස්වනු සමීක්ෂණ පද්ධතිය")
st.write("කුඹුරේ වී කරල් සහිත ඡායාරූපයක් ඇතුළත් කර AI තාක්ෂණික වාර්තාව ක්ෂණිකව ලබා ගන්න.")

# 2. පරිශීලකයාගෙන් API Key එක ලබා ගන්නා කොටස (ආරක්ෂාව සඳහා)
api_key = st.text_input("ඔයාගේ Gemini API Key එක මෙතැනට ඇතුළත් කරන්න:", type="password")

# 3. ඡායාරූපයක් ඇතුළත් කිරීමට (Upload) බොත්තමක් සෑදීම
uploaded_file = st.file_uploader("කුඹුරේ ඡායාරූපයක් තෝරන්න (Upload Image)...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # පින්තූරය තිරය මත පෙන්වීම
    image = Image.open(uploaded_file)
    st.image(image, caption='ඇතුළත් කළ ඡායාරූපය', use_container_width=True)
    
    # 4. AI විශ්ලේෂණ බොත්තම ක්‍රියාත්මක වීම
    if st.button("AI හරහා පරීක්ෂා කරන්න ➔"):
        if not api_key:
            st.error("කරුණාකර ඉදිරියට යාමට ඔයාගේ Gemini API Key එක ඇතුළත් කරන්න!")
        else:
            # Gemini පද්ධතිය ක්‍රියාත්මක කිරීම
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            # AI එකට දෙන සිංහල/ඉංග්‍රීසි මිශ්‍ර විධානය
            prompt = """
            Analyze this image of a paddy field or rice panicle for an agricultural survey.
            Provide the response in clear bullet points in Sinhala language. Include:
            1. Estimated Panicle Count (වී කරල් ගණන පිළිබඳ දළ තක්සේරුව)
            2. Grain Density (වී ඇටවල පිරිමාව - High/Medium/Low)
            3. Crop Maturity (පරිණතභාවය සහ අස්වනු නෙලීමට ඇති සූදානම)
            4. Brief technical recommendation for extension officers.
            """
            
            with st.spinner('Gemini AI පද්ධතිය ඡායාරූපය විශ්ලේෂණය කරමින් පවතී. කරුණාකර රැඳී සිටින්න...'):
                try:
                    response = model.generate_content([prompt, image])
                    st.success("විශ්ලේෂණය සාර්ථකයි!")
                    st.subheader("📊 AI ක්ෂේත්‍ර වාර්තාව:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"සම්බන්ධතාවයේ දෝෂයක් පවතී: {e}")