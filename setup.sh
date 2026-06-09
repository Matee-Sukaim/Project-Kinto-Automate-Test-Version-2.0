#!/usr/bin/env bash

# 1. สร้างโฟลเดอร์สำหรับแคชเบราว์เซอร์ให้ระบบมองเห็น
mkdir -p ~/.cache/ms-playwright

# 2. สั่งติดตั้ง Playwright Chromium ลงตำแหน่งแกนหลักของระบบ
python -m playwright install chromium --with-deps

# 3. ตรวจสอบสถานะการติดตั้ง (ส่ง Log ไปยังหน้าเซิร์ฟเวอร์)
echo "=== Playwright Browser Installation Completed ==="