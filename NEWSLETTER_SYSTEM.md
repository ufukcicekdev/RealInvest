# 📧 Newsletter (Bülten) Sistemi - Kullanım Kılavuzu

## 🎯 Özellikler

### ✅ Tamamlanan Özellikler:

1. **✨ Profesyonel Email Template**
   - Site Settings'den logo, adres, telefon, email otomatik çekilir
   - Sosyal medya bağlantıları (Facebook, Instagram, Twitter, LinkedIn, YouTube)
   - Responsive tasarım (mobil uyumlu)
   - Unsubscribe (abonelikten çıkma) linki
   - Gradient header ve footer
   - Modern ve şık tasarım

2. **🤖 Otomatik Zamanlama (APScheduler)**
   - Her dakika otomatik kontrol
   - Zamanı gelen bültenler otomatik gönderilir
   - Background task olarak çalışır
   - Sunucu çalıştığı sürece aktif

3. **📊 Detaylı Logging (Database)**
   - Her işlem database'e kaydedilir
   - Admin panelden görüntüleme
   - Hata detayları ile birlikte
   - Filtreleme ve arama

4. **🎨 Popup Newsletter Formu**
   - İlk ziyarette otomatik açılır
   - "Bir daha gösterme" seçeneği
   - Cookie ile 365 gün hatırlanır
   - Admin panelden yönetilebilir

5. **📈 İstatistikler**
   - Toplam alıcı sayısı
   - Gönderilen email sayısı
   - Başarısız email sayısı
   - Gönderim tarihi

---

## 🚀 Kullanım

### 1. Newsletter Oluşturma

**Admin Panel → Bültenler → Yeni Bülten Ekle**

1. **Başlık**: Bülten başlığı (admin için)
2. **E-posta Konusu**: Email'in subject'i
3. **İçerik**: HTML içerik kullanabilirsiniz
4. **Durum**: 
   - **Taslak**: Henüz gönderilmeyecek
   - **Zamanlanmış**: Belirlenen tarihte otomatik gönderilir
5. **Gönderim Zamanı**: Boş bırakılırsa "Bülteni Gönder" butonuyla manuel gönderilir

**Örnek:**
```
Başlık: Şubat 2025 Bülteni
E-posta Konusu: Bu Ay'ın En İyi Emlak Fırsatları! 🏠
İçerik: 
  <h3>Merhaba!</h3>
  <p>Bu ay sizin için özel fırsatlar hazırladık...</p>
  <ul>
    <li>Villa - 2.500.000 TL</li>
    <li>Daire - 1.200.000 TL</li>
  </ul>

Durum: Zamanlanmış
Gönderim Zamanı: 15 Şubat 2025 10:00
```

### 2. Manuel Gönderim

1. Admin Panel → Bültenler
2. Göndermek istediğiniz bülteni seçin
3. Eylemler → **"Seçili bültenleri gönder"**
4. Git'e tıklayın

### 3. Zamanlanmış Gönderim

1. Bülten oluştururken **Durum: Zamanlanmış** seçin
2. **Gönderim Zamanı** belirleyin
3. Kaydet
4. APScheduler her dakika kontrol eder
5. Zaman geldiğinde otomatik gönderilir

**⚠️ Önemli**: Sunucu çalışmıyor ise zamanlanmış bültenler gönderilemez!

---

## 📝 Email Template Özellikleri

### Otomatik Çekilen Bilgiler (SiteSettings'den):

1. **Logo**: Header ve footer'da görünür
2. **Site Adı**: Email başlığında
3. **Adres**: Footer'da 📍 ile
4. **Telefon**: Footer'da 📞 ile (tıklanabilir link)
5. **Email**: Footer'da 📧 ile (tıklanabilir link)
6. **Sosyal Medya**: Footer'da butonlar olarak
   - Facebook (f)
   - Instagram (📷)
   - Twitter (🐦)
   - LinkedIn (in)
   - YouTube (▶)

### Template Yapısı:

```
┌─────────────────────────────┐
│    [LOGO]                   │
│    Site Adı                 │  ← Header (Gradient)
└─────────────────────────────┘
┌─────────────────────────────┐
│  Bülten Başlığı            │
│                             │
│  Bülten İçeriği            │  ← İçerik
│  (HTML destekli)           │
│                             │
│  [Web Sitesini Ziyaret Et] │  ← CTA Button
└─────────────────────────────┘
┌─────────────────────────────┐
│    [LOGO]                   │
│                             │
│  📍 Adres                  │
│  📞 Telefon                │
│  📧 Email                  │  ← Footer (Dark)
│                             │
│  [f] [📷] [🐦] [in] [▶]   │  ← Sosyal Medya
│                             │
│  Abonelikten çık linki     │
│  © 2025 Site Adı           │
└─────────────────────────────┘
```

---

## 🔧 Teknik Detaylar

### APScheduler Kurulumu:

```python
# properties/scheduler.py
- BackgroundScheduler kullanır
- Her 1 dakikada bir çalışır
- Zamanı gelen bültenleri otomatik gönderir

# properties/apps.py
- Django başlarken scheduler otomatik başlar
- ready() metodunda initialize edilir
```

### Email Template:

```
templates/emails/newsletter.html
- Django template engine kullanır
- Context: newsletter, site_settings, subscriber, unsubscribe_url, current_year
- Responsive CSS (mobile-friendly)
- Inline styles (email uyumluluğu için)
```

### Logging:

```python
NewsletterLog modeli:
- info: Bilgilendirme (başlatıldı, vb.)
- success: Başarılı gönderimler
- warning: Kısmi başarı
- error: Hatalar
```

---

## 📊 Admin Panel

### Bültenler Listesi:
- Başlık
- Durum (badge ile renkli)
- Gönderim zamanı
- İstatistikler
- Logları görüntüleme (inline)

### Abone Listesi:
- Email
- İsim
- Durum (Aktif/Pasif)
- Abonelik tarihi
- Toplu aktifleştirme/pasifleştirme

### Bülten Logları:
- Tarih/saat
- Bülten
- Log tipi (renkli badge)
- Mesaj
- Abone email
- Hata detayları

---

## 🎨 Popup Ayarları

**Admin Panel → Newsletter Popup Ayarları**

- **Popup Aktif**: Açık/Kapalı
- **Başlık**: Popup başlığı
- **Açıklama**: Alt metin
- **Gecikme**: Kaç saniye sonra açılsın (varsayılan: 3)
- **Mobilde Göster**: Mobil cihazlarda göster
- **Buton Metni**: "Abone Ol" gibi
- **Buton Rengi**: Hex kod (#007bff)

---

## 🔒 Güvenlik

1. **Unsubscribe Token**: Her abone için benzersiz 32 karakter token
2. **SMTP Şifreleme**: TLS desteği
3. **CSRF Koruması**: Form gönderimlerinde
4. **XSS Koruması**: HTML içerik filtreleme

---

## 📱 Production Deployment

### Gunicorn ile:
```bash
gunicorn realestate_project.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

### Systemd ile (otomatik başlatma):
```bash
# /etc/systemd/system/newsletter.service dosyası oluşturun
sudo systemctl enable newsletter
sudo systemctl start newsletter
```

### Docker ile:
```bash
docker-compose up -d
```

**Önemli**: APScheduler otomatik başlar, ek konfigürasyon gerekmez!

---

## 🐛 Sorun Giderme

### Bülten gönderilmiyor:
1. SMTP ayarlarını kontrol edin (Site Ayarları)
2. Sunucunun çalıştığından emin olun
3. Logları kontrol edin (Bülten Logları)
4. Firewall SMTP port'unu (587/465) engelliyor olabilir

### Popup çıkmıyor:
1. Popup Ayarları'nda "Popup Aktif" açık mı?
2. Cookie silinmiş olabilir (developer tools'dan kontrol)
3. Browser cache'i temizleyin

### Scheduled newsletter geç gönderiliyor:
1. APScheduler her 1 dakikada kontrol eder
2. Maksimum 1 dakika gecikme normal
3. Sunucu saati doğru mu? (timezone kontrol)

---

## 📞 Destek

Sorularınız için:
- Email: support@example.com
- Telefon: +90 XXX XXX XX XX

---

**Son Güncelleme**: 14 Ekim 2025
**Versiyon**: 2.0 (APScheduler + Professional Email Template)
