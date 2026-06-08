import csv
import os
from playwright.sync_api import sync_playwright

def run_automation():
    # ชี้ไปที่ไฟล์ CSV ในโฟลเดอร์ของคุณ
    csv_file_path = os.path.join(os.getcwd(), 'tests', 'DataTest', 'test-data-tc.csv')
    
    with open(csv_file_path, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        
        with sync_playwright() as p:
            # เปิดเบราว์เซอร์แบบไม่มีหน้าจอ (Headless) ซึ่งจำเป็นมากบน Cloud
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(viewport={"width": 1920, "height": 3000})
            page = context.new_page()
            
            # วนลูปเทสตามตารางข้อมูล CSV ทุกลูป
            for row in reader:
                # แก้ลิงก์ URL ระบบเสนอราคาของคุณตรงนี้
                page.goto("https://ชื่อเว็บระบบเสนอราคาของคุณ.com") 
                
                # ตัวอย่างการกรอกข้อมูล (เปลี่ยน selector เป็นตัวที่คุณใช้อยู่ใน POM นะครับ)
                page.fill("input[name='registerNo']", row['registerNo'])
                page.fill("input[name='companyName']", row['companyName'])
                
                # ... ใส่สเต็ปการเลือก Dropdown และกรอกผู้ติดต่อเพิ่มตรงนี้ให้ครบ ...
                # เช่น page.select_option("select[name='province']", row['province'])
                # เช่น page.click("button#next")
                
                # แคปหน้าจอสรุปผลของลูปนั้นๆ ตั้งชื่อแยกตาม Scenario เหมือนเดิม
                scenario_clean = row['scenario'].replace(" ", "_")
                save_path = os.path.join(os.getcwd(), f"screenshot_{scenario_clean}.png")
                page.screenshot(path=save_path, full_page=True)
                
            browser.close()

if __name__ == "__main__":
    run_automation()