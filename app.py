import subprocess
import os
import sys

# 🚀 ด่านตรวจเช็กส่วนกลาง: สั่งดาวน์โหลดและติดตั้งเบราว์เซอร์ Chromium ทันทีตั้งแต่เสี้ยววินาทีแรกที่แอปถูกเปิดตัวบน Cloud
# วิธีนี้จะโหลดเบราว์เซอร์มารอไว้หลังบ้าน โดยไม่ติดปัญหาเรื่องบล็อก Permission ตอนกดปุ่มหน้าเว็บ
if not os.path.exists('/home/appuser/.cache/ms-playwright') and not os.path.exists('/home/adminuser/.cache/ms-playwright'):
    try:
        # ใช้ sys.executable เพื่อวิ่งท่อ Python เดียวกับที่ Streamlit ทำงานอยู่ ป้องกันการเซฟไฟล์รูปผิดโฟลเดอร์
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium", "--with-deps"], capture_output=True)
    except:
        pass

# นำเข้าไลบรารีหลักสำหรับแสดงผลหน้าบ้าน
import streamlit as st
import glob
from test_script import run_automation  # ดึงฟังก์ชันเทสระบบเสนอราคาที่เราเขียนไว้ใน test_script.py มาใช้

# ตั้งค่าหน้าเว็บสไตล์โมเดิร์น
st.set_page_config(page_title="Playwright Automation Test", page_icon="🤖", layout="centered")

# หัวข้อหลักหน้าเว็บ
st.title("🤖 ระบบทดสอบอัตโนมัติ (Playwright)")
st.write("ระบบจะอ่านข้อมูลจากไฟล์ CSV วนลูปกรอกข้อมูลระบบเสนอราคา และบันทึกรูปภาพผลลัพธ์ของทุกลูปมาแสดงด้านล่าง")
st.markdown("---")

# 1. ปุ่มกดสั่งรันบอทหน้าบ้าน
if st.button("🚀 เริ่มทำการทดสอบระบบ", type="primary", use_container_width=True):
    
    # แสดงสถานะกำลังรันพร้อมแอนิเมชันดาวหมุน
    with st.spinner("⏳ บอทกำลังเริ่มทำงานและเปิดเบราว์เซอร์จำลองหลังบ้าน... กรุณารอสักครู่ (ทุกลูปใช้เวลาประมาณ 1-2 นาที)"):
        
        # 🧹 เคลียร์รูปภาพผลลัพธ์เก่าของรอบก่อน ๆ ทิ้งไปก่อน เพื่อไม่ให้ภาพปนกันเวลารันรอบใหม่
        for old_img in glob.glob("screenshot_*.png"):
            try:
                os.remove(old_img)
            except:
                pass
            
        # 2. เรียกฟังก์ชันรันบอทเทสอัตโนมัติแบบ Native ที่ส่งมาจากไฟล์ test_script.py
        try:
            run_automation()
            st.success("🎉 บอทวิ่งทำงานวนลูปและทดสอบระบบเสร็จสิ้นเรียบร้อยแล้ว!")
        except Exception as e:
            st.error(f"❌ เกิดข้อผิดพลาดขณะบอทรันระบบ: {str(e)}")
            st.info("💡 คำแนะนำ: ตรวจสอบความถูกต้องของสคริปต์กรอกข้อมูล หรือ Selector ในไฟล์เทสหลักของคุณอีกครั้ง")

    st.markdown("---")

    # 3. 🔎 โซนสแกนค้นหาไฟล์รูปภาพทุกลูปมาแสดงผล (Report Zone)
    image_files = sorted(glob.glob("screenshot_*.png"))
    
    if image_files:
        st.subheader("📸 รูปภาพหลักฐานการทดสอบของทุกลูป:")
        
        # วนลูปเปิดภาพของทุกลูปแสดงผลเรียงลงมาด้านล่าง
        for img_path in image_files:
            # แปลงชื่อไฟล์ให้กลับมาเป็นชื่อรอบสคริปต์เทส เช่น "screenshot_ชุดที่_1.png" -> "ชุดที่ 1"
            scenario_name = img_path.replace("screenshot_", "").replace(".png", "").replace("_", " ")
            
            # ตกแต่งหัวข้อของแต่ละรูปภาพให้น่าอ่าน
            st.markdown(f"🔹 **ผลการทดสอบรอบ:** `{scenario_name}`")
            st.image(img_path, use_container_width=True)
            st.markdown("---") # ขีดเส้นใต้คั่นระหว่างรูปภาพของแต่ละลูป
    else:
        st.warning("⚠️ บอทรันผ่านตามกระบวนการ แต่ไม่พบไฟล์ภาพหลักฐานของลูปใด ๆ ในระบบเลย")
        st.info("💡 คำแนะนำ: อย่าลืมตรวจสอบบรรทัดสุดท้ายในไฟล์ `test_script.py` ว่าใส่คำสั่ง `page.screenshot` บังคับเซฟชื่อขึ้นต้นด้วย `screenshot_` ไว้ถูกต้องแล้วหรือยัง")