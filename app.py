import streamlit as st
import subprocess
import os
import glob
import sys

# 🚀 บังคับให้ Playwright ติดตั้งและเรียกใช้เบราว์เซอร์จากโฟลเดอร์โปรเจกต์นี้เท่านั้น 
# ตัดปัญหาเรื่องหาโฟลเดอร์ /home/appuser หรือ /home/adminuser ไม่เจอเด็ดขาด
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = os.path.join(os.getcwd(), ".playwright-browsers")

from test_script import run_automation

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Playwright Automation Test", page_icon="🤖")

st.title("🤖 ระบบทดสอบอัตโนมัติ (Playwright)")
st.write("กดปุ่มด้านล่างเพื่อสั่งให้บอทเริ่มวิ่งทดสอบระบบ และดูผลลัพธ์ของทุกลูป")

# 1. ปุ่มกดหน้าบ้าน
if st.button("🚀 เริ่มทำการทดสอบระบบ", type="primary"):
    
    with st.spinner("⏳ ระบบกำลังเตรียมเบราว์เซอร์และเริ่มรันบอท... กรุณารอสักครู่ (ครั้งแรกจะใช้เวลาดาวน์โหลด 1-2 นาที)"):
        
        # เคลียร์รูปเก่าทิ้งก่อน
        for old_img in glob.glob("screenshot_*.png"):
            try: os.remove(old_img)
            except: pass
            
        # 🚀 สั่งติดตั้งเบราว์เซอร์สด ๆ ลงโฟลเดอร์จำลองที่เราล็อกไว้ด้านบน
        try:
            subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], capture_output=True)
        except Exception as install_err:
            st.warning(f"⚠️ บันทึกระบบติดตั้งเบราว์เซอร์: {str(install_err)}")
            
        # 2. ปล่อยบอทตัวจริงไปวิ่งกรอกข้อมูล
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