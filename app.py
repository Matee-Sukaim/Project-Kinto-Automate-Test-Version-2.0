import streamlit as st
import subprocess
import os

# ตั้งค่าหน้าเว็บให้สวยงาม
st.set_page_config(page_title="Playwright Automation Test", page_icon="🤖")

st.title("ระบบทดสอบอัตโนมัติ (Playwright)")
st.write("กดปุ่มด้านล่างเพื่อสั่งให้บอทเริ่มวิ่งทดสอบระบบ และดูผลลัพธ์ผ่านรูปภาพ")

# 1. สร้างปุ่มกด
if st.button("🚀 เริ่มทำการทดสอบระบบ"):
    
    # 2. แสดงสถานะกำลังรันระบบ
    with st.spinner("⏳ บอทกำลังเริ่มทำงานและเปิดเบราว์เซอร์... กรุณารอสักครู่"):
        
        # สั่งให้ระบบดาวน์โหลดเบราว์เซอร์ของ Playwright มาเตรียมพร้อม (ทำเฉพาะครั้งแรกที่กด)
        subprocess.run(["npx", "playwright", "install", "--with-deps"], capture_output=True)
        
        # สั่งรันโค้ดเทสตัวเดิมของคุณ (มันจะสร้างไฟล์รายงานผลเทสอันใหม่)
        result = subprocess.run(["npx", "playwright", "test"], capture_output=True, text=True)
        
        # ก๊อปปี้รายงานผลเทสมาทับไฟล์หน้าแรกเพื่อความชัวร์
        if os.path.exists("playwright-report/index.html"):
            subprocess.run(["cp", "playwright-report/index.html", "index.html"])

    st.success("🎉 ทดสอบระบบเสร็จสิ้นเรียบร้อยแล้ว!")
    
    # 3. การแสดงผลลัพธ์เป็นรูปภาพตามที่คุณต้องการ
    # (สมมติว่าในโค้ดสคริปต์เทสของคุณ มีการสั่งให้เซฟรูปหลักฐานชื่อ screenshot.png ไว้ในเครื่อง)
    if os.path.exists("screenshot.png"):
        st.subheader("📸 รูปภาพผลลัพธ์การทดสอบล่าสุด:")
        st.image("screenshot.png", use_container_width=True)
    else:
        st.warning("⚠️ บอทรันผ่าน แต่ไม่พบไฟล์ภาพหลักฐาน (screenshot.png) ในระบบ")
        st.info("💡 ทริค: ตรวจสอบให้แน่ใจว่าในสคริปต์เทสของคุณ มีคำสั่งแคปหน้าจอเซฟเป็นชื่อไฟล์นี้ด้วยนะ")