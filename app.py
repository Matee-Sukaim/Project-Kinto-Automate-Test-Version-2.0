import streamlit as st
import subprocess
import os
import shutil

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Playwright Automation Test", page_icon="🤖")

st.title("ระบบทดสอบอัตโนมัติ (Playwright)")
st.write("กดปุ่มด้านล่างเพื่อสั่งให้บอทเริ่มวิ่งทดสอบระบบ และดูผลลัพธ์ผ่านรูปภาพ")

# 1. ปุ่มกดหน้าบ้าน
if st.button("🚀 เริ่มทำการทดสอบระบบ"):
    
    with st.spinner("⏳ ระบบกำลังเตรียมเครื่องมือและเปิดเบราว์เซอร์... (หากรันครั้งแรกอาจใช้เวลา 1-2 นาที)"):
        
        # --- [โซนแก้ปัญหาเออร์เรอร์บน Linux Cloud] ---
        # เช็กก่อนว่าบนเซิร์ฟเวอร์มีคำสั่ง npx หรือ node หรือยัง ถ้ายังไม่มี (เช่นบน Cloud) จะสั่งติดตั้งสดๆ
        if not shutil.which("npx") and not shutil.which("node"):
            # ดาวน์โหลดและติดตั้ง Node.js เวอร์ชันพกพาลง Linux Cloud ทันที
            subprocess.run("curl -fsSL https://deb.nodesource.com/setup_18.x | bash -", shell=True, capture_output=True)
            subprocess.run("apt-get install -y nodejs", shell=True, capture_output=True)
            
        # สั่งติดตั้งเบราว์เซอร์และเครื่องมือของ Playwright สำหรับฝั่ง Node.js
        subprocess.run(["npx", "playwright", "install", "--with-deps"], capture_output=True)
        # --------------------------------------------

        # 2. สั่งรันสคริปต์เทส Playwright ตัวเก่งของคุณ 
        # (ตรวจสอบให้แน่ใจว่าในโค้ดเทสมีการเขียนสั่งให้แคปหน้าจอชื่อ screenshot.png ด้วยนะครับ)
        result = subprocess.run(["npx", "playwright", "test"], capture_output=True, text=True)

    st.success("🎉 ทดสอบระบบเสร็จสิ้นเรียบร้อยแล้ว!")
    
    # 3. ดึงรูปภาพผลลัพธ์มาแสดงผล
    if os.path.exists("screenshot.png"):
        st.subheader("📸 รูปภาพผลลัพธ์การทดสอบล่าสุด:")
        st.image("screenshot.png", use_container_width=True)
    else:
        st.warning("⚠️ บอทรันผ่าน แต่ไม่พบไฟล์ภาพหลักฐาน (screenshot.png) ในระบบ")
        st.info("💡 คำแนะนำ: ใส่คำสั่งแคปหน้าจอในสคริปต์เทสของคุณ และเซฟชื่อไฟล์ว่า screenshot.png นะครับ")