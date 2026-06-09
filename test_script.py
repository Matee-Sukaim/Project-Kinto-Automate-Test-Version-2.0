import csv
import os
from playwright.sync_api import sync_playwright

def run_automation():
    # 📌 เช็กจุดนี้: ปัจจุบันระบบจะหาไฟล์จากโฟลเดอร์ tests/DataTest/test-data-tc.csv
    # ถ้าพี่วางไฟล์ไว้ข้างนอกสุด ให้แก้บรรทัดนี้เป็น: csv_file_path = os.path.join(os.getcwd(), 'test-data-tc.csv')
    csv_file_path = os.path.join(os.getcwd(), 'tests', 'DataTest', 'test-data-tc.csv')
    
    with open(csv_file_path, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    results = []

    with sync_playwright() as p:
        # เปิดเบราว์เซอร์ Chromium โดยอิงตามโฟลเดอร์ที่เราเซ็ตไว้ใน app.py
        browser = p.chromium.launch(headless=True)

        for row in rows:
            context = browser.new_context(viewport={"width": 1920, "height": 3000})
            page = context.new_page()

            try:
                # 🚀 บรรทัดนี้: เปลี่ยนเป็น URL หน้าเว็บที่ต้องการทดสอบจริง ๆ ครับพี่ (ตอนนี้ใส่ตัวอย่างเว็บจำลองไว้)
                page.goto("https://www.google.com", timeout=30000)

                # บรรทัดกรอกข้อมูล (เปิดคอมเมนต์เพื่อใช้งาน Selector จริงของพี่ได้เลย)
                # page.fill("input[name='registerNo']", row['registerNo'])
                # page.fill("input[name='companyName']", row['companyName'])

                # 📸 บังคับเซฟรูปไว้ที่โฟลเดอร์หลักเพื่อให้ app.py ดึงไปโชว์หน้าบ้านได้ถูกตำแหน่ง
                scenario_clean = row['scenario'].replace(" ", "_")
                save_path = os.path.join(os.getcwd(), f"screenshot_{scenario_clean}.png")
                page.screenshot(path=save_path, full_page=True)

                results.append({"scenario": row['scenario'], "status": "✅ สำเร็จ"})

            except Exception as e:
                # กรณี Error ก็แคปหน้าจอเก็บไว้เป็นหลักฐานด้วย
                scenario_clean = row.get('scenario', 'unknown').replace(" ", "_")
                error_path = os.path.join(os.getcwd(), f"screenshot_{scenario_clean}.png")
                try:
                    page.screenshot(path=error_path, full_page=True)
                except:
                    pass
                results.append({"scenario": row.get('scenario'), "status": f"❌ {str(e)}"})

            finally:
                context.close()

        browser.close()

    return results

if __name__ == "__main__":
    results = run_automation()
    for r in results:
        print(r['scenario'], "→", r['status'])