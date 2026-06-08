import { test, expect } from '@playwright/test';
import fs from 'fs';
// ปรับเปลี่ยนจาก /sync มาเป็นชี้ไฟล์ตรงๆ เพื่อให้รันบนระบบ ES Module (ESM) ได้แน่นอนไม่มีเส้นแดง
import { parse } from 'csv-parse/sync';
import { QuotationRegisterPage } from './Pages/QuotationRegisterPage';

interface QuotationTestData {
  scenario: string;
  registerNo: string;
  companyName: string;
  registrationType: string;
  businessType: string;
  province: string;
  title: string;
  firstName: string;
  lastName: string;
  position: string;
  email: string;
  phone: string;
}

// 🚀 [แก้ไขจุดที่ 3] ตัดคำสั่ง path ออกทั้งหมด แล้วใช้ process.cwd() ต่อข้อความแทน
// โค้ดจะดึงพิกัดโฟลเดอร์นอกสุดของโปรเจกต์ แล้วเดินเข้าโฟลเดอร์ตามที่คุณแจ้งมาทันที
const csvFilePath = process.cwd() + '/tests/DataTest/test-data-tc.csv';

// 4. อ่านไฟล์และแปลงข้อมูลเป็น Object Array
const fileContent = fs.readFileSync(csvFilePath, { encoding: 'utf-8' });
const records: QuotationTestData[] = parse(fileContent, {
  columns: true,
  skip_empty_lines: true,
  trim: true,
  bom: true
});

// 5. วนลูปสร้าง Test Case อัตโนมัติตามตารางข้อมูล
for (const row of records) {

  test(`ทดสอบระบบเสนอราคา [${row.scenario}]`, async ({ page }) => {
    const quotationPage = new QuotationRegisterPage(page);
    await page.setViewportSize({ width: 1920, height: 3000 });


    await quotationPage.goto();

    // สเต็ป 2: กรอกข้อมูลบริษัท
    await quotationPage.fillRegisterNo(row.registerNo);
    await quotationPage.fillCompanyName(row.companyName);

    // สเต็ป 3: เลือกค่าใน Dropdown
    await quotationPage.selectRegistrationType(row.registrationType);
    await quotationPage.selectBusinessType(row.businessType);
    await quotationPage.selectProvince(row.province);

    // สเต็ป 4: กรอกข้อมูลผู้ติดต่อ
    await quotationPage.selectCustomerTitle(row.title);
    await quotationPage.fillContactName(row.firstName);
    await quotationPage.fillContactLastName(row.lastName);
    await quotationPage.fillPosition(row.position);
    await quotationPage.fillEmail(row.email);
    await quotationPage.fillPhone(row.phone);

    // สเต็ป 5: กดปุ่มถัดไป
    await quotationPage.clickNext();
    await page.waitForTimeout(1500);
    await quotationPage.submitAndWait();
    await quotationPage.verifyAllConfirmationData({
      companyName: row.companyName,
      phone: row.phone,
      email: row.email
    });

    await page.screenshot({ path: 'screenshot.png', fullPage: true });
  });
}