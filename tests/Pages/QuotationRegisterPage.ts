import { Page, Locator, expect } from '@playwright/test';

export class QuotationRegisterPage {
    readonly page: Page;
    readonly url = 'https://tlcl-dev.outsystemsenterprise.com/KintoONE/QuotationForm?PackageCustomerSelectedId=4330&ProductCategoryId=5';

    // Business Information
    readonly registerNoInput: Locator;
    readonly companyNameInput: Locator;
    readonly registrationTypeDropdown: Locator;
    readonly businessTypeDropdown: Locator;
    readonly provinceDropdown: Locator;

    // Contact Information
    readonly customerTitleDropdown: Locator;
    readonly contactPersonNameInput: Locator;
    readonly contactPersonLastNameInput: Locator;
    readonly contactPersonPositionInput: Locator;
    readonly customerEmailInput: Locator;
    readonly contactPersonPhoneInput: Locator;

    // Buttons
    readonly nextButton: Locator;

    constructor(page: Page) {
        this.page = page;

        this.registerNoInput = page.locator('#RegisterNo_Input');
        this.companyNameInput = page.locator('#companyName_Input');
        this.registrationTypeDropdown = page.locator('#Input_RegistrationType');
        this.businessTypeDropdown = page.locator('#BusinessType_Input');
        this.provinceDropdown = page.locator('#Province_Input');

        this.customerTitleDropdown = page.locator('#CustomerTitle_Input');
        this.contactPersonNameInput = page.locator('#contactPerson_Name_Input');
        this.contactPersonLastNameInput = page.locator('#contactPerson_LastName_Input');
        this.contactPersonPositionInput = page.locator('#contactPerson_PositionInput');
        this.customerEmailInput = page.locator('#CustomerEmail_Input');
        this.contactPersonPhoneInput = page.locator('#contactPerson_PhoneNumber_Input');

        this.nextButton = page.locator('.btn.btn-primary.next-btn.dis-btn');
    }

    async goto() {
        await this.page.goto(this.url);
        const acceptBtn = this.page.locator('#accept-recommended-btn-handler');
        if (await acceptBtn.isVisible({ timeout: 3000 }).catch(() => false)) {
            await acceptBtn.click();
        }
    }

    async fillRegisterNo(value: string) {
        await this.registerNoInput.fill(value ?? '');
    }
    async fillCompanyName(value: string) {
        await this.companyNameInput.fill(value ?? '');
    }
    async fillContactName(value: string) {
        await this.contactPersonNameInput.fill(value ?? '');
    }
    async fillContactLastName(value: string) {
        await this.contactPersonLastNameInput.fill(value ?? '');
    }
    async fillPosition(value: string) {
        await this.contactPersonPositionInput.fill(value ?? '');
    }
    async fillEmail(value: string) {
        await this.customerEmailInput.fill(value ?? '');
    }
    async fillPhone(value: string) {
        await this.contactPersonPhoneInput.fill(value ?? '');
    }

    async selectRegistrationType(label: string) {
        await this.registrationTypeDropdown.selectOption({ label });
    }
    async selectBusinessType(label: string) {
        await this.businessTypeDropdown.selectOption({ label });
    }
    async selectProvince(label: string) {
        await this.provinceDropdown.selectOption({ label });
    }
    async selectCustomerTitle(label: string) {
        await this.customerTitleDropdown.selectOption({ label });
    }

    async clickNext() { 
        await this.page.getByRole('button', { name: 'ดำเนินการต่อ' }).click(); 
    }

    async submitAndWait() {
        await this.page.locator('#Consent_Checkbox').check();
        await this.page.getByRole('button', { name: 'ยืนยัน' }).click();
        await this.page.waitForTimeout(1000);
    }

    // 🌟 [ฟังก์ชันตรวจสอบที่อัปเดตใหม่] ตรวจสอบข้อมูลในหน้ายืนยันแบบทีละฟิลด์ดึงจาก CSV
    async checkCompanyNameOnConfirmation(expectedName: string) {
        // เปลี่ยนจาก '#companyNameInput' ข้อความดิบ มาเป็นการเอาตัวแปรที่กรอกไปมาเช็คจริง
        await expect(this.page.getByText(expectedName)).toBeVisible();
    }

    async checkRegisterNoOnConfirmation(expectedNo: string) {
        await expect(this.page.getByText(expectedNo)).toBeVisible();
    }

    // 🚀 [ฟังก์ชันแถมพิเศษ] รวมร่างตรวจสอบข้อมูลทุกช่องรวดเดียวในฟังก์ชันเดียว เพื่อให้โค้ดสะอาด
    async verifyAllConfirmationData(row: { companyName: string; phone: string; email: string }) {
        await expect(this.page.getByText(row.companyName)).toBeVisible();
        await expect(this.page.getByText(row.phone)).toBeVisible(); // เปลี่ยนมาเช็คเบอร์โทรศัพท์ตรงนี้
        await expect(this.page.getByText(row.email)).toBeVisible();
    }
}