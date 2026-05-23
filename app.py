import streamlit as st
from groq import Groq
from PIL import Image
import base64
import io

# 1. ඇප් එකේ මුහුණත සහ මාතෘකා සැකසීම
st.set_page_config(page_title="AI Paddy Surveyor", page_icon="🌾")
st.title("🌾 AI වී අස්වනු සමීක්ෂණ පද්ධතිය (Groq Speed)")
st.write("කුඹුරේ වී කරල් සහිත ඡායාරූපයක් ඇතුළත් කර ක්ෂණික AI තාක්ෂණික වාර්තාව ලබා ගන්න.")

# 2. පරිශීලකයාගෙන් API Key එක ලබා ගන්නා කොටස
api_key = st.text_input("ඔයාගේ Groq API Key එක මෙතැනට ඇතුළත් කරන්න (gsk_...):", type="password")

# 3. ඡායාරූපයක් ඇතුළත් කිරීමට බොත්තමක් සෑදීම
uploaded_file = st.file_uploader("කුඹුරේ ඡායාරූපයක් තෝරන්න (Upload Image)...", type=["jpg", "jpeg", "png"])

# පින්තූරය Groq එකට කියවිය හැකි පරිදි සකසන ශ්‍රිතය (Helper function)
def encode_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='ඇතුළත් කළ ඡායාරූපය', use_container_width=True)
    
    # 4. AI විශ්ලේෂණ බොත්තම ක්‍රියාත්මක වීම
    if st.button("AI හරහා පරීක්ෂා කරන්න ➔"):
        if not api_key:
            st.error("කරුණාකර ඉදිරියට යාමට ඔයාගේ Groq API Key එක ඇතුළත් කරන්න!")
        else:
            with st.spinner('Groq AI පද්ධතිය ඡායාරූපය විශ්ලේෂණය කරමින් පවතී. කරුණාකර රැඳී සිටින්න...'):
                try:
                    # පින්තූරය සකස් කිරීම
                    base64_image = encode_image(image)
                    
                    # Groq ක්ලයන්ට් එක සක්‍රීය කිරීම
                    client = Groq(api_key=api_key)
                    
                    # ලොව වේගවත්ම Vision මාදිලිය භාවිතා කිරීම
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": """
                                        Analyze this image of a paddy field or rice panicle for an agricultural survey.
                                        Provide the response in clear bullet points in Sinhala language. Include:
                                        1. Estimated Panicle Count (වී කරල් ගණන පිළිබඳ දළ තක්සේරුව)
                                        2. Grain Density (වී ඇටවල පිරිමාව - High/Medium/Low)
                                        3. Crop Maturity (පරිණතභාවය සහ අස්වනු නෙලීමට ඇති සූදානම)
                                        4. Brief technical recommendation for extension officers.
                                        """
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/jpeg;base64,{base64_image}",
                                        },
                                    },
                                ],
                            }
                        ],
                        model="llama-3.2-11b-vision-preview",
                    )
                    
                    st.success("විශ්ලේෂණය සාර්ථකයි!")
                    st.subheader("📊 AI ක්ෂේත්‍ර වාර්තාව:")
                    st.write(chat_completion.choices[0].message.content)
                    
                except Exception as e:
                    st.error(f"සම්බන්ධතාවයේ දෝෂයක් පවතී: {e}")
