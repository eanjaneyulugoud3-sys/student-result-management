import streamlit as st
import pandas as pd
import os
import random
import io
import zipfile
from PIL import Image, ImageDraw, ImageFont

st.set_page_config(page_title="Malla Reddy ULTRA PRO FIXED", layout="wide", page_icon="🏆")

if "college_name" not in st.session_state:
    st.session_state.college_name = "Malla Reddy Vishwavidyapeeth [Deemed to be University]"
if "college_logo" not in st.session_state:
    st.session_state.college_logo = ""

PASSWORD = "python"
ADMIN = "admin"

if "logged_in" not in st.session_state: st.session_state.logged_in=False
if "logged_user" not in st.session_state: st.session_state.logged_user=""
if "is_admin" not in st.session_state: st.session_state.is_admin=False
if "otp_sent" not in st.session_state: st.session_state.otp_sent=False
if "otp" not in st.session_state: st.session_state.otp=""
if "editing_roll" not in st.session_state: st.session_state.editing_roll=None

try:
    import qrcode
    QR_AVAILABLE=True
except:
    QR_AVAILABLE=False

DATA_FILE="students.csv"
LOGO_FILE="college_logo.png"

if "df" not in st.session_state:
    if os.path.exists(DATA_FILE):
        try: st.session_state.df=pd.read_csv(DATA_FILE)
        except: st.session_state.df=pd.DataFrame(columns=["Roll No","Name","Class","Email","Telugu","English","Maths","Science","Social","Total","Percentage","Grade","Photo"])
    else:
        st.session_state.df=pd.DataFrame(columns=["Roll No","Name","Class","Email","Telugu","English","Maths","Science","Social","Total","Percentage","Grade","Photo"])

df=st.session_state.df

if os.path.exists(LOGO_FILE):
    st.session_state.college_logo=LOGO_FILE

def get_grade(p):
    if p>=90: return "A+ (Outstanding)"
    elif p>=75: return "A (Excellent)"
    elif p>=60: return "B (Good)"
    elif p>=50: return "C (Average)"
    elif p>=35: return "D (Pass)"
    else: return "FAIL"

def create_qr_code(data):
    if not QR_AVAILABLE:
        return None
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").resize((120,120))
    return qr_img

def create_ultra_marksheet(row):
    img = Image.new('RGB', (900, 1200), 'white')
    draw = ImageDraw.Draw(img)
    try:
        font_big = ImageFont.truetype("arial.ttf", 26)
        font_med = ImageFont.truetype("arial.ttf", 20)
        font_small = ImageFont.truetype("arial.ttf", 16)
        font_tiny = ImageFont.truetype("arial.ttf", 13)
    except:
        font_big=ImageFont.load_default()
        font_med=ImageFont.load_default()
        font_small=ImageFont.load_default()
        font_tiny=ImageFont.load_default()

    draw.rectangle([0,0,900,140], fill='#8B0000')

    if st.session_state.college_logo and os.path.exists(st.session_state.college_logo):
        try:
            logo = Image.open(st.session_state.college_logo).resize((90,90))
            img.paste(logo, (20,20))
        except: pass

    draw.text((130, 15), st.session_state.college_name[:45], fill='gold', font=font_big)
    draw.text((130, 50), "Deemed to be University - UGC Approved", fill='white', font=font_small)
    draw.text((130, 75), "STATEMENT OF MARKS - WITH PHOTO & QR", fill='white', font=font_med)
    draw.text((130, 105), "2024-25 Academic Year", fill='#FFD700', font=font_small)

    y=160
    if row["Photo"] and os.path.exists(str(row["Photo"])):
        try:
            p = Image.open(str(row["Photo"])).resize((140,170))
            img.paste(p, (30,y))
            draw.rectangle([30,y,170,y+170], outline='#8B0000', width=3)
        except: pass
    else:
        draw.rectangle([30,y,170,y+170], outline='black', width=2)
        draw.text((50, y+70), "No Photo", fill='black', font=font_small)

    qr_data = f"Verified: {row['Roll No']} | {row['Name']} | {row['Total']}/500 | {row['Percentage']}%"
    qr_img = create_qr_code(qr_data)
    if qr_img:
        img.paste(qr_img, (750, y))
        draw.text((740, y+125), "Scan to Verify", fill='black', font=font_tiny)

    draw.text((200, y), f"Roll No: {row['Roll No']} | Rank: #{row.get('Rank',1)}", fill='black', font=font_med)
    draw.text((200, y+30), f"Name: {str(row['Name'])[:30]}", fill='black', font=font_med)
    draw.text((200, y+60), f"Class: {str(row.get('Class','B.Tech'))}", fill='black', font=font_small)
    draw.text((200, y+85), f"Email: {str(row.get('Email',''))[:30]}", fill='black', font=font_small)
    draw.text((200, y+110), f"Grade: {row['Grade']} | {row['Percentage']}%", fill='#8B0000', font=font_med)

    ty=380
    draw.rectangle([20,ty,880,ty+40], fill='#8B0000')
    draw.text((30, ty+10), "SUBJECT", fill='white', font=font_med)
    draw.text((350, ty+10), "MARKS OBTAINED", fill='white', font=font_med)
    draw.text((650, ty+10), "MAX MARKS", fill='white', font=font_med)

    subs=[("Sub1", row['Telugu']),("Sub2", row['English']),("Sub3", row['Maths']),("Sub4", row['Science']),("Sub5", row['Social'])]
    for i,(s,m) in enumerate(subs):
        yy=ty+50+i*50
        draw.rectangle([20,yy,880,yy+45], fill="#fff9c4" if i%2==0 else "white")
        draw.text((30, yy+12), f"{s}", fill='black', font=font_small)
        draw.text((380, yy+12), str(m), fill='black', font=font_med)
        draw.text((670, yy+12), "100", fill='black', font=font_small)

    total_y=ty+320
    draw.rectangle([20,total_y,880,total_y+80], fill='gold')
    draw.text((30, total_y+10), f"TOTAL MARKS: {row['Total']}/500", fill='black', font=font_big)
    draw.text((30, total_y+45), f"PERCENTAGE: {row['Percentage']}% | GRADE: {row['Grade']}", fill='#8B0000', font=font_med)

    draw.text((30, 1100), "Principal Signature", fill='black', font=font_small)
    draw.text((350, 1100), "Controller of Exams", fill='black', font=font_small)
    draw.text((650, 1100), "Date: 2025 | QR Verified", fill='black', font=font_tiny)

    return img

with st.sidebar:
    st.markdown("### 🔐 RollNo + python + OTP")
    if not st.session_state.logged_in:
        if not st.session_state.otp_sent:
            roll = st.text_input("Roll No / admin")
            pwd = st.text_input("Password", type="password", placeholder="python")
            if st.button("Get OTP", use_container_width=True):
                if pwd!=PASSWORD: st.error("Password=python")
                else:
                    if roll==ADMIN or (not df.empty and roll in df["Roll No"].astype(str).values):
                        st.session_state.otp=str(random.randint(100000,999999))
                        st.session_state.otp_sent=True
                        st.session_state.logged_user=roll
                        st.session_state.is_admin=(roll==ADMIN)
                        st.rerun()
                    else: st.error("Roll not found! Admin first")
        else:
            st.success(f"OTP for {st.session_state.logged_user}")
            st.markdown(f"<div style='background:yellow; padding:10px; border-radius:10px; text-align:center; border:2px solid red;'><h1 style='color:red;'>{st.session_state.otp}</h1></div>", unsafe_allow_html=True)
            ot = st.text_input("OTP Enter")
            if st.button("Verify", use_container_width=True):
                if ot==st.session_state.otp:
                    st.session_state.logged_in=True
                    st.session_state.otp_sent=False
                    st.rerun()
                else: st.error("Wrong")
            if st.button("Back"): st.session_state.otp_sent=False; st.rerun()
    else:
        st.success(f"Logged: {st.session_state.logged_user} {'(Admin)' if st.session_state.is_admin else ''}")
        if st.button("Logout"): st.session_state.logged_in=False; st.session_state.logged_user=""; st.rerun()

    if st.session_state.logged_in and st.session_state.is_admin:
        st.write("---")
        st.subheader("🏛️ College Logo (1)")
        logo_up = st.file_uploader("Logo Upload", type=["png","jpg","jpeg"])
        if logo_up:
            Image.open(logo_up).save(LOGO_FILE)
            st.session_state.college_logo=LOGO_FILE
            st.success("Logo Saved!")
            st.image(logo_up, width=100)
        if st.session_state.college_logo and os.path.exists(st.session_state.college_logo):
            st.image(st.session_state.college_logo, width=80)
            if st.button("Remove Logo"): os.remove(LOGO_FILE); st.session_state.college_logo=""; st.rerun()

        st.write("---")
        with st.form("add", clear_on_submit=True):
            st.subheader("➕ Add Student")
            r = st.text_input("Roll No *")
            n = st.text_input("Name *")
            em = st.text_input("Email")
            cl = st.text_input("Class", value="B TECH 2nd year")
            t = st.number_input("S1",0,100,0)
            e = st.number_input("S2",0,100,0)
            m = st.number_input("S3",0,100,0)
            sc = st.number_input("S4",0,100,0)
            so = st.number_input("S5",0,100,0)
            ph = st.file_uploader("📸 Photo", type=["jpg","jpeg","png"])
            if st.form_submit_button("Save"):
                if r and n:
                    os.makedirs("photos", exist_ok=True)
                    pp=""
                    if ph:
                        pp=f"photos/{r}.png"
                        Image.open(ph).save(pp)
                    tot=t+e+m+sc+so
                    per=tot/5
                    new={"Roll No":r,"Name":n,"Class":cl,"Email":em,"Telugu":t,"English":e,"Maths":m,"Science":sc,"Social":so,"Total":tot,"Percentage":round(per,2),"Grade":get_grade(per),"Photo":pp}
                    st.session_state.df=pd.concat([df, pd.DataFrame([new])], ignore_index=True)
                    st.session_state.df.to_csv(DATA_FILE, index=False)
                    st.success(f"Saved {r}"); st.rerun()

if st.session_state.logged_in:
    df_sorted = df.sort_values(by="Total", ascending=False).reset_index(drop=True) if not df.empty else df
    if not df_sorted.empty:
        df_sorted["Rank"]=df_sorted["Total"].rank(method="dense", ascending=False).astype(int)

    if not df_sorted.empty:
        st.subheader("🏆 Top 3 Toppers with Photos")
        top3 = df_sorted.head(3)
        cols = st.columns(3)
        medals = ["🥇 GOLD - 1st", "🥈 SILVER - 2nd", "🥉 BRONZE - 3rd"]
        colors = ["#FFD700", "#C0C0C0", "#CD7F32"]
        for idx,(i,row) in enumerate(top3.iterrows()):
            with cols[idx]:
                st.markdown(f"<div style='background:{colors[idx]}; padding:10px; border-radius:10px; text-align:center; border:3px solid #8B0000;'><h4>{medals[idx]}</h4></div>", unsafe_allow_html=True)
                if row["Photo"] and os.path.exists(str(row["Photo"])):
                    st.image(str(row["Photo"]), width=200)
                st.write(f"**{row['Name']}** {row['Roll No']} {row['Total']}/500 {row['Percentage']}%")

    if st.session_state.is_admin and not df_sorted.empty:
        st.subheader("📦 All ZIP Download")
        if st.button("Create ZIP of All Photo Marksheets"):
            zip_buf = io.BytesIO()
            with zipfile.ZipFile(zip_buf, 'w') as z:
                for i,row in df_sorted.iterrows():
                    mark_img = create_ultra_marksheet(row)
                    img_buf = io.BytesIO()
                    mark_img.save(img_buf, format="PNG")
                    z.writestr(f"{row['Roll No']}_{row['Name']}.png", img_buf.getvalue())
            st.download_button("⬇️ Download ZIP", zip_buf.getvalue(), "All_Marksheets.zip", "application/zip", use_container_width=True)

    if st.session_state.is_admin:
        filtered = df_sorted
    else:
        filtered = df_sorted[df_sorted["Roll No"].astype(str)==str(st.session_state.logged_user)] if not df_sorted.empty else pd.DataFrame()

    for i,row in filtered.iterrows():
        if st.session_state.editing_roll == str(row["Roll No"]) and st.session_state.is_admin:
            st.info(f"Editing {row['Roll No']}")
            with st.form(f"edit_{row['Roll No']}"):
                c1,c2 = st.columns(2)
                with c1:
                    en = st.text_input("Name", value=row['Name'])
                    ec = st.text_input("Class", value=row.get('Class',''))
                    et = st.number_input("S1",0,100,int(row['Telugu']))
                    ee2 = st.number_input("S2",0,100,int(row['English']))
                    em = st.number_input("S3",0,100,int(row['Maths']))
                with c2:
                    esc = st.number_input("S4",0,100,int(row['Science']))
                    eso = st.number_input("S5",0,100,int(row['Social']))
                    eph = st.file_uploader("New Photo", type=["jpg","jpeg","png"], key=f"eph{i}")
                if st.form_submit_button("Save Changes"):
                    tot=et+ee2+em+esc+eso
                    per=tot/5
                    pp=row["Photo"]
                    if eph:
                        os.makedirs("photos", exist_ok=True)
                        pp=f"photos/{row['Roll No']}.png"
                        Image.open(eph).save(pp)
                    st.session_state.df.loc[st.session_state.df["Roll No"].astype(str)==str(row["Roll No"]), ["Name","Class","Telugu","English","Maths","Science","Social","Total","Percentage","Grade","Photo"]] = [en,ec,et,ee2,em,esc,eso,tot,round(per,2),get_grade(per),pp]
                    st.session_state.df.to_csv(DATA_FILE, index=False)
                    st.session_state.editing_roll=None
                    st.rerun()
                if st.form_submit_button("Cancel"):
                    st.session_state.editing_roll=None
                    st.rerun()
        else:
            col1,col2,col3,col4 = st.columns([1,2,1,1])
            with col1:
                if row["Photo"] and os.path.exists(str(row["Photo"])):
                    st.image(str(row["Photo"]), width=130)
                if st.session_state.college_logo and os.path.exists(st.session_state.college_logo):
                    st.image(st.session_state.college_logo, width=60)
            with col2:
                st.write(f"**{row['Name']} ({row['Roll No']}) Rank #{row['Rank']}**")
                st.write(f"{row.get('Class','')} | {row['Total']}/500 | {row['Percentage']}% | {row['Grade']}")
                st.write(f"S1:{row['Telugu']} S2:{row['English']} S3:{row['Maths']} S4:{row['Science']} S5:{row['Social']}")
            with col3:
                qr_data = f"{row['Roll No']}|{row['Name']}|{row['Total']}"
                qr_img = create_qr_code(qr_data)
                if qr_img:
                    buf = io.BytesIO()
                    qr_img.save(buf, format="PNG")
                    st.image(buf.getvalue(), width=100, caption="QR Verify")
            with col4:
                mark_img = create_ultra_marksheet(row)
                buf = io.BytesIO()
                mark_img.save(buf, format="PNG")
                st.download_button(f"📸 Photo+Logo+QR", buf.getvalue(), f"{row['Roll No']}_Marksheet.png", "image/png", key=f"dl{i}", use_container_width=True)
                if st.session_state.is_admin:
                    if st.button(f"✏️ Edit", key=f"ed{i}", use_container_width=True):
                        st.session_state.editing_roll=str(row["Roll No"])
                        st.rerun()
                    if st.button(f"🗑️ Delete", key=f"del{i}", use_container_width=True):
                        st.session_state.df = df[df["Roll No"].astype(str)!=str(row["Roll No"])]
                        st.session_state.df.to_csv(DATA_FILE, index=False)
                        st.rerun()
            st.divider()
else:
    st.info("Login: Roll No / python -> OTP")
