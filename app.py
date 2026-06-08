import streamlit as st
import subprocess
import os
import glob
import sys
from test_script import run_automation

# 🚀 [แก้ไขจุดที่ 1] ย้ายมาสั่งติดตั้งตรงนี้ เพื่อให้ทำงานทันทีตั้งแต่แอปเริ่มเปิดเครื่อง (Startup)
# วิธีนี้จะโหลดเบราว์เซอร์มารอไว้เลย โดยไม่ติดปัญหาเรื่องบล็อก Permission ตอนกดปุ่ม
if "browser_installed" not in st.session_state:
    try:
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium", "--with-deps"], capture_output=True)
        st.session_state["browser_installed"] = True
    except:
        pass

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Playwright Automation Test", page_icon="🤖")

st.title("ระบบทดสอบอัตโนมัติ (Playwright)")
st.write("กดปุ่มด้านล่างเพื่อสั่งให้บอทเริ่มวิ่งทดสอบระบบ และดูผลลัพธ์ของทุกลูป")

# 1. ปุ่มกดหน้าบ้าน
if st.button("🚀 เริ่มทำการทดสอบระบบ"):
    
    with st.spinner("⏳ บอทกำลังเริ่มทำงานและเปิดเบราว์เซอร์... กรุณารอสักครู่"):
        
        # เคลียร์รูปเก่าทิ้ง
        for old_img in glob.glob("screenshot_*.png"):
            try: os.remove(old_img)
            except: pass
            
        # 2. เรียกฟังก์ชันรันบอทเทสอัตโนมัติแบบ Native (ไม่ต้องสั่ง install ตรงนี้แล้ว)
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