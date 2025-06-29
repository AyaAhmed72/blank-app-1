import streamlit as st
import qrcode
from io import BytesIO
from datetime import date
import urllib.parse

st.title("Home Visit QR Generator")

# Ask user to input the Display App URL
DISPLAY_APP_URL = st.text_input("Enter Display App URL (e.g. https://your-display-app.loca.lt):")

# Visit Info
name = st.text_input("Homeowner Name")
visit_date = st.date_input("Visit Date")
visit_time = st.time_input("Visit Time")
notes = st.text_area("Additional Notes")

if st.button("Generate QR Code"):
    if visit_date < date.today():
        st.error("⚠️ This QR code has expired. Please select today or a future date.")
    else:
        params = {
            'name': name,
            'date': str(visit_date),
            'time': str(visit_time),
            'notes': notes
        }
        encoded_params = urllib.parse.urlencode(params)
        qr_url = f"{DISPLAY_APP_URL.rstrip('/')}?{encoded_params}"
        
        qr = qrcode.make(qr_url)
        buf = BytesIO()
        qr.save(buf)
        buf.seek(0)

        st.image(buf.getvalue(), caption="Scan with Mobile Camera")
        st.markdown(f"**Encoded URL:** `{qr_url}`")
        st.markdown(f"[🔗 Open Display Page]({qr_url})", unsafe_allow_html=True)

        st.download_button(
            label="📥 Download QR Code",
            data=buf,
            file_name=f"qr_{name}.png",
            mime="image/png"
        )
