import streamlit as st
import subprocess
import os
import glob

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Playwright Automation Test", page_icon="🤖")

st.title("ระบบทดสอบอัตโนมัติ (Playwright)")
st.write("กดปุ่มด้านล่างเพื่อสั่งให้บอทเริ่มวิ่งทดสอบระบบ และดูผลลัพธ์ของทุกลูป")

# 1. ปุ่มกดหน้าบ้าน
if st.button("🚀 เริ่มทำการทดสอบระบบ"):
    
    with st.spinner("⏳ ระบบกำลังเริ่มรันบอทเทส... กรุณารอสักครู่"):
        
        # ลบไฟล์รูปเก่าของรอบก่อนๆ ทิ้งไปก่อน เพื่อไม่ให้ปนกับรอบใหม่
        for old_img in glob.glob("screenshot_*.png"):
            try: os.remove(old_img)
            except: pass
            
        # มั่นใจว่าติดตั้ง Chromium แล้ว
        subprocess.run(["playwright", "install", "chromium"], capture_output=True)
            
        # 2. สั่งรันสคริปต์เทส Playwright ตัวเก่งของคุณ
        result = subprocess.run(["npx", "playwright", "test"], capture_output=True, text=True)

    st.success("🎉 ทดสอบระบบเสร็จสิ้นเรียบร้อยแล้ว!")
    
    # 3. 🔎 ค้นหาไฟล์รูปภาพทุกลูปที่บอทเซฟไว้มาแสดงผล
    image_files = sorted(glob.glob("screenshot_*.png"))
    
    if image_files:
        st.subheader("📸 รูปภาพผลลัพธ์การทดสอบของทุกลูป:")
        
        # วนลูปดึงรูปภาพของทุกลูปขึ้นมาแสดงบนหน้าเว็บเรียงกันลงมา
        for img_path in image_files:
            # ดึงชื่อรอบออกมาจากชื่อไฟล์เพื่อทำเป็นหัวข้อรูป เช่น "ผลการทดสอบรอบ: ชุดที่_2"
            scenario_name = img_path.replace("screenshot_", "").replace(".png", "").replace("_", " ")
            st.write(f"🔹 **ผลการทดสอบรอบ:** {scenario_name}")
            st.image(img_path, use_container_width=True)
            st.markdown("---") # ขีดเส้นใต้คั่นระหว่างรูป
    else:
        st.warning("⚠️ บอทรันผ่าน แต่ไม่พบไฟล์ภาพหลักฐานของลูปใดๆ ในระบบเลย")