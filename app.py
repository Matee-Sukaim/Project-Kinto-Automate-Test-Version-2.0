import streamlit as st
import subprocess
import os

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Playwright Automation Test", page_icon="🤖")

st.title("ระบบทดสอบอัตโนมัติ (Playwright)")
st.write("กดปุ่มด้านล่างเพื่อสั่งให้บอทเริ่มวิ่งทดสอบระบบ และดูผลลัพธ์ผ่านรูปภาพ")

# 1. ปุ่มกดหน้าบ้าน
if st.button("🚀 เริ่มทำการทดสอบระบบ"):
    
    with st.spinner("⏳ ระบบกำลังเปิดเบราว์เซอร์เพื่อเริ่มรันบอท... กรุณารอสักครู่"):
        
        # สั่งติดตั้งเบราว์เซอร์ลีนุกซ์ของ Playwright (คราวนี้ npx จะทำงานได้แล้วเพราะมีในระบบแล้ว)
        subprocess.run(["npx", "playwright", "install", "chromium"], capture_output=True)
            
        # 2. สั่งรันสคริปต์เทส Playwright ของคุณ
        result = subprocess.run(["npx", "playwright", "test"], capture_output=True, text=True)

    st.success("🎉 ทดสอบระบบเสร็จสิ้นเรียบร้อยแล้ว!")
    
    # 3. ดึงรูปภาพผลลัพธ์มาแสดงผล (เปลี่ยนชื่อไฟล์รูปให้ตรงกับที่สคริปต์เทสของคุณเซฟไว้นะครับ)
    if os.path.exists("screenshot.png"):
        st.subheader("📸 รูปภาพผลลัพธ์การทดสอบล่าสุด:")
        st.image("screenshot.png", use_container_width=True)
    else:
        st.warning("⚠️ บอทรันผ่าน แต่ไม่พบไฟล์ภาพหลักฐาน (screenshot.png) ในระบบ")
        st.info("💡 คำแนะนำ: ตรวจสอบให้แน่ใจว่าในสคริปต์เทสของคุณ มีคำสั่งแคปหน้าจอเซฟเป็นชื่อไฟล์นี้ด้วยนะ")