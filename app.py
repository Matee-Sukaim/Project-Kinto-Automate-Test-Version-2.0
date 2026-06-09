import streamlit as st
import subprocess
import os
import glob
import sys

# ตั้งค่าพิกัดเบราว์เซอร์
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "/home/adminuser/.cache/ms-playwright"

@st.cache_resource(show_spinner="📦 กำลังติดตั้งเบราว์เซอร์จำลอง (ทำครั้งเดียว)...")
def ensure_browser():
    browser_dir = os.environ["PLAYWRIGHT_BROWSERS_PATH"]
    os.makedirs(browser_dir, exist_ok=True)

    result1 = subprocess.run(
        [sys.executable, "-m", "playwright", "install", "chromium"],
        capture_output=True, text=True
    )
    result2 = subprocess.run(
        [sys.executable, "-m", "playwright", "install-deps", "chromium"],
        capture_output=True, text=True
    )
    subprocess.run(["chmod", "-R", "755", browser_dir], capture_output=True)

    return result1.returncode, result2.returncode


# ติดตั้งเบราว์เซอร์ตอน app โหลด
r1, r2 = ensure_browser()

from test_script import run_automation

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Playwright Automation Test", page_icon="🤖")
st.title("🤖 ระบบทดสอบอัตโนมัติ (Playwright)")

# แสดงสถานะ browser
if r1 == 0:
    st.success("✅ เบราว์เซอร์พร้อมใช้งาน")
else:
    st.warning("⚠️ ติดตั้งเบราว์เซอร์อาจมีปัญหา — ลองรันดูก่อน")

st.write("กดปุ่มด้านล่างเพื่อสั่งให้บอทเริ่มวิ่งทดสอบระบบ และดูผลลัพธ์ของทุกลูป")

# ปุ่มเริ่มทดสอบ
if st.button("🚀 เริ่มทำการทดสอบระบบ", type="primary"):

    # เคลียร์รูปเก่าทิ้งก่อน
    for old_img in glob.glob("screenshot_*.png"):
        try:
            os.remove(old_img)
        except:
            pass

    with st.spinner("⏳ บอทกำลังเปิดเบราว์เซอร์จำลองและเริ่มทำงานตามข้อมูลใน CSV..."):
        try:
            results = run_automation()
            st.success("🎉 ทดสอบระบบเสร็จสิ้นเรียบร้อยแล้ว!")

            # แสดงตารางสรุปผล
            st.subheader("📊 สรุปผลการทดสอบทุก Scenario:")
            for r in results:
                st.write(f"{r['status']} — **{r['scenario']}**")

        except Exception as e:
            st.error(f"❌ เกิดข้อผิดพลาดขณะบอทรันระบบ: {str(e)}")

    # แสดงรูปภาพผลลัพธ์ทุกลูป
    image_files = sorted(glob.glob("screenshot_*.png"))
    if image_files:
        st.subheader("📸 รูปภาพผลลัพธ์การทดสอบของทุกลูป:")
        for img_path in image_files:
            scenario_name = (
                img_path
                .replace("screenshot_", "")
                .replace(".png", "")
                .replace("_", " ")
            )
            st.write(f"🔹 **ผลการทดสอบรอบ:** {scenario_name}")
            st.image(img_path, use_container_width=True)
            st.markdown("---")
    else:
        st.info("ℹ️ ไม่พบรูปภาพผลลัพธ์ — อาจเกิด error ก่อนแคปหน้าจอได้")