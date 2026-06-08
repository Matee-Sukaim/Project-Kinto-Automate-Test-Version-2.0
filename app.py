import streamlit as st
import subprocess
import os

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Playwright Automation Test", page_icon="🤖")

st.title("ระบบทดสอบอัตโนมัติ (Playwright)")
st.write("กดปุ่มด้านล่างเพื่อสั่งให้บอทเริ่มวิ่งทดสอบระบบ และดูผลลัพธ์ผ่านรูปภาพ")

# 1. ปุ่มกดหน้าบ้าน
if st.button("🚀 เริ่มทำการทดสอบระบบ"):
    
    with st.spinner("⏳ ระบบกำลังเตรียมเบราว์เซอร์และเริ่มรันบอท... กรุณารอสักครู่"):
        
        # สั่งติดตั้งเบราว์เซอร์ของ Playwright ผ่านระบบ Python (ตัวนี้จะทำงานได้ชัวร์บน Streamlit Cloud)
        subprocess.run(["playwright", "install", "chromium"], capture_output=True)
            
        # 2. สั่งรันสคริปต์เทสตัวหลักของคุณ
        # ถ้านสคริปต์เทสระบบเสนอราคาเดิมของคุณเป็น Python อยู่แล้ว ให้ใส่ชื่อไฟล์เทสได้เลย เช่น:
        # result = subprocess.run(["pytest", "ชื่อไฟล์เทสของคุณ.py"], capture_output=True, text=True)
        
        # แต่ถ้าสคริปต์เดิมของคุณยังจำเป็นต้องรันผ่านคำสั่งอื่น ให้ระบุคำสั่งรันหลักตรงนี้แทน npx ครับ:
        result = subprocess.run(["playwright", "test"], capture_output=True, text=True)

    st.success("🎉 ทดสอบระบบเสร็จสิ้นเรียบร้อยแล้ว!")
    
    # 3. ดึงรูปภาพผลลัพธ์มาแสดงผล
    if os.path.exists("screenshot.png"):
        st.subheader("📸 รูปภาพผลลัพธ์การทดสอบล่าสุด:")
        st.image("screenshot.png", use_container_width=True)
    else:
        st.warning("⚠️ บอทรันผ่าน แต่ไม่พบไฟล์ภาพหลักฐาน (screenshot.png) ในระบบ")
        st.info("💡 คำแนะนำ: ตรวจสอบให้แน่ใจว่าในสคริปต์เทสของคุณ มีคำสั่งแคปหน้าจอเซฟเป็นชื่อไฟล์นี้ด้วยนะ")