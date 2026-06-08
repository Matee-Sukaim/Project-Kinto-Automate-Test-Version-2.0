import streamlit as st
import subprocess
import os
import glob
from test_script import run_automation  # ดึงฟังก์ชันเทสที่เราเขียนไว้มาใช้

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Playwright Automation Test", page_icon="🤖")

st.title("ระบบทดสอบอัตโนมัติ (Playwright)")
st.write("กดปุ่มด้านล่างเพื่อสั่งให้บอทเริ่มวิ่งทดสอบระบบ และดูผลลัพธ์ของทุกลูป")

# 1. ปุ่มกดหน้าบ้าน
if st.button("🚀 เริ่มทำการทดสอบระบบ"):
    
    with st.spinner("⏳ ระบบกำลังดาวน์โหลดเบราว์เซอร์และเริ่มรันบอท... กรุณารอสักครู่ (ครั้งแรกอาจใช้เวลา 1-2 นาที)"):
        
        # เคลียร์รูปเก่าทิ้ง
        for old_img in glob.glob("screenshot_*.png"):
            try: os.remove(old_img)
            except: pass
            
        # 🚀 [แก้ไขจุดนี้] สั่งติดตั้งเบราว์เซอร์ผ่านโมดูลของ Python แบบสมบูรณ์และบังคับเอาเฉพาะ chromium
        subprocess.run(["python", "-m", "playwright", "install", "chromium", "--with-deps"], capture_output=True)
            
        # 2. เรียกฟังก์ชันรันบอทเทสอัตโนมัติแบบ Native
        try:
            run_automation()
            st.success("🎉 ทดสอบระบบเสร็จสิ้นเรียบร้อยแล้ว!")
        except Exception as e:
            st.error(f"❌ เกิดข้อผิดพลาดขณะบอทรันระบบ: {str(e)}")

    # 3. ค้นหาไฟล์รูปภาพทุกลูปมาแสดงผล
    image_files = sorted(glob.glob("screenshot_*.png"))
    
    if image_files:
        st.subheader("📸 รูปภาพผลลัพธ์การทดสอบของทุกลูป:")
        for img_path in image_files:
            scenario_name = img_path.replace("screenshot_", "").replace(".png", "").replace("_", " ")
            st.write(f"🔹 **ผลการทดสอบรอบ:** {scenario_name}")
            st.image(img_path, use_container_width=True)
            st.markdown("---")