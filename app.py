import streamlit as st
import os
import glob
import subprocess
import sys

# 🚀 1. บังคับล็อกพิกัดเบราว์เซอร์ไว้ที่โฟลเดอร์โปรเจกต์ตั้งแต่ตอนเปิดแอป
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = os.path.join(os.getcwd(), ".playwright-browsers")

# 🚀 2. สั่งติดตั้งเบราว์เซอร์และแก้ปัญหาไลบรารีลีนุกซ์ขาด (รันออโต้แค่ครั้งแรกที่เปิดเครื่อง)
if not os.path.exists(os.environ["PLAYWRIGHT_BROWSERS_PATH"]):
    try:
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium", "--with-deps"], capture_output=True)
    except:
        pass

from test_script import run_automation

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Playwright Automation Test", page_icon="🤖")

st.title("🤖 ระบบทดสอบอัตโนมัติ (Playwright)")
st.write("กดปุ่มด้านล่างเพื่อสั่งให้บอทเริ่มวิ่งทดสอบระบบ และดูผลลัพธ์ของทุกลูป")

# ปุ่มกดหน้าบ้าน
if st.button("🚀 เริ่มทำการทดสอบระบบ", type="primary"):
    
    with st.spinner("⏳ บอทกำลังเปิดเบราว์เซอร์จำลองและเริ่มทำงาน... กรุณารอสักครู่"):
        
        # เคลียร์รูปเก่าทิ้งก่อน
        for old_img in glob.glob("screenshot_*.png"):
            try: os.remove(old_img)
            except: pass
            
        # ปล่อยบอทตัวจริงไปวิ่งรันงาน
        try:
            run_automation()
            st.success("🎉 ทดสอบระบบเสร็จสิ้นเรียบร้อยแล้ว!")
        except Exception as e:
            st.error(f"❌ เกิดข้อผิดพลาดขณะบอทรันระบบ: {str(e)}")

    # ค้นหาไฟล์รูปภาพทุกลูปมาแสดงผล
    image_files = sorted(glob.glob("screenshot_*.png"))
    
    if image_files:
        st.subheader("📸 รูปภาพผลลัพธ์การทดสอบของทุกลูป:")
        for img_path in image_files:
            scenario_name = img_path.replace("screenshot_", "").replace(".png", "").replace("_", " ")
            st.write(f"🔹 **ผลการทดสอบรอบ:** {scenario_name}")
            st.image(img_path, use_container_width=True)
            st.markdown("---")