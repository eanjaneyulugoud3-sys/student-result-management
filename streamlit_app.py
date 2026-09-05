import streamlit as st
import pandas as pd
import os
from PIL import Image

st.set_page_config(page_title="Student Result Management", layout="wide", page_icon="🎓")

# ==== BEST LOGO DIRECT ====
st.markdown("""
<style>
.logo-box {
    text-align:center; background: linear-gradient(135deg, #0f4c75, #1b262c);
    padding:15px; border-radius:20px; border:4px solid #f9c74f;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}
.logo-box h2 { color:#f9c74f; margin:0; font-size:22px; }
.logo-box h4 { color:white; margin:0; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div class='logo-box'>
        <div style='font-size:60px;'>🎓</div>
        <div style='font-size:40px;'>📊</div>
        <h2>STUDENT RESULT</h2>
        <h4>MANAGEMENT APP</h4>
        <p style='color:#f9c74f;'>🏆 Rank & Grade System</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("---")

# If you uploaded logo.png it will show here automatically
if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", use_container_width=True)
if os.path.exists("logo_final.png"):
    st.sidebar.image("logo_final.png", use_container_width=True)

st.title("🎓 Student Result Management")
st.caption("Photo + Subject Wise + Grade + Rank")

DATA_FILE = "students.csv"
if "df" not in st.session_state:
    if os.path.exists(DATA_FILE):
        st.session_state.df = pd.read_csv(DATA_FILE)
    else:
        st.session_state.df = pd.DataFrame(columns=["Roll No", "Name", "Class", "Telugu", "English", "Maths", "Science", "Social", "Total", "Percentage", "Grade", "Photo"])

def get_grade(per):
    if per >= 90: return "A+"
    elif per >= 75: return "A"
    elif per >= 60: return "B"
    elif per >= 50: return "C"
    elif per >= 35: return "D"
    else: return "FAIL"

df = st.session_state.df

with st.sidebar.form("form", clear_on_submit=True):
    st.subheader("➕ Add Student")
    roll = st.text_input("Roll No *")
    name = st.text_input("Name *")
    class_name = st.text_input("Class", value="10th")
    telugu = st.number_input("Telugu", 0, 100, 0)
    english = st.number_input("English", 0, 100, 0)
    maths = st.number_input("Maths", 0, 100, 0)
    science = st.number_input("Science", 0, 100, 0)
    social = st.number_input("Social", 0, 100, 0)
    photo_file = st.file_uploader("Photo", type=["jpg","jpeg","png"])
    btn = st.form_submit_button("💾 Save Result", use_container_width=True)
    if btn:
        if not roll or not name:
            st.error("Roll & Name kavali")
        else:
            total = telugu+english+maths+science+social
            per = total/5
            grade = get_grade(per)
            photo_path = ""
            if photo_file:
                os.makedirs("photos", exist_ok=True)
                photo_path = f"photos/{roll}.png"
                Image.open(photo_file).save(photo_path)
            new = {"Roll No":roll,"Name":name,"Class":class_name,"Telugu":telugu,"English":english,"Maths":maths,"Science":science,"Social":social,"Total":total,"Percentage":round(per,2),"Grade":grade,"Photo":photo_path}
            st.session_state.df = pd.concat([df, pd.DataFrame([new])], ignore_index=True)
            st.session_state.df.to_csv(DATA_FILE, index=False)
            st.success(f"Saved {grade}")
            st.rerun()

st.sidebar.download_button("⬇️ Download CSV", df.to_csv(index=False).encode(), "students.csv", "text/csv", use_container_width=True)

if not df.empty:
    df_sorted = df.sort_values(by="Total", ascending=False).reset_index(drop=True)
    df_sorted["Rank"] = df_sorted["Total"].rank(method="dense", ascending=False).astype(int)
    st.subheader(f"📋 Results ({len(df_sorted)})")
    for i,row in df_sorted.iterrows():
        c1,c2 = st.columns([1,4])
        with c1:
            if row["Photo"] and os.path.exists(str(row["Photo"])):
                st.image(str(row["Photo"]), width=150)
            st.metric("🏆 RANK", f"#{row['Rank']}")
        with c2:
            st.markdown(f"### {row['Name']} | {row['Roll No']} | {row['Class']} | {row['Percentage']}% | **Grade {row['Grade']}**")
            cols = st.columns(6)
            cols[0].metric("Tel", row["Telugu"])
            cols[1].metric("Eng", row["English"])
            cols[2].metric("Maths", row["Maths"])
            cols[3].metric("Sci", row["Science"])
            cols[4].metric("Soc", row["Social"])
            cols[5].metric("Total", f"{row['Total']}/500")
        st.divider()
else:
    st.info("Sidebar nunchi student add chey")
            
