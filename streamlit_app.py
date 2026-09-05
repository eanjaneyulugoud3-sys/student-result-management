import streamlit as st
import pandas as pd
import os
import random
import io
import zipfile
from PIL import Image, ImageDraw, ImageFont

st.set_page_config(page_title="Malla Reddy ULTRA PRO", layout="wide", page_icon="🏆")

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

# Try QR import
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

# Load logo
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

    # Header
    draw.rectangle([0,0,900,140], fill='#8B0000')
    # Logo
    if st.session_state.college_logo and os.path.exists(st.session_state.college_logo):
        try:
            logo = Image.open(st.session_state.college_logo).resize((90,90))
            img.paste(logo, (20,20))
        except: pass

    draw.text((130,15), st.session_state.college_name[:45], fill='gold', font=font_big)
    draw.text((130,50), "Deemed to be University - UGC Approved", fill='white', font=font_small)
    draw.text((130,75), "STATEMENT OF MARKS - WITH PHOTO & QR", fill='white', font=font_med)
    draw.text((130,105), "2024-25 Academic Year", fill='#FFD700', font=font_small)

    # Photo + QR
    y=160
    if row["Photo"] and os.path.exists(str(row["Photo"])):
        try:
            p = Image.open(str(row["Photo"])).resize((140,170))
            img.paste(p, (30,y))
            draw.rectangle([30,y,170,y+170], outline='#8B0000', width=3)
        except: pass
    else:
        draw.rectangle([30,y,170,y+170], outline='black', width=2)

    # QR Code
    qr_data = f"Verified: {row['Roll No']} | {row['Name']} | {row['Total']}/500 | {row['Percentage']}% | {st.session_state.college_name}"
    qr_img = create_qr_code(qr_data)
    if qr_img:
        img.paste(qr_img, (750, y))
        draw.text((740, y+125, "Scan to Verify"), fill='black', font=font_tiny)

    # Details
    draw.text((200,y, f"Roll No: {row['Roll No']} | Rank: #{row.get('Rank',1)}"), fill='black', font=font_med)
    draw.text((200,y+30, f"Name: {row['Name'][:30]}"), fill='black', font=font_med)
    draw.text((200,y+60, f"Class: {row.get('Class','B.Tech')}"), fill='black', font=font_small)
    draw.text((200,y+85, f"Email: {row.get('Email','')[:30]}"), fill='black', font=font_small)
    draw.text((200,y+110, f"Grade: {row['Grade']} | Percentage: {row['Percentage']}%"), fill='#8B0000', font=font_med)

    # Table
    ty=380
    draw.rectangle([20,ty,880,ty+40], fill='#8B0000')
    draw.text((30,ty+10,"SUBJECT"), fill='white', font=font_med)
    draw.text((350,ty+10,"MARKS OBTAINED"), fill='white', font=font_med)
    draw.text((650,ty+10,"MAX MARKS"), fill='white', font=font_med)
    draw.text((780,ty+10,"RESULT"), fill='white', font=font_small)

    subs=[("Sub1 - Telugu/Subject1", row['Telugu']),("Sub2 - English/Subject2", row['English']),("Sub3 - Maths/Subject3", row['Maths']),("Sub4 - Science/Subject4", row['Science']),("Sub5 - Social/Subject5", row['Social'])]
    for i,(s,m) in enumerate(subs):
        yy=ty+50+i*50
        draw.rectangle([20,yy,880,yy+45], fill="#fff9c4" if i%2==0 else "white")
        draw.text((30,yy+12,s[:30]), fill='black', font=font_small)
        draw.text((380,yy+12,str(m)), fill='black', font=font_med)
        draw.text((670,yy+12,"100"), fill='black', font=font_small)
        draw.text((780,yy+12,"P" if m>=35 else "F"), fill='green' if m>=35 else 'red', font=font_small)

    # Total
    total_y=ty+320
    draw.rectangle([20,total_y,880,total_y+80], fill='gold')
    draw.text((30,total_y+10,f"TOTAL MARKS: {row['Total']}/500"), fill='black', font=font_big)
    draw.text((30,total_y+45,f"PERCENTAGE: {row['Percentage']}% | GRADE: {row['Grade']} | {'PASS' if 'FAIL' not in row['Grade'] else 'FAIL'}"), fill='#8B0000', font=font_med)

    # Footer
    draw.text((30,1100,"Principal Signature"), fill='black', font=font_small)
    draw.text((350,1100,"Controller of Exams"), fill='black', font=font_small)
    draw.text((650,1100,f"Date: 2025 | QR Verified"), fill='black', font=font_tiny)

    return img

# ============ LOGIN ============
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

    # ADMIN FEATURES
    if st.session_state.logged_in and st.session_state.is_admin:
        st.write("---")
        st.subheader("🏛️ College Logo (1)")
        logo_up = st.file_uploader("Logo Upload", type=["png","jpg","jpeg"])
        if logo_up:
            Image.open(logo_up).save(LOGO_FILE)
            st.session_state.college_logo=LOGO_FILE
            st.success("Logo Saved! Marksheet lo vastundi")
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
            cl = st.text_input("Class", value="B.Tech")
            t = st.number_input("Sub1",0,100,0)
            e = st.number_input("Sub2",0,100,0)
            m = st.number_input("Sub3",0,100,0)
            sc = st.number_input("Sub4",0,100,0)
            so = st.number_input("Sub5",0,100,0)
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

# ============ MAIN ============
if st.session_state.logged_in:
    df_sorted = df.sort_values(by="Total", ascending=False).reset_index(drop=True) if not df.empty else df
    if not df_sorted.empty:
        df_sorted["Rank"]=df_sorted["Total"].rank(method="dense", ascending=False).astype(int)

    # 5. TOPPER LIST WITH PHOTOS
    if not df_sorted.empty:
        st.subheader("🏆 5. Top 3 Toppers with Photos + Medals")
        top3 = df_sorted.head(3)
        cols = st.columns(3)
        medals = ["🥇 GOLD MEDAL - 1st Rank", "🥈 SILVER MEDAL - 2nd Rank", "🥉 BRONZE MEDAL - 3rd Rank"]
        colors = ["#FFD700", "#C0C0C0", "#CD7F32"]
        for idx,(i,row) in enumerate(top3.iterrows()):
            with cols[idx]:
                st.markdown(f"<div style='background:{colors[idx]}; padding:15px; border-radius:15px; text-align:center; border:3px solid #8B0000;'><h3>{medals[idx]}</h3></div>", unsafe_allow_html=True)
                if row["Photo"] and os.path.exists(str(row["Photo"])):
                    st.image(str(row["Photo"]), width=200)
                else:
                    st.markdown("<div style='width:200px;height:200px;background:#eee;display:flex;align-items:center;justify-content:center;font-size:60px;'>👤</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='text-align:center;'><h2>{row['Name']}</h2><p>{row['Roll No']} | {row['Class']}</p><h3>{row['Total']}/500 | {row['Percentage']}%</h3><p>{row['Grade']}</p></div>", unsafe_allow_html=True)

        st.write("---")

    # 4. ALL STUDENTS ZIP DOWNLOAD
    if st.session_state.is_admin and not df_sorted.empty:
        st.subheader("📚 4. All Students Photo Marksheets ZIP Download")
        if st.button("📦 Create ZIP of All Photo Marksheets", use_container_width=True):
            zip_buf = io.BytesIO()
            with zipfile.ZipFile(zip_buf, 'w') as z:
                for i,row in df_sorted.iterrows():
                    mark_img = create_ultra_marksheet(row)
                    img_buf = io.BytesIO()
                    mark_img.save(img_buf, format="PNG")
                    z.writestr(f"{row['Roll No']}_{row['Name']}_Photo_Marksheet.png", img_buf.getvalue())
            st.download_button("⬇️ Download ZIP (All Marksheets with Photo+Logo+QR)", zip_buf.getvalue(), "All_Photo_Marksheets_with_QR.zip", "application/zip", use_container_width=True)
            st.success(f"ZIP Ready! {len(df_sorted)} marksheets with Logo+Photo+QR")

    # RESULTS WITH EDIT OPTION (8)
    if st.session_state.is_admin:
        filtered = df_sorted
        st.subheader(f"📋 All Results ({len(filtered)}) - 8. Edit Option")
    else:
        filtered = df_sorted[df_sorted["Roll No"].astype(str)==str(st.session_state.logged_user)] if not df_sorted.empty else pd.DataFrame()
        st.subheader(f"Your Marksheet - {st.session_state.logged_user}")

    for i,row in filtered.iterrows():
        # Check if editing this roll
        if st.session_state.editing_roll == str(row["Roll No"]) and st.session_state.is_admin:
            st.markdown(f"<div style='background:#fff3cd; padding:15px; border-radius:10px; border:2px solid gold;'><h3>✏️ Editing {row['Roll No']} - {row['Name']}</h3></div>", unsafe_allow_html=True)
            with st.form(f"edit_{row['Roll No']}"):
                c1,c2,c3 = st.columns(3)
                with c1:
                    en = st.text_input("Name", value=row['Name'])
                    ec = st.text_input("Class", value=row.get('Class','B.Tech'))
                    ee = st.text_input("Email", value=row.get('Email',''))
                with c2:
                    et = st.number_input("Sub1",0,100,int(row['Telugu']))
                    ee2 = st.number_input("Sub2",0,100,int(row['English']))
                    em = st.number_input("Sub3",0,100,int(row['Maths']))
                with c3:
                    esc = st.number_input("Sub4",0,100,int(row['Science']))
                    eso = st.number_input("Sub5",0,100,int(row['Social']))
                    eph = st.file_uploader("New Photo (optional)", type=["jpg","jpeg","png"], key=f"eph{i}")
                save_edit = st.form_submit_button("💾 Save Changes", use_container_width=True)
                cancel_edit = st.form_submit_button("❌ Cancel", use_container_width=True)
                if save_edit:
                    tot=et+ee2+em+esc+eso
                    per=tot/5
                    pp=row["Photo"]
                    if eph:
                        os.makedirs("photos", exist_ok=True)
                        pp=f"photos/{row['Roll No']}.png"
                        Image.open(eph).save(pp)
                    st.session_state.df.loc[st.session_state.df["Roll No"].astype(str)==str(row["Roll No"]), ["Name","Class","Email","Telugu","English","Maths","Science","Social","Total","Percentage","Grade","Photo"]] = [en,ec,ee,et,ee2,em,esc,eso,tot,round(per,2),get_grade(per),pp]
                    st.session_state.df.to_csv(DATA_FILE, index=False)
                    st.session_state.editing_roll=None
                    st.success("Updated!")
                    st.rerun()
                if cancel_edit:
                    st.session_state.editing_roll=None
                    st.rerun()
        else:
            # Normal Display with Logo + Photo + QR
            col_photo, col_details, col_qr, col_btns = st.columns([1,2,1,1])
            with col_photo:
                if row["Photo"] and os.path.exists(str(row["Photo"])):
                    st.image(str(row["Photo"]), width=130)
                else:
                    st.markdown("<div style='width:130px;height:150px;background:#eee;display:flex;align-items:center;justify-content:center;'>👤 No Photo</div>", unsafe_allow_html=True)
                if st.session_state.college_logo and os.path.exists(st.session_state.college_logo):
                    st.image(st.session_state.college_logo, width=60, caption="College Logo")

            with col_details:
                st.markdown(f"**{row['Name']} ({row['Roll No']})** | Rank #{row['Rank']}")
                st.write(f"{row.get('Class','B.Tech')} | {row['Total']}/500 | {row['Percentage']}% | {row['Grade']}")
                st.write(f"S1:{row['Telugu']} S2:{row['English']} S3:{row['Maths']} S4:{row['Science']} S5:{row['Social']}")

            with col_qr:
                qr_data = f"{row['Roll No']}|{row['Name']}|{row['Total']}/500|Verified"
                qr_img = create_qr_code(qr_data)
                if qr_img:
                    buf = io.BytesIO()
                    qr_img.save(buf, format="PNG")
                    st.image(buf.getvalue(), width=100, caption="3. QR Verify")
                else:
                    st.caption("3. QR Code - pip install qrcode needed")
                    st.code(qr_data)

            with col_btns:
                # Download with Logo+Photo+QR
                mark_img = create_ultra_marksheet(row)
                buf = io.BytesIO()
                mark_img.save(buf, format="PNG")
                st.download_button(f"📸 Photo+Logo+QR Marksheet", buf.getvalue(), f"{row['Roll No']}_ULTRA_Marksheet.png", "image/png", key=f"ultra{i}", use_container_width=True)

                if st.session_state.is_admin:
                    if st.button(f"✏️ 8. Edit Marks", key=f"edit_btn{i}", use_container_width=True):
                        st.session_state.editing_roll=str(row["Roll No"])
                        st.rerun()
                    if st.button(f"🗑️ Delete", key=f"del{i}", use_container_width=True):
                        st.session_state.df = df[df["Roll No"].astype(str)!=str(row["Roll No"])]
                        st.session_state.df.to_csv(DATA_FILE, index=False)
                        st.rerun()
        st.divider()

else:
    st.info("👈 Login: admin / python or Roll No / python -> OTP yellow box lo")
    if not df.empty:
        df_sorted = df.sort_values(by="Total", ascending=False).reset_index(drop=True)
        st.subheader("🏆 Top 3 Preview (Login to see full)")
        cols=st.columns(3)
        for idx,(i,row) in enumerate(df_sorted.head(3).iterrows()):
            with cols[idx]:
                if row["Photo"] and os.path.exists(str(row["Photo"])):
                    st.image(str(row["Photo"]), width=100)
                st.write(f"{row['Name']} - {row['Total']}/500")
