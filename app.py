import streamlit as st
import subprocess
import os
import glob
import sys

# เปลี่ยนมาใช้โฟลเดอร์ใน /tmp ที่ Streamlit Cloud อนุญาตให้เขียนได้เสมอ
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "/tmp/ms-playwright"

@st.cache_resource(show_spinner="📦 กำลังติดตั้งเบราว์เซอร์จำลอง (ทำครั้งเดียว)...")
def ensure_browser():
    browser_dir = "/tmp/ms-playwright"
    os.makedirs(browser_dir, exist_ok=True)

    result1 = subprocess.run(
        [sys.executable, "-m", "playwright", "install", "chromium"],
        capture_output=True, text=True
    )
    result2 = subprocess.run(
        [sys.executable, "-m", "playwright", "install-deps", "chromium"],
        capture_output=True, text=True
    )

    return result1.returncode, result2.returncode


r1, r2 = ensure_browser()

from test_script import run_automation

st.set_page_config(page_title="Playwright Automation Test", page_icon="🤖")
st.title("🤖 ระบบทดสอบอัตโนมัติ (Playwright)")

if r1 == 0:
    st.success("✅ เบราว์เซอร์พร้อมใช้งาน")
else:
    st.warning("⚠️ ติดตั้งเบราว์เซอร์อาจมีปัญหา — ลองรันดูก่อน")

st.write("กดปุ่มด้านล่างเพื่อสั่งให้บอทเริ่มวิ่งทดสอบระบบ และดูผลลัพธ์ของทุกลูป")

if st.button("🚀 เริ่มทำการทดสอบระบบ", type="primary"):

    for old_img in glob.glob("screenshot_*.png"):
        try:
            os.remove(old_img)
        except:
            pass

    with st.spinner("⏳ บอทกำลังเปิดเบราว์เซอร์จำลองและเริ่มทำงานตามข้อมูลใน CSV..."):
        try:
            results = run_automation()
            st.success("🎉 ทดสอบระบบเสร็จสิ้นเรียบร้อยแล้ว!")

            st.subheader("📊 สรุปผลการทดสอบทุก Scenario:")
            for r in results:
                st.write(f"{r['status']} — **{r['scenario']}**")

        except Exception as e:
            st.error(f"❌ เกิดข้อผิดพลาดขณะบอทรันระบบ: {str(e)}")

    st.markdown("---")
    
    # ดึงพิกัดปัจจุบันให้ชัวร์ ป้องกันปัญหาตำแหน่งไฟล์บนเซิร์ฟเวอร์จำลอง คลาดเคลื่อน
    current_dir = os.getcwd()
    image_files = sorted(glob.glob(os.path.join(current_dir, "screenshot_*.png")))
    
    if image_files:
        st.subheader("📸 รูปภาพผลลัพธ์การทดสอบในแต่ละ Scenario:")
        st.info(f"💡 พบรูปภาพหลักฐานทั้งหมด {len(image_files)} รูป")
        
        for img_path in image_files:
            # ดึงเฉพาะชื่อไฟล์ออกมาตัดแต่ง (เช่น /mount/src/.../screenshot_Test_1.png -> Test 1)
            file_name = os.path.basename(img_path)
            scenario_name = (
                file_name
                .replace("screenshot_", "")
                .replace(".png", "")
                .replace("_", " ")
            )
            
            # ใช้ st.expander ม้วนเก็บรูปไว้ เพื่อให้หน้าเว็บสแกนตรวจงานง่าย ไม่ยาวเป็นหางว่าว
            with st.expander(f"🔍 ดูภาพหลักฐานรอบ: {scenario_name}", expanded=True):
                st.image(img_path, caption=f"ภาพหน้าจอของ Scenario: {scenario_name}", use_container_width=True)
                
                # เพิ่มปุ่มดาวน์โหลดรูปภาพเผื่อพี่ต้องส่งให้ทีมดู
                with open(img_path, "rb") as file:
                    st.download_button(
                        label=f"📥 ดาวน์โหลดรูปภาพ ({scenario_name})",
                        data=file,
                        file_name=file_name,
                        mime="image/png",
                        key=file_name # ป้องกันปุ่มตีกันบน Streamlit
                    )
    else:
        st.warning("⚠️ ไม่พบรูปภาพผลลัพธ์การทดสอบในโฟลเดอร์ระบบ")
        st.info(
            "💡 คำแนะนำในการตรวจสอบ:\n"
            "1. ตรวจสอบใน `test_script.py` ว่าเขียนตำแหน่งเซฟภาพด้วย `os.path.join(os.getcwd(), f'screenshot_{scenario}.png')` ชี้มาที่เดียวกันหรือไม่\n"
            "2. หาก Scenario ไหนติด Error ลองเช็กดูว่าบอทสามารถรันคำสั่ง `page.screenshot` ได้ทันก่อนที่เบราว์เซอร์จะหลุดปิดตัวหรือไม่"
        )