import csv
import os
import time
from playwright.sync_api import sync_playwright

def run_automation():
    # ชี้ไปที่โฟลเดอร์เก็บไฟล์ CSV ของพี่
    csv_file_path = os.path.join(os.getcwd(), 'tests', 'DataTest', 'test-data-tc.csv')
    
    with open(csv_file_path, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        for row in rows:
            context = browser.new_context(viewport={"width": 1920, "height": 3000})
            page = context.new_page()

            try:
                # 🌐 1. เปิดเข้าหน้า Quotation Form ของ KintoONE ตามที่พี่ระบุมา
                page.goto("https://tlcl-dev.outsystemsenterprise.com/KintoONE/QuotationForm?PackageCustomerSelectedId=5239&ProductCategoryId=5", timeout=30000)
                page.wait_for_load_state("networkidle") # รอหน้าแรกโหลดนิ่ง ๆ 

                # ✍️ 2. กรอกข้อมูลตามตาราง CSV (ผมเปิดคอมเมนต์ให้รันจริงแล้วครับ)
                page.fill("input[name='registerNo']", row['registerNo'])
                page.fill("input[name='companyName']", row['companyName'])

                # -------------------------------------------------------------------------
                # 🛑 [พี่ต้องปรับจุดนี้ให้ตรงกับหน้างานจริง] ท่อนพาบอทเดินไปหน้าสุดท้าย
                # -------------------------------------------------------------------------
                # เนื่องจากหน้าสุดท้ายของ OutSystems มักจะต้องมีการกดปุ่ม "ถัดไป" หรือ "คำนวณ" หรือ "บันทึก"
                # พี่ต้องเปลี่ยนคำว่า "button.btn-next" หรือ "text=ถัดไป" ให้ตรงกับ Selector ปุ่มบนเว็บจริงของพี่ครับ
                
                # ตัวอย่างท่าที่ 1: สั่งคลิกโดยหาจากข้อความบนปุ่มตรง ๆ
                page.click("text=ถัดไป") 
                
                # ตัวอย่างท่าที่ 2: สั่งคลิกปุ่มบันทึกหรือส่งข้อมูลหน้าถัดไปเพื่อให้ไปหน้าสุดท้าย
                # page.click("button#CalculateButton")
                
                # ⏳ 3. บังคับให้บอท "หยุดรอ" จนกว่าตัวเลขผลลัพธ์หรือหน้าสุดท้ายจะโหลดข้อมูลเสร็จ 100%
                page.wait_for_load_state("networkidle")
                time.sleep(5) # แรปแถมเพิ่มให้อีก 3 วินาทีเพื่อให้มั่นใจว่าหน้าจอไม่ขาว/ไม่โหลดค้าง
                # -------------------------------------------------------------------------

                # 📸 4. บรรทัดนี้แหละครับ! เมื่อบอทมันรอจนหน้านิ่งที่ "หน้าสุดท้าย" แล้ว 
                # สั่งแคปภาพหน้าเว็บเต็ม ๆ เซฟไฟล์ส่งกลับไปให้ app.py ดึงไปวางโชว์หน้าบ้านทันที
                scenario_clean = row['scenario'].replace(" ", "_")
                save_path = os.path.join(os.getcwd(), f"screenshot_{scenario_clean}.png")
                page.screenshot(path=save_path, full_page=True)

                results.append({"scenario": row['scenario'], "status": "✅ สำเร็จ"})

            except Exception as e:
                # ถ้าลูปไหนระเบิดค้างกลางทาง ก็ให้แคปหน้าปัจจุบัน ณ ตอนที่พังเก็บไว้เป็นหลักฐานด้วย
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