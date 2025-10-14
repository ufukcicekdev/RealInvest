# 📅 Newsletter Cron Job Kurulum Kılavuzu

## 🎯 Amaç

Zamanlanmış bültenlerin otomatik olarak belirlenen tarih ve saatte gönderilmesi için cron job kurulumu.

---

## 🔧 Management Command

### Komut Konumu
```
properties/management/commands/send_scheduled_newsletters.py
```

### Manuel Test
```bash
cd /Users/mac/Desktop/emlakcı2
source venv/bin/activate
python manage.py send_scheduled_newsletters
```

### Çıktı Örneği
```
============================================================
Found 1 newsletter(s) to send.
============================================================
Processing: Şubat Ayı Fırsatları
Scheduled for: 2025-02-14 10:00:00
============================================================

SMTP connection established.
  ✓ Sent to: user1@example.com
  ✓ Sent to: user2@example.com
  ✓ Sent to: user3@example.com

✓ Newsletter sent successfully: 3/3 emails sent
============================================================
Scheduled newsletter processing completed.
============================================================
```

---

## 🖥️ Cron Job Kurulumu

### macOS / Linux

#### 1. Crontab Dosyasını Aç
```bash
crontab -e
```

#### 2. Cron Job Ekle

**Her 15 dakikada bir kontrol et:**
```cron
*/15 * * * * cd /Users/mac/Desktop/emlakcı2 && /Users/mac/Desktop/emlakcı2/venv/bin/python manage.py send_scheduled_newsletters >> /Users/mac/Desktop/emlakcı2/logs/newsletter_cron.log 2>&1
```

**Her saat başı kontrol et:**
```cron
0 * * * * cd /Users/mac/Desktop/emlakcı2 && /Users/mac/Desktop/emlakcı2/venv/bin/python manage.py send_scheduled_newsletters >> /Users/mac/Desktop/emlakcı2/logs/newsletter_cron.log 2>&1
```

**Her gün saat 09:00'da kontrol et:**
```cron
0 9 * * * cd /Users/mac/Desktop/emlakcı2 && /Users/mac/Desktop/emlakcı2/venv/bin/python manage.py send_scheduled_newsletters >> /Users/mac/Desktop/emlakcı2/logs/newsletter_cron.log 2>&1
```

**Her Pazartesi saat 10:00'da kontrol et:**
```cron
0 10 * * 1 cd /Users/mac/Desktop/emlakcı2 && /Users/mac/Desktop/emlakcı2/venv/bin/python manage.py send_scheduled_newsletters >> /Users/mac/Desktop/emlakcı2/logs/newsletter_cron.log 2>&1
```

#### 3. Cron Job Formatı Açıklaması
```
* * * * * command
│ │ │ │ │
│ │ │ │ └─── Haftanın günü (0-6, Pazar=0)
│ │ │ └───── Ay (1-12)
│ │ └─────── Ayın günü (1-31)
│ └───────── Saat (0-23)
└─────────── Dakika (0-59)
```

#### 4. Log Klasörü Oluştur
```bash
mkdir -p /Users/mac/Desktop/emlakcı2/logs
```

#### 5. Crontab'ı Kaydet ve Çık
```
:wq  (vi/vim için)
veya
Ctrl+X, sonra Y, sonra Enter (nano için)
```

#### 6. Aktif Cron Job'ları Görüntüle
```bash
crontab -l
```

#### 7. Cron Job'u Sil
```bash
crontab -r
```

---

### 🪟 Windows

#### Yöntem 1: Task Scheduler

1. **Task Scheduler'ı Aç**
   - Windows tuşu + R
   - `taskschd.msc` yazın
   - Enter

2. **Yeni Görev Oluştur**
   - Actions > Create Basic Task
   - Name: "Newsletter Cron"
   - Description: "Send scheduled newsletters"

3. **Trigger (Tetikleyici) Ayarla**
   - Daily / Weekly / Monthly seçin
   - Saat: 09:00 (örnek)

4. **Action (Eylem) Ayarla**
   - Action: Start a program
   - Program/script:
     ```
     C:\Users\YourUser\Desktop\emlakcı2\venv\Scripts\python.exe
     ```
   - Add arguments:
     ```
     manage.py send_scheduled_newsletters
     ```
   - Start in:
     ```
     C:\Users\YourUser\Desktop\emlakcı2
     ```

5. **Finish**

#### Yöntem 2: Batch Script ile

1. **Batch dosyası oluştur: `run_newsletter.bat`**
```batch
@echo off
cd C:\Users\YourUser\Desktop\emlakcı2
call venv\Scripts\activate.bat
python manage.py send_scheduled_newsletters >> logs\newsletter_cron.log 2>&1
```

2. **Task Scheduler ile batch'i çalıştır**
   - Program/script: `C:\Users\YourUser\Desktop\emlakcı2\run_newsletter.bat`

---

## ☁️ Production Sunucu (Ubuntu/Debian)

### Sistem Kullanıcısı Olarak Cron

```bash
# Crontab'ı düzenle
sudo crontab -e -u www-data

# Cron job ekle (her 30 dakikada bir)
*/30 * * * * cd /var/www/emlak && /var/www/emlak/venv/bin/python manage.py send_scheduled_newsletters >> /var/www/emlak/logs/newsletter_cron.log 2>&1
```

### Systemd Timer (Alternatif)

#### 1. Service Dosyası: `/etc/systemd/system/newsletter.service`
```ini
[Unit]
Description=Send Scheduled Newsletters
After=network.target

[Service]
Type=oneshot
User=www-data
WorkingDirectory=/var/www/emlak
ExecStart=/var/www/emlak/venv/bin/python manage.py send_scheduled_newsletters
StandardOutput=append:/var/www/emlak/logs/newsletter.log
StandardError=append:/var/www/emlak/logs/newsletter_error.log
```

#### 2. Timer Dosyası: `/etc/systemd/system/newsletter.timer`
```ini
[Unit]
Description=Newsletter Timer
Requires=newsletter.service

[Timer]
OnCalendar=*:0/30
Persistent=true

[Install]
WantedBy=timers.target
```

#### 3. Aktifleştir
```bash
sudo systemctl daemon-reload
sudo systemctl enable newsletter.timer
sudo systemctl start newsletter.timer
sudo systemctl status newsletter.timer
```

---

## 📝 .env Ayarları

Cron job'un çalışması için `.env` dosyasına ekleyin:

```env
# Site Domain (Newsletter unsubscribe links için)
SITE_PROTOCOL=https
SITE_DOMAIN=www.realinvestgayrimenkul.com

# Veya development için:
# SITE_PROTOCOL=http
# SITE_DOMAIN=localhost:8000
```

---

## 🧪 Test Senaryosu

### 1. Test Bülteni Oluştur
```
Admin Panel > Bültenler > Bülten Ekle

Başlık: Test Zamanlanmış Bülten
Konu: Test Email
İçerik: Bu bir test mailidir.
Durum: Zamanlanmış
Gönderim Zamanı: [2 dakika sonra]
```

### 2. Manuel Çalıştır (Test)
```bash
cd /Users/mac/Desktop/emlakcı2
source venv/bin/activate
python manage.py send_scheduled_newsletters
```

### 3. Beklenen Çıktı
```
Found 1 newsletter(s) to send.
Processing: Test Zamanlanmış Bülten
...
✓ Newsletter sent successfully: X/X emails sent
```

### 4. Kontrol Et
- Admin panelde bülten status'ü "Gönderildi" olmalı
- Gönderim tarihi güncellenmeli
- İstatistikler dolu olmalı

---

## 📊 Log Kontrolü

### Log Dosyasını İzle (Real-time)
```bash
tail -f /Users/mac/Desktop/emlakcı2/logs/newsletter_cron.log
```

### Son 50 Satırı Görüntüle
```bash
tail -n 50 /Users/mac/Desktop/emlakcı2/logs/newsletter_cron.log
```

### Log Temizle
```bash
> /Users/mac/Desktop/emlakcı2/logs/newsletter_cron.log
```

---

## ⚠️ Sorun Giderme

### Cron Çalışmıyor

#### 1. Cron Servisini Kontrol Et
```bash
# macOS
sudo launchctl list | grep cron

# Linux
sudo systemctl status cron
```

#### 2. Yol Kontrolü
```bash
which python  # Python yolunu kontrol et
echo $PATH    # PATH değişkenini kontrol et
```

#### 3. Manuel Test
```bash
cd /Users/mac/Desktop/emlakcı2
source venv/bin/activate
python manage.py send_scheduled_newsletters
```

### Log'da Hata Var

#### "SMTP settings not configured"
```
Çözüm:
Admin Panel > Site Ayarları > Email SMTP Ayarları
- Tüm alanları doldurun
```

#### "Site settings not found"
```
Çözüm:
Admin Panel > Site Ayarları
- En az bir SiteSettings objesi oluşturun
```

#### "No active subscribers"
```
Çözüm:
Admin Panel > Bülten Aboneleri
- En az bir aktif abone olmalı
```

### Cron Log'u Boş

#### Cron çalışıyor mu kontrol et:
```bash
# macOS/Linux
ps aux | grep cron

# Cron job listesi
crontab -l
```

#### Cron output'u kontrol et:
```bash
# Sistem log'ları
tail -f /var/log/syslog    # Ubuntu/Debian
tail -f /var/log/cron      # CentOS/RHEL
```

---

## 🚀 Önerilen Cron Ayarları

### Küçük Site (< 100 abone)
```cron
# Her 15 dakikada bir kontrol
*/15 * * * * [command]
```

### Orta Boy Site (100-1000 abone)
```cron
# Her 30 dakikada bir kontrol
*/30 * * * * [command]
```

### Büyük Site (> 1000 abone)
```cron
# Her saat başı kontrol
0 * * * * [command]
```

---

## 📈 Performans İpuçları

### 1. Toplu Gönderim
- Çok fazla abone varsa, batch sending kullanın
- Her 100 abonede bir progress log'u

### 2. Rate Limiting
- SMTP sağlayıcınızın limitlerine dikkat edin
- Gmail: ~500 email/gün (free)
- Gmail Workspace: ~2000 email/gün
- SendGrid: 100 email/gün (free)

### 3. Retry Mekanizması
- Başarısız mailleri tekrar gönderme mantığı
- Exponential backoff

---

## 📞 Destek

Cron job ile ilgili sorularınız için:
- Log dosyalarını kontrol edin
- Manuel test yapın
- SMTP ayarlarını doğrulayın

**Son Güncelleme:** 2025-02-14
