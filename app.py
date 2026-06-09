import streamlit as st
import subprocess
import os
import glob
import sys

# บังคับตั้งค่าพิกัดเบราว์เซอร์ให้อยู่ในโฟลเดอร์หลักของระบบ Cloud
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "/home/adminuser/.cache/ms-playwright"

# ฟังก์ชันบังคับติดตั้งเบราว์เซอร์รุ่นตรงเป๊ะๆ กับที่ Error เรียกหา
def ensure_browser():
    browser_dir = os.environ["PLAYWRIGHT_BROWSERS_PATH"]
    # ถ้ายังไม่มีโฟลเดอร์ หรือโฟลเดอร์ว่างเปล่า ให้บังคับโหลดใหม่
    if not os.path.exists(browser_dir) or len(os.listdir(browser_dir)) == 0:
        with st.spinner("📦 ระบบกำลังดาวน์โหลดจิ๊กซอว์เบราว์เซอร์จำลองรุ่นตรงสเปก (ทำเฉพาะครั้งแรก ไม่เกิน 1 นาที)..."):
            # 🚀 [จุดสำคัญ] บังคับลงทั้ง chromium และ chromium-headless-shell เพื่อให้มีไฟล์รองรับทุกล็อคของระบบ
            subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], capture_output=True)
            subprocess.run([sys.executable, "-m", "playwright", "install", "chromium-headless-shell"], capture_output=True)
            
            # บังคับเปิดสิทธิ์เผื่อลีนุกซ์ล็อกไฟล์
            subprocess.run(["chmod", "-R", "777", browser_dir], capture_output=True)

from test_script import run_automation

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Playwright Automation Test", page_icon="🤖")

st.title("🤖 ระบบทดสอบอัตโนมัติ (Playwright)")
st.write("กดปุ่มด้านล่างเพื่อสั่งให้บอทเริ่มวิ่งทดสอบระบบ และดูผลลัพธ์ของทุกลูป")

# ปุ่มกดหน้าบ้าน
if st.button("🚀 เริ่มทำการทดสอบระบบ", type="primary"):
    
    # 1. ตรวจสอบและบังคับลงเบราว์เซอร์ให้ถูกรุ่นก่อน
    ensure_browser()
    
    with st.spinner("⏳ บอทกำลังเปิดเบราว์เซอร์จำลองและเริ่มทำงานตามข้อมูลใน CSV... กรุณารอสักครู่"):
        
        # เคลียร์รูปเก่าทิ้งก่อน
        for old_img in glob.glob("screenshot_*.png"):
            try: os.remove(old_img)
            except: pass
            
        # 2. ปล่อยบอทตัวจริงไปวิ่งรันงาน
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