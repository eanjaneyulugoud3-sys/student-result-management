
  import streamlit as st
import pandas as pd
import os, random, io
from PIL import Image, ImageDraw, ImageFont

st.set_page_config(page_title="MRV University", layout="wide", page_icon="🏛️")

TEACHER_USER = "Anjaneyulu"
TEACHER_PASS = "anji123"
DATA_FILE = "students.csv"
LOGO_FILE = "college_logo.png"
PHOTO_DIR = "photos"
SUBJECTS = ["Telugu", "English", "Maths", "Science", "Social"]

if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "role" not in st.session_state: st.session_state.role = ""
if "logged_user" not in st.session_state: st.session_state.logged_user = ""
if "otp_sent" not in st.session_state: st.session_state.otp_sent = False
if "otp" not in st.session_state: st.session_state.otp = ""
if "temp_user" not in st.session_state: st.session_state.temp_user = ""
if "temp_role" not in st.session_state: st.session_state.temp_role = ""
if "df" not in st.session_state:
    if os.path.exists(DATA_FILE):
        try: st.session_state.df = pd.read_csv(DATA_FILE)
        except: st.session_state.df = pd.DataFrame(columns=["Roll No","Name","Class","Telugu","English","Maths","Science","Social","Total","Percentage","Grade","Photo"])
    else:
        st.session_state.df = pd.DataFrame(columns=["Roll No","Name","Class","Telugu","English","Maths","Science","Social","Total","Percentage","Grade","Photo"])
df = st.session_state.df

try:
    import qrcode
    QR_AVAILABLE = True
except: QR_AVAILABLE = False

def get_grade(p):
    if p>=90: return "A+"
    elif p>=75: return "A"
    elif p>=60: return "B"
    elif p>=50: return "C"
    elif p>=35: return "D"
    else: return "FAIL"

def create_qr_with_details(row):
    if not QR_AVAILABLE: return None
    qr_data = f"MRV UNIVERSITY\nRoll:{row['Roll No']} Name:{row['Name']}\nTelugu:{row['Telugu']} English:{row['English']} Maths:{row['Maths']} Science:{row['Science']} Social:{row['Social']}\nTotal:{row['Total']}/500 Per:{row['Percentage']}% Grade:{row['Grade']} Rank:{row.get('Rank',1)}"
    qr = qrcode.QRCode(version=2, box_size=10, border=2)
    qr.add_data(qr_data); qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white").resize((160,160))

def create_marksheet(row):
    img = Image.new('RGB', (900, 1350), 'white')
    draw = ImageDraw.Draw(img)
    try:
        f_big=ImageFont.truetype("arial.ttf",26); f_med=ImageFont.truetype("arial.ttf",18); f_small=ImageFont.truetype("arial.ttf",15)
    except: f_big=f_med=f_small=ImageFont.load_default()
    draw.rectangle([0,0,900,130], fill='#8B0000')
    if os.path.exists(LOGO_FILE):
        try: logo = Image.open(LOGO_FILE).resize((100,100)); img.paste(logo, (15,15))
        except: draw.ellipse([20,20,120,120], fill='gold')
    else: draw.ellipse([20,20,120,120], fill='gold')
    draw.text((140,35), "MALLA REDDY VISHWAVIDYAPEETH UNIVERSITY", fill='gold', font=f_big)
    y=160
    if row["Photo"] and os.path.exists(str(row["Photo"])):
        try: p = Image.open(str(row["Photo"])).resize((140,170)); img.paste(p,(30,y)); draw.rectangle([30,y,170,y+170], outline='#8B0000', width=3)
        except: pass
    qimg = create_qr_with_details(row)
    if qimg: img.paste(qimg,(720,y))
    draw.text((190,y), f"Roll: {row['Roll No']} Rank #{row.get('Rank',1)}", fill='black', font=f_med)
    draw.text((190,y+35), f"Name: {str(row['Name'])[:32]}", fill='black', font=f_med)
    draw.text((190,y+70), f"Class: {str(row.get('Class',''))} | {row['Percentage']}% | {row['Grade']}", fill='black', font=f_small)
    ty=360
    draw.rectangle([20,ty,880,ty+40], fill='#8B0000')
    draw.text((30,ty+10), "SUBJECT (0-100)", fill='white', font=f_med); draw.text((400,ty+10), "MARKS", fill='white', font=f_med)
    subs=[(SUBJECTS[0],row['Telugu']),(SUBJECTS[1],row['English']),(SUBJECTS[2],row['Maths']),(SUBJECTS[3],row['Science']),(SUBJECTS[4],row['Social'])]
    for i,(s,m) in enumerate(subs):
        yy=ty+50+i*50; draw.rectangle([20,yy,880,yy+45], fill="#fff9c4" if i%2==0 else "white", outline="black")
        draw.text((30,yy+12), f"{s} (0-100)", fill='black', font=f_small); draw.text((410,yy+12), f"{m}/100", fill='black', font=f_med)
    draw.rectangle([20,ty+330,880,ty+420], fill='gold', outline='#8B0000', width=2)
    draw.text((30,ty+340), f"TOTAL: {row['Total']}/500", fill='black', font=f_big)
    draw.text((30,ty+375), f"{row['Percentage']}% - {row['Grade']}", fill='#8B0000', font=f_med)
    return img

# HEADER - LOGO LEFT + NO LINE BELOW - YOUR ASK
col_logo, col_title = st.columns([1, 8])
with col_logo:
    if os.path.exists(LOGO_FILE): st.image(LOGO_FILE, width=90)
with col_title:
    st.markdown('<h1 style="color:#8B0000;margin:0;padding-top:15px;">🏛️ MALLA REDDY VISHWAVIDYAPEETH UNIVERSITY</h1>', unsafe_allow_html=True)
st.divider()

with st.sidebar:
    if os.path.exists(LOGO_FILE): st.image(LOGO_FILE, width=180)
    st.markdown(f"<div style='background:#e3f2fd;padding:8px;border-radius:8px;border:2px solid #1976d2;font-size:12px;'><b>Subjects 0-100</b><br>{'<br>'.join(SUBJECTS)}</div>", unsafe_allow_html=True)
    if not st.session_state.logged_in:
        st.header("🔐 Login")
        login_type = st.radio("Role:", ["👨‍🏫 Teacher", "👨‍🎓 Student"])
        if not st.session_state.otp_sent:
            if "Teacher" in login_type:
                u = st.text_input("Username"); p = st.text_input("Password", type="password")
                if st.button("Get OTP Teacher", use_container_width=True, type="primary"):
                    if u==TEACHER_USER and p==TEACHER_PASS:
                        st.session_state.otp=str(random.randint(100000,999999)); st.session_state.otp_sent=True; st.session_state.temp_user=TEACHER_USER; st.session_state.temp_role="teacher"; st.rerun()
                    else: st.error("Invalid")
            else:
                u = st.text_input("Roll No"); p = st.text_input("Password Same", type="password")
                if st.button("Get OTP Student", use_container_width=True, type="primary"):
                    if u!=p: st.error("Same Roll required")
                    elif df.empty or u not in df["Roll No"].astype(str).values: st.error(f"{u} not found")
                    else: st.session_state.otp=str(random.randint(100000,999999)); st.session_state.otp_sent=True; st.session_state.temp_user=u; st.session_state.temp_role="student"; st.rerun()
        else:
            st.markdown(f"<div style='background:yellow;padding:15px;text-align:center;border:3px solid red;'><h1 style='color:red;'>{st.session_state.otp}</h1></div>", unsafe_allow_html=True)
            ot = st.text_input("OTP", type="password")
            if st.button("Verify", use_container_width=True, type="primary"):
                if ot==st.session_state.otp:
                    st.session_state.logged_in=True; st.session_state.logged_user=st.session_state.temp_user; st.session_state.role=st.session_state.temp_role; st.session_state.otp_sent=False; st.rerun()
                else: st.error("Wrong")
            if st.button("Back"): st.session_state.otp_sent=False; st.rerun()
    else:
        st.success(f"Logged: {st.session_state.logged_user} ({st.session_state.role})")
        if st.button("Logout", use_container_width=True): st.session_state.logged_in=False; st.rerun()

    if st.session_state.logged_in and st.session_state.role=="teacher":
        st.divider()
        st.subheader("ENTER - 0-100 Only")
        with st.form("enter", clear_on_submit=True):
            r=st.text_input("Roll *"); n=st.text_input("Name *"); cl=st.text_input("Class", value="10th")
            s1=st.number_input(f"{SUBJECTS[0]} (0-100)", min_value=0, max_value=100, value=0)
            s2=st.number_input(f"{SUBJECTS[1]} (0-100)", min_value=0, max_value=100, value=0)
            s3=st.number_input(f"{SUBJECTS[2]} (0-100)", min_value=0, max_value=100, value=0)
            s4=st.number_input(f"{SUBJECTS[3]} (0-100)", min_value=0, max_value=100, value=0)
            s5=st.number_input(f"{SUBJECTS[4]} (0-100)", min_value=0, max_value=100, value=0)
            ph=st.file_uploader("Photo", type=["jpg","png","jpeg"])
            if st.form_submit_button("SAVE", use_container_width=True, type="primary"):
                if r and n:
                    if any(m<0 or m>100 for m in [s1,s2,s3,s4,s5]): st.error("0-100 only!")
                    else:
                        os.makedirs(PHOTO_DIR,exist_ok=True); pp=""
                        if ph: pp=f"{PHOTO_DIR}/{r}.png"; Image.open(ph).save(pp)
                        tot=s1+s2+s3+s4+s5; per=tot/5
                        new={"Roll No":r,"Name":n,"Class":cl,"Telugu":s1,"English":s2,"Maths":s3,"Science":s4,"Social":s5,"Total":tot,"Percentage":round(per,2),"Grade":get_grade(per),"Photo":pp}
                        st.session_state.df=pd.concat([df,pd.DataFrame([new])], ignore_index=True); st.session_state.df.to_csv(DATA_FILE,index=False); st.rerun()

if st.session_state.logged_in:
    df_sorted = df.sort_values(by="Total", ascending=False).reset_index(drop=True) if not df.empty else df
    if not df_sorted.empty: df_sorted["Rank"] = df_sorted["Total"].rank(method="dense", ascending=False).astype(int)
    if st.session_state.role=="teacher":
        st.subheader(f"Teacher - {len(df_sorted)} Students - Storage Data")
        search = st.text_input("Search", placeholder="101")
        fdf=df_sorted
        if search: fdf=df_sorted[df_sorted["Roll No"].astype(str).str.contains(search,case=False) | df_sorted["Name"].str.contains(search,case=False)]
        for i,row in fdf.iterrows():
            with st.container(border=True):
                st.write(f"{row['Name']} ({row['Roll No']}) - {row['Total']}/500 {row['Percentage']}% Rank {row.get('Rank',1)}")
                with st.expander(f"UPDATE {row['Roll No']}"):
                    with st.form(f"up_{i}"):
                        un=st.text_input("Name",value=row['Name'],key=f"un{i}")
                        us1=st.number_input(f"{SUBJECTS[0]}", min_value=0, max_value=100, value=int(row['Telugu']),key=f"s1{i}")
                        us2=st.number_input(f"{SUBJECTS[1]}", min_value=0, max_value=100, value=int(row['English']),key=f"s2{i}")
                        us3=st.number_input(f"{SUBJECTS[2]}", min_value=0, max_value=100, value=int(row['Maths']),key=f"s3{i}")
                        us4=st.number_input(f"{SUBJECTS[3]}", min_value=0, max_value=100, value=int(row['Science']),key=f"s4{i}")
                        us5=st.number_input(f"{SUBJECTS[4]}", min_value=0, max_value=100, value=int(row['Social']),key=f"s5{i}")
                        if st.form_submit_button(f"UPDATE {row['Roll No']}",use_container_width=True,type="primary"):
                            tot=us1+us2+us3+us4+us5; per=tot/5
                            idx=st.session_state.df[st.session_state.df["Roll No"].astype(str)==str(row["Roll No"])].index[0]
                            st.session_state.df.loc[idx,["Name","Telugu","English","Maths","Science","Social","Total","Percentage","Grade"]]=[un,us1,us2,us3,us4,us5,tot,round(per,2),get_grade(per)]
                            st.session_state.df.to_csv(DATA_FILE,index=False); st.rerun()
                if st.button(f"Delete {row['Roll No']}",key=f"del{i}"):
                    st.session_state.df=df[df["Roll No"].astype(str)!=str(row["Roll No"])]; st.session_state.df.to_csv(DATA_FILE,index=False); st.rerun()
        # STORAGE DATA - BACKUP SECTION - NEW
        if not df_sorted.empty:
            st.divider()
            st.subheader("💾 STORAGE DATA - Backup & List")
            c1,c2 = st.columns(2)
            with c1:
                st.download_button("📥 DOWNLOAD BACKUP CSV - All Students Data", df_sorted.to_csv(index=False).encode('utf-8'), f"MRV_backup_{pd.Timestamp.now().strftime('%Y%m%d')}.csv", "text/csv", use_container_width=True, type="primary")
                st.metric("Total Records", len(df_sorted))
                st.metric("Storage File", "students.csv")
            with c2:
                uploaded = st.file_uploader("📤 RESTORE Backup CSV", type=["csv"])
                if uploaded is not None:
                    if st.button("Restore Now", use_container_width=True):
                        st.session_state.df = pd.read_csv(uploaded)
                        st.session_state.df.to_csv(DATA_FILE,index=False)
                        st.success(f"Restored {len(st.session_state.df)} students!")
                        st.rerun()
            st.dataframe(df_sorted[["Roll No","Name","Class","Telugu","English","Maths","Science","Social","Total","Percentage","Grade","Rank"]], use_container_width=True)
    else:
        my_data = df_sorted[df_sorted["Roll No"].astype(str)==str(st.session_state.logged_user)] if not df_sorted.empty else pd.DataFrame()
        if not my_data.empty:
            row=my_data.iloc[0]
            mimg=create_marksheet(row); b=io.BytesIO(); mimg.save(b,format="PNG")
            st.image(b.getvalue(), use_container_width=True)
            st.download_button("📸 DOWNLOAD MY RESULT", b.getvalue(), f"{row['Roll No']}_Result.png", "image/png", use_container_width=True, type="primary")
else:
    st.info("👈 Login - Teacher: Anjaneyulu / anji123 - Student: Roll=Password") 
