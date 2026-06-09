import csv
import os
from playwright.sync_api import sync_playwright

def run_automation():
    csv_file_path = os.path.join(os.getcwd(), 'tests', 'DataTest', 'test-data-tc.csv')
    
    with open(csv_file_path, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        rows = list(reader)  # อ่านทั้งหมดก่อน เพื่อให้ใช้ใน with block ได้

    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        for row in rows:
            context = browser.new_context(viewport={"width": 1920, "height": 3000})
            page = context.new_page()

            try:
                # ✅ เปลี่ยน URL ตรงนี้เป็น URL จริง
                page.goto("https://github.com/matee-sukaim/project-kinto-automate-test-version-2.0", timeout=30000)

                # กรอกข้อมูล
                page.fill("input[name='registerNo']", row['registerNo'])
                page.fill("input[name='companyName']", row['companyName'])

                # เพิ่ม step อื่นๆ ตรงนี้
                # page.select_option("select[name='province']", row['province'])
                # page.click("button#next")
                # page.wait_for_load_state("networkidle")

                # แคปหน้าจอ
                scenario_clean = row['scenario'].replace(" ", "_")
                save_path = os.path.join(os.getcwd(), f"screenshot_{scenario_clean}.png")
                page.screenshot(path=save_path, full_page=True)

                results.append({"scenario": row['scenario'], "status": "✅ สำเร็จ"})

            except Exception as e:
                # แคปหน้าจอตอน error ด้วย
                scenario_clean = row.get('scenario', 'unknown').replace(" ", "_")
                error_path = os.path.join(os.getcwd(), f"screenshot_{scenario_clean}.png")
                try:
                    page.screenshot(path=error_path, full_page=True)
                except:
                    pass
                results.append({"scenario": row.get('scenario'), "status": f"❌ {str(e)}"})

            finally:
                context.close()  # ปิด context ทุก row เพื่อล้าง session/cookie

        browser.close()

    return results  # ส่งผลกลับไปให้ app.py แสดงผล

if __name__ == "__main__":
    results = run_automation()
    for r in results:
        print(r['scenario'], "→", r['status'])