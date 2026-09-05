import streamlit as st
import pandas as pd
import os, random, io, zipfile
from PIL import Image, ImageDraw, ImageFont

st.set_page_config(page_title="Malla Reddy - Anjaneyulu Permanent Admin", layout="wide", page_icon="🏛️")

# ========== ALL FIXED PERMANENT POINTS ==========
TEACHER_USER = "Anjaneyulu" # PERMANENT - CANNOT CHANGE
TEACHER_PASS = "anji123" # PERMANENT - CANNOT CHANGE
DATA_FILE = "students.csv" # STORE DATA FILE
LOGO_FILE = "college_logo.png"
PHOTO_DIR = "photos"
# ================================================

# Session States
if "college_name" not in st.session_state: st.session_state.college_name = "Malla Reddy Vishwavidyapeeth [Deemed to be University]"
if "college_logo" not in st.session_state: st.session_state.college_logo = ""
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "role" not in st.session_state: st.session_state.role = ""
if "logged_user" not in st.session_state: st.session_state.logged_user = ""
if "otp_sent" not in st.session_state: st.session_state.otp_sent = False
if "otp" not in st.session_state: st.session_state.otp = ""
if "temp_user" not in st.session_state: st.session_state.temp_user = ""
if "temp_role" not in st.session_state: st.session_state.temp_role = ""
if "zip_data" not in st.session_state: st.session_state.zip_data = None

# Load Data - STORE DATA
if "df" not in st.session_state:
    if os.path.exists(DATA_FILE):
        try: st.session_state.df = pd.read_csv(DATA_FILE)
        except: st.session_state.df = pd.DataFrame(columns=["Roll No","Name","Class","Telugu","English","Maths","Science","Social","Total","Percentage","Grade","Photo"])
    else:
        st.session_state.df = pd.DataFrame(columns=["Roll No","Name","Class","Telugu","English","Maths","Science","Social","Total","Percentage","Grade","Photo"])

df = st.session_state.df
if os.path.exists(LOGO_FILE): st.session_state.college_logo = LOGO_FILE

try:
    import qrcode
    QR_AVAILABLE = True
except: QR_AVAILABLE = False

def get_grade(p):
    if p>=90: return "A+ (Outstanding)"
    elif p>=75: return "A (Excellent)"
    elif p>=60: return "B (Good)"
    elif p>=50: return "C (Average)"
    elif p>=35: return "D (Pass)"
    else: return "FAIL"

def create_qr(data):
    if not QR_AVAILABLE: return None
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(data); qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white").resize((160,160))

def create_marksheet(row):
    img = Image.new('RGB', (900, 1300), 'white')
    draw = ImageDraw.Draw(img)
    try:
        f_big=ImageFont.truetype("arial.ttf",28)
        f_med=ImageFont.truetype("arial.ttf",20)
        f_small=ImageFont.truetype("arial.ttf",16)
        f_tiny=ImageFont.truetype("arial.ttf",12)
    except: f_big=f_med=f_small=f_tiny=ImageFont.load_default()

    draw.rectangle([0,0,900,150], fill='#8B0000')
    if st.session_state.college_logo and os.path.exists(st.session_state.college_logo):
        try:
            logo = Image.open(st.session_state.college_logo).resize((100,100))
            img.paste(logo,(20,20))
        except: pass
    draw.text((140,20), st.session_state.college_name[:45], fill='gold', font=f_big)
    draw.text((140,60), "Deemed to be University - Hyderabad", fill='white', font=f_small)
    draw.text((140,90), "STATEMENT OF MARKS - 2025 - QR VERIFIED", fill='white', font=f_med)

    y=170
    if row["Photo"] and os.path.exists(str(row["Photo"])):
        try:
            p = Image.open(str(row["Photo"])).resize((150,180))
            img.paste(p,(30,y))
            draw.rectangle([30,y,180,y+180], outline='#8B0000', width=3)
        except: pass

    qr_data = f"College:{st.session_state.college_name}\nRoll:{row['Roll No']}\nName:{row['Name']}\nClass:{row.get('Class','')}\nS1:{row['Telugu']} S2:{row['English']} S3:{row['Maths']} S4:{row['Science']} S5:{row['Social']}\nTotal:{row['Total']}/500 Per:{row['Percentage']}% Grade:{row['Grade']}\nRank:{row.get('Rank',1)}\nVerified by {TEACHER_USER} Permanent"
    qimg = create_qr(qr_data)
    if qimg:
        img.paste(qimg,(720,y))
        draw.text((710,y+165), "SCAN FULL DETAILS", fill='black', font=f_tiny)

    draw.text((210,y), f"Roll No: {row['Roll No']} | Rank: #{row.get('Rank',1)}", fill='black', font=f_med)
    draw.text((210,y+35), f"Name: {str(row['Name'])[:30]}", fill='black', font=f_med)
    draw.text((210,y+70), f"Class: {str(row.get('Class',''))}", fill='black', font=f_small)
    draw.text((210,y+100), f"Percentage: {row['Percentage']}% | Grade: {row['Grade']}", fill='#8B0000', font=f_med)

    ty=400
    draw.rectangle([20,ty,880,ty+45], fill='#8B0000')
    draw.text((30,ty+12), "SUBJECT NAME", fill='white', font=f_med)
    draw.text((380,ty+12), "MARKS", fill='white', font=f_med)
    draw.text((680,ty+12), "MAX 100", fill='white', font=f_med)

    subs=[("Subject 1",row['Telugu']),("Subject 2",row['English']),("Subject 3",row['Maths']),("Subject 4",row['Science']),("Subject 5",row['Social'])]
    for i,(s,m) in enumerate(subs):
        yy=ty+55+i*55
        draw.rectangle([20,yy,880,yy+50], fill="#fff9c4" if i%2==0 else "white", outline="black")
        draw.text((30,yy+15), s, fill='black', font=f_small)
        draw.text((400,yy+15), str(m), fill='black', font=f_med)

    total_y=ty+350
    draw.rectangle([20,total_y,880,total_y+100], fill='gold', outline='#8B0000', width=2)
    draw.text((30,total_y+15), f"TOTAL: {row['Total']}/500", fill='black', font=f_big)
    draw.text((30,total_y+60), f"PER: {row['Percentage']}% | GRADE: {row['Grade']}", fill='#8B0000', font=f_med)
    return img

# HEADER
st.markdown(f"<div style='background:linear-gradient(90deg,#8B0000,#FF4500);color:white;padding:25px;border-radius:15px;text-align:center;'><h1>🏛️ {st.session_state.college_name}</h1><p>TEACHER: Anjaneyulu / anji123 + OTP PERMANENT | STUDENT: RollNo / RollNo + OTP | UPDATE ONLY ONE PERSON | STORE DATA CSV | PHOTO+LOGO+QR+ZIP</p></div>", unsafe_allow_html=True)

# SIDEBAR - LOGIN + ENTER + LOGO + STORE
with st.sidebar:
    st.markdown(f"<div style='background:#e8f5e9;padding:12px;border-radius:10px;border:2px solid green;'><b>🔒 PERMANENT LOGIN - NO CHANGE</b><br>👨‍🏫 Teacher: <b>{TEACHER_USER}/{TEACHER_PASS}+OTP</b><br>👨‍🎓 Student: <b>RollNo/RollNo+OTP</b> Ex:101/101+OTP<br>Store: {DATA_FILE} + {PHOTO_DIR}/</div>", unsafe_allow_html=True)

    if not st.session_state.logged_in:
        st.header("🔐 Login Panel")
        login_type = st.radio("Select Role:", ["👨‍🏫 Teacher", "👨‍🎓 Student"])
        if not st.session_state.otp_sent:
            if "Teacher" in login_type:
                st.subheader("Teacher Login Permanent")
                u = st.text_input("Username", placeholder="Anjaneyulu")
                p = st.text_input("Password", type="password", placeholder="anji123")
                if st.button("Get OTP - Teacher", use_container_width=True, type="primary"):
                    if u==TEACHER_USER and p==TEACHER_PASS:
                        st.session_state.otp=str(random.randint(100000,999999)); st.session_state.otp_sent=True; st.session_state.temp_user=TEACHER_USER; st.session_state.temp_role="teacher"; st.rerun()
                    else: st.error(f"Only {TEACHER_USER}/{TEACHER_PASS} PERMANENT")
            else:
                st.subheader("Student Login - RollNo/RollNo")
                u = st.text_input("Roll No Username", placeholder="101")
                p = st.text_input("Password Same Roll No", placeholder="101")
                if st.button("Get OTP - Student", use_container_width=True, type="primary"):
                    if u!=p: st.error("Username & Password SAME Roll No! Ex:101/101")
                    elif df.empty or u not in df["Roll No"].astype(str).values: st.error(f"Roll {u} not found! Ask Teacher")
                    else: st.session_state.otp=str(random.randint(100000,999999)); st.session_state.otp_sent=True; st.session_state.temp_user=u; st.session_state.temp_role="student"; st.rerun()
        else:
            st.success(f"OTP for {st.session_state.temp_user}")
            st.markdown(f"<div style='background:yellow;padding:20px;text-align:center;border:4px solid red;border-radius:15px;'><h1 style='color:red;letter-spacing:8px;'>{st.session_state.otp}</h1><small>YELLOW BOX OTP</small></div>", unsafe_allow_html=True)
            ot = st.text_input("Enter OTP")
            if st.button("✅ Verify Login", use_container_width=True, type="primary"):
                if ot==st.session_state.otp:
                    st.session_state.logged_in=True; st.session_state.logged_user=st.session_state.temp_user; st.session_state.role=st.session_state.temp_role; st.session_state.otp_sent=False; st.rerun()
                else: st.error("Wrong OTP")
            if st.button("⬅️ Back"): st.session_state.otp_sent=False; st.rerun()
    else:
        st.success(f"✅ Logged: {st.session_state.logged_user} ({st.session_state.role})")
        if st.button("🚪 Logout", use_container_width=True): st.session_state.logged_in=False; st.session_state.role=""; st.rerun()

    if st.session_state.logged_in and st.session_state.role=="teacher":
        st.divider()
        st.subheader("🏛️ College Logo Upload")
        logo_up = st.file_uploader("Upload Logo PNG/JPG", type=["png","jpg","jpeg"])
        if logo_up: Image.open(logo_up).save(LOGO_FILE); st.session_state.college_logo=LOGO_FILE; st.success("Logo Saved - Marksheet lo vastundi"); st.image(logo_up,width=80)

        st.divider()
        st.subheader("➕ ENTER New Student - Store Data")
        with st.form("enter_form", clear_on_submit=True):
            r = st.text_input("Roll No * Ex:101")
            n = st.text_input("Name * Ex:Ramesh")
            cl = st.text_input("Class", value="B TECH 2nd Year")
            s1=st.number_input("Subject 1",0,100,0); s2=st.number_input("Subject 2",0,100,0); s3=st.number_input("Subject 3",0,100,0); s4=st.number_input("Subject 4",0,100,0); s5=st.number_input("Subject 5",0,100,0)
            ph = st.file_uploader("Student Photo", type=["jpg","png","jpeg"])
            if st.form_submit_button("💾 SAVE & STORE", use_container_width=True, type="primary"):
                if not r or not n: st.error("Roll No & Name compulsory")
                elif not df.empty and r in df["Roll No"].astype(str).values: st.error(f"{r} exists! Use UPDATE")
                else:
                    os.makedirs(PHOTO_DIR, exist_ok=True)
                    pp=""
                    if ph: pp=f"{PHOTO_DIR}/{r}.png"; Image.open(ph).save(pp)
                    tot=s1+s2+s3+s4+s5; per=tot/5
                    new={"Roll No":r,"Name":n,"Class":cl,"Telugu":s1,"English":s2,"Maths":s3,"Science":s4,"Social":s5,"Total":tot,"Percentage":round(per,2),"Grade":get_grade(per),"Photo":pp}
                    st.session_state.df=pd.concat([df,pd.DataFrame([new])], ignore_index=True)
                    st.session_state.df.to_csv(DATA_FILE,index=False)
                    st.success(f"Stored {r}-{n} {tot}/500 | Student Login {r}/{r}+OTP"); st.balloons(); st.rerun()

        st.divider()
        st.subheader("💾 Store Data Backup")
        if not df.empty:
            st.download_button("⬇️ Download CSV Backup (All Data)", df.to_csv(index=False).encode('utf-8'), "students_backup.csv", "text/csv", use_container_width=True)
            st.write(f"Total Stored: {len(df)} students in {DATA_FILE}")

# MAIN
if st.session_state.logged_in:
    df_sorted = df.sort_values(by="Total", ascending=False).reset_index(drop=True) if not df.empty else df
    if not df_sorted.empty: df_sorted["Rank"] = df_sorted["Total"].rank(method="dense", ascending=False).astype(int)

    if st.session_state.role=="teacher":
        if not df_sorted.empty:
            st.subheader("🏆 Top 3 Toppers")
            top3=df_sorted.head(3)
            cols=st.columns(3)
            medals=["🥇 GOLD 1st","🥈 SILVER 2nd","🥉 BRONZE 3rd"]
            colors=["#FFD700","#C0C0C0","#CD7F32"]
            for idx,(i,row) in enumerate(top3.iterrows()):
                with cols[idx]:
                    st.markdown(f"<div style='background:{colors[idx]};padding:15px;border-radius:12px;text-align:center;border:3px solid #8B0000;'><b>{medals[idx]}<br>{row['Name']}({row['Roll No']})<br>{row['Total']}/500 {row['Percentage']}%</b></div>", unsafe_allow_html=True)
                    if row["Photo"] and os.path.exists(str(row["Photo"])): st.image(str(row["Photo"]), use_container_width=True)

        if not df_sorted.empty:
            st.divider()
            c1,c2=st.columns([3,1])
            with c1: st.subheader("📦 Download All Marksheets ZIP (Photo+Logo+QR)")
            with c2:
                if st.button("Create ZIP", use_container_width=True, type="primary"):
                    zbuf=io.BytesIO()
                    with zipfile.ZipFile(zbuf,'w') as z:
                        for _,row in df_sorted.iterrows():
                            mimg=create_marksheet(row)
                            b=io.BytesIO(); mimg.save(b,format="PNG")
                            z.writestr(f"{row['Roll No']}_{row['Name']}.png", b.getvalue())
                    st.session_state.zip_data=zbuf.getvalue()
            if st.session_state.zip_data:
                st.download_button("⬇️ Download ZIP All", st.session_state.zip_data, "All_Marksheets.zip", "application/zip", use_container_width=True, type="primary")

        st.divider()
        search = st.text_input("🔍 Search - Type Roll No to Update Only ONE Person", placeholder="101 or Ramesh")
        fdf=df_sorted
        if search and not df_sorted.empty: fdf=df_sorted[df_sorted["Roll No"].astype(str).str.contains(search,case=False) | df_sorted["Name"].str.contains(search,case=False)]

        st.subheader(f"📋 Students {len(fdf)} - UPDATE ONLY ONE PERSON + DELETE + STORE")
        for i,row in fdf.iterrows():
            with st.container(border=True):
                st.markdown(f"### {row['Name']} ({row['Roll No']}) Rank #{row.get('Rank',1)} {row['Total']}/500 {row['Percentage']}% {row['Grade']} | Login:{row['Roll No']}/{row['Roll No']}+OTP")
                c1,c2,c3,c4=st.columns([1,2.5,1,1])
                with c1:
                    if row["Photo"] and os.path.exists(str(row["Photo"])): st.image(str(row["Photo"]), width=140)
                with c2:
                    st.write(f"Class:{row.get('Class','')} S1:{row['Telugu']} S2:{row['English']} S3:{row['Maths']} S4:{row['Science']} S5:{row['Social']}")
                    with st.expander(f"✏️ UPDATE ONLY THIS ONE - {row['Roll No']}"):
                        st.warning(f"Changing ONLY {row['Roll No']} - Others NOT change - Store Data auto")
                        with st.form(f"up_{i}"):
                            un=st.text_input("Name",value=row['Name'],key=f"un_{i}"); uc=st.text_input("Class",value=row.get('Class',''),key=f"uc_{i}")
                            us1=st.number_input("S1",0,100,int(row['Telugu']),key=f"us1_{i}"); us2=st.number_input("S2",0,100,int(row['English']),key=f"us2_{i}"); us3=st.number_input("S3",0,100,int(row['Maths']),key=f"us3_{i}"); us4=st.number_input("S4",0,100,int(row['Science']),key=f"us4_{i}"); us5=st.number_input("S5",0,100,int(row['Social']),key=f"us5_{i}")
                            uph=st.file_uploader("New Photo",type=["jpg","png","jpeg"],key=f"uph_{i}")
                            if st.form_submit_button(f"UPDATE ONLY {row['Roll No']}",use_container_width=True,type="primary"):
                                tot=us1+us2+us3+us4+us5; per=tot/5; pp=row["Photo"]
                                if uph: os.makedirs(PHOTO_DIR,exist_ok=True); pp=f"{PHOTO_DIR}/{row['Roll No']}.png"; Image.open(uph).save(pp)
                                idx=st.session_state.df[st.session_state.df["Roll No"].astype(str)==str(row["Roll No"])].index[0]
                                st.session_state.df.loc[idx,["Name","Class","Telugu","English","Maths","Science","Social","Total","Percentage","Grade","Photo"]]=[un,uc,us1,us2,us3,us4,us5,tot,round(per,2),get_grade(per),pp]
                                st.session_state.df.to_csv(DATA_FILE,index=False)
                                st.success(f"Updated ONLY {row['Roll No']} & Stored"); st.rerun()
                with c3:
                    q=create_qr(f"Roll:{row['Roll No']} Name:{row['Name']} Total:{row['Total']}/500 {row['Percentage']}% Rank:{row.get('Rank',1)} Verified:{TEACHER_USER}");
                    if q: b=io.BytesIO(); q.save(b,format="PNG"); st.image(b.getvalue(),width=140,caption="QR Full")
                with c4:
                    mimg=create_marksheet(row); b=io.BytesIO(); mimg.save(b,format="PNG")
                    st.download_button("📸 Download\nPhoto+Logo+QR",b.getvalue(),f"{row['Roll No']}_{row['Name']}.png","image/png",key=f"dl_{i}",use_container_width=True)
                    if st.button(f"🗑️ Delete {row['Roll No']}",key=f"del_{i}",use_container_width=True):
                        st.session_state.df=df[df["Roll No"].astype(str)!=str(row["Roll No"])]; st.session_state.df.to_csv(DATA_FILE,index=False); st.rerun()
    else:
        my_data = df_sorted[df_sorted["Roll No"].astype(str)==str(st.session_state.logged_user)] if not df_sorted.empty else pd.DataFrame()
        if not my_data.empty:
            row=my_data.iloc[0]
            st.success(f"Welcome {row['Name']} Login:{row['Roll No']}/{row['Roll No']}+OTP - Only YOUR Data")
            st.markdown(f"## {row['Name']} ({row['Roll No']}) Rank #{row.get('Rank',1)} {row['Total']}/500 {row['Percentage']}%")
            c1,c2=st.columns([1,2])
            with c1:
                if row["Photo"] and os.path.exists(str(row["Photo"])): st.image(str(row["Photo"]),width=250)
            with c2:
                mimg=create_marksheet(row); b=io.BytesIO(); mimg.save(b,format="PNG")
                st.image(b.getvalue(),use_container_width=True)
                st.download_button("📸 Download My Marksheet Photo+Logo+QR",b.getvalue(),f"{row['Roll No']}_Marksheet.png","image/png",use_container_width=True,type="primary")
else:
    st.info("👈 Login from Sidebar - All Points Working")
    st.code(f"TEACHER PERMANENT: {TEACHER_USER}/{TEACHER_PASS}+OTP\nSTUDENT: RollNo/RollNo+OTP Ex:101/101+OTP\nSTORE: {DATA_FILE} + {PHOTO_DIR}/\nFEATURES: Enter, Update ONE Person, Delete, Photo, Logo, QR, ZIP, Rank, Gold/Silver/Bronze, Download")
