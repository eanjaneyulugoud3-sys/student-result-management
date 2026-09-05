import streamlit as st
import sqlite3
import pandas as pd
from PIL import Image
import io

conn = sqlite3.connect('students.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS students (id TEXT PRIMARY KEY, name TEXT, marks INTEGER, result TEXT, photo BLOB)')
conn.commit()

st.title("📸 Student Result with Photo")

choice = st.sidebar.selectbox("Menu", ["Add Student", "View Result"])

if choice == "Add Student":
    sid = st.text_input("Student ID")
    name = st.text_input("Student Name")
    marks = st.number_input("Marks", 0, 100, 0)
    photo = st.file_uploader("Upload Student Photo", type=['jpg','jpeg','png'])

    if st.button("Save Student"):
        res = "Pass" if marks >= 35 else "Fail"
        img_bytes = photo.read() if photo else None
        try:
            c.execute("INSERT INTO students VALUES (?,?,?,?,?)", (sid, name, marks, res, img_bytes))
            conn.commit()
            st.success(f"{name} saved with photo!")
        except:
            st.error("ID already exists!")

else:
    sid = st.text_input("Enter ID to View")
    if st.button("Get Result"):
        c.execute("SELECT * FROM students WHERE id=?", (sid,))
        row = c.fetchone()
        if row:
            c1, c2 = st.columns(2)
            with c1:
                st.write(f"**Name:** {row[1]}")
                st.write(f"**Marks:** {row[2]}")
                st.write(f"**Result:** {row[3]}")
            with c2:
                if row[4]:
                    st.image(Image.open(io.BytesIO(row[4])), width=200)
                else:
                    st.warning("No photo")
        else:
            st.error("Student not found")
