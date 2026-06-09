import streamlit as st
import subprocess
import os
import glob
import sys
from test_script import run_automation

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Playwright Automation Test", page_icon="🤖")

st.title("ระบบทดสอบอัตโนมัติ (Playwright)")
st.write("กดปุ่มด้านล่างเพื่อสั่งให้บอทเริ่มวิ่งทดสอบระบบ และดูผลลัพธ์ของทุกลูป")

# 1. ปุ่มกดหน้าบ้าน
if st.button("🚀 เริ่มทำการทดสอบระบบ"):
    
    with st.spinner("⏳ ระบบกำลังเตรียมความพร้อมของเบราว์เซอร์... กรุณารอสักครู่ (หากรันครั้งแรกอาจใช้เวลา 1-2 นาที)"):
        
        # 🧹 เคลียร์รูปเก่าทิ้งก่อน
        for old_img in glob.glob("screenshot_*.png"):
            try: os.remove(old_img)
            except: pass
            
        # 🚀 [ทริคเด็ด] บังคับรันคำสั่งติดตั้งเบราว์เซอร์สดๆ ในปุ่มนี้เลย โดยชี้ช่องทางผ่านท่อ Python หลัก
        # วิธีนี้จะบังคับให้มันดาวน์โหลดลงโฟลเดอร์ของเซิร์ฟเวอร์เวอร์ชันนี้ตรงๆ ไม่หลงทางแน่นอน
        try:
            st.info("🔄 กำลังเช็กและอัปเดตเครื่องมือเบราว์เซอร์หลังบ้าน...")
            subprocess.run([sys.executable, "-m", "playwright", "install", "chromium", "--with-deps"], capture_output=True)
        except Exception as install_err:
            st.warning(f"⚠️ บันทึกระบบติดตั้งเบราว์เซอร์: {str(install_err)}")
            
        # 2. เมื่อเตรียมเบราว์เซอร์เสร็จ ค่อยปล่อยบอทตัวจริงไปวิ่ง
        try:
            st.info("🤖 บอทกำลังเปิดเบราว์เซอร์จำลองและเริ่มกรอกข้อมูลตาม CSV...")
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