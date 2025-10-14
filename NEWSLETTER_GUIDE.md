# 📧 Newsletter (Bülten) Sistemi Kullanım Kılavuzu

## 🎯 Özellikler

✅ **Popup Newsletter Formu** - İlk ziyarette otomatik açılır
✅ **"Bir daha gösterme" özelliği** - Cookie ile hatırlanır  
✅ **Admin panelden popup kontrolü** - Açma/kapama
✅ **Abone yönetimi** - Tüm aboneleri görüntüleme ve yönetme
✅ **Bülten gönderimi** - Zamanlanmış veya anında gönderim
✅ **Unsubscribe (Abonelikten çıkma)** - Her mailde link
✅ **Duplicate kontrol** - Aynı mail varsa sadece aktifleştir
✅ **İstatistikler** - Gönderim raporları ve başarı oranları

---

## 🚀 Hızlı Başlangıç

### 1. Admin Paneline Giriş

```
http://yourdomain.com/admin/
```

### 2. Newsletter Popup Ayarları

**Menü:** `Newsletter Popup Ayarları`

#### Popup Ayarları
```
✅ Popup Aktif: Popup'ın gösterilip gösterilmeyeceği
📝 Popup Başlığı: "Bültenimize Abone Olun!"
📝 Popup Açıklaması: "En son emlak fırsatları..."
```

#### Görüntüleme Ayarları
```
⏱️ Gecikme (saniye): 3 (Popup kaç saniye sonra açılsın)
📱 Mobilde Göster: ✓ (Mobil cihazlarda da göster)
```

#### Stil Ayarları
```
🎨 Buton Metni: "Abone Ol"
🎨 Buton Rengi: #007bff (Hex renk kodu)
```

---

## 👥 Abone Yönetimi

### Abone Listesi Görüntüleme

**Menü:** `Bülten Aboneleri`

Liste görünümünde:
- ✉️ E-posta adresi
- 👤 Ad Soyad
- ✅ Aktif/Pasif durumu
- 📅 Abone olma tarihi
- 🟢 Durum badge'i

### Abone Filtreleme

```
Filtreleme seçenekleri:
- Aktif/Pasif durumu
- Abone olma tarihi
```

### Toplu İşlemler

**Seçili aboneleri aktifleştir:**
1. Aboneleri seçin
2. Üstteki "Action" menüsünden "Seçili aboneleri aktifleştir"
3. "Go" butonuna tıklayın

**Seçili aboneleri pasifleştir:**
1. Aboneleri seçin
2. "Action" menüsünden "Seçili aboneleri pasifleştir"
3. "Go" butonuna tıklayın

---

## 📨 Bülten Oluşturma ve Gönderme

### Yeni Bülten Oluşturma

**Menü:** `Bültenler` → `Bülten Ekle`

#### 1. Bülten Bilgileri
```
📌 Başlık: "Şubat Ayı Emlak Fırsatları"
├─ İç kullanım için, müşteri görmez
└─ Örnek: "2025 Şubat - Yeni İlanlar"

📧 E-posta Konusu: "Bu Ay Kaçırılmayacak Fırsatlar!"
├─ Müşterinin inbox'unda görünen
└─ İlgi çekici ve net olmalı

📝 İçerik: (HTML kullanabilirsiniz)
├─ Bülten mesajınızı buraya yazın
├─ HTML etiketleri kullanılabilir
└─ Örnek aşağıda
```

#### 2. Zamanlama
```
📊 Durum: "Taslak"
├─ Taslak: Henüz gönderilmedi
├─ Zamanlanmış: Belirli tarihe ayarlandı
├─ Gönderiliyor: Şu an gönderiliyor
├─ Gönderildi: Başarıyla tamamlandı
└─ Başarısız: Hata oluştu

📅 Gönderim Zamanı: (Opsiyonel)
├─ Boş bırakılırsa → Hemen gönderilir
├─ Tarih seçilirse → O tarihte gönderilir
└─ Format: 2025-02-15 10:00
```

### Örnek Bülten İçeriği

```html
<h2>Merhaba!</h2>

<p>Bu ay sizin için özel olarak seçtiğimiz emlak fırsatlarını paylaşmak istiyoruz:</p>

<h3>🏠 Yeni İlanlar</h3>
<ul>
    <li><strong>Kadıköy'de 3+1 Daire</strong> - ₺2.500.000</li>
    <li><strong>Beşiktaş'ta Lüks Villa</strong> - ₺8.900.000</li>
    <li><strong>Şişli'de Ofis</strong> - Kiralık - ₺25.000/ay</li>
</ul>

<h3>📢 Özel Kampanya</h3>
<p>Şubat ayı boyunca tüm yeni inşaat projelerimizde <strong>%10 indirim</strong>!</p>

<p>Detaylı bilgi için <a href="https://yoursite.com">web sitemizi</a> ziyaret edebilirsiniz.</p>

<p>Saygılarımızla,<br>
Emlak Ekibimiz</p>
```

### Bülten Gönderme

#### Yöntem 1: Hemen Gönder
1. Bülteni oluşturun
2. "Gönderim Zamanı" alanını **boş bırakın**
3. Kaydedin
4. Liste görünümünden bülteni seçin
5. Actions → "Seçili bültenleri gönder" → Go

#### Yöntem 2: Zamanlanmış Gönderim
1. Bülteni oluşturun
2. "Gönderim Zamanı" alanına **gelecek bir tarih** girin
3. Durum: "Zamanlanmış" seçin
4. Kaydedin
5. **Otomatik gönderim için cron job kurulumu gerekir** (aşağıda açıklandı)

---

## 📊 İstatistikler ve Raporlama

Bülten detay sayfasında şu bilgileri görebilirsiniz:

```
📈 İstatistikler:
├─ Toplam Alıcı: 150
├─ Gönderilen: 148
├─ Başarısız: 2
└─ Başarı Oranı: %98.67

📅 Tarihler:
├─ Oluşturma Tarihi: 2025-02-01 10:30
├─ Gönderilme Tarihi: 2025-02-01 11:15
└─ Güncelleme Tarihi: 2025-02-01 11:20
```

---

## 🔔 Otomatik Zamanlanmış Gönderim (Cron Job)

Zamanlanmış bültenlerin otomatik gönderilmesi için:

### Linux/Mac Cron Job

```bash
# Crontab dosyasını düzenle
crontab -e

# Her saat başı kontrol et
0 * * * * cd /path/to/emlakcı2 && /path/to/venv/bin/python manage.py send_scheduled_newsletters

# Veya her 15 dakikada bir
*/15 * * * * cd /path/to/emlakcı2 && /path/to/venv/bin/python manage.py send_scheduled_newsletters
```

### Management Command Oluşturma

`properties/management/commands/send_scheduled_newsletters.py` dosyası:

```python
from django.core.management.base import BaseCommand
from django.utils import timezone
from properties.models import Newsletter, NewsletterSubscriber
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

class Command(BaseCommand):
    help = 'Send scheduled newsletters'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        
        # Get scheduled newsletters that are ready to send
        newsletters = Newsletter.objects.filter(
            status='scheduled',
            scheduled_date__lte=now
        )
        
        for newsletter in newsletters:
            # Send logic here (copy from admin.py send_newsletter)
            self.stdout.write(f'Sending newsletter: {newsletter.title}')
```

---

## 🚫 Abonelikten Çıkma (Unsubscribe)

### Kullanıcı Perspektifi

1. Kullanıcı bülten mailini açar
2. Mail sonundaki "Buraya tıklayarak aboneliğinizden çıkabilirsiniz" linkine tıklar
3. Onay sayfası açılır
4. "Evet, Abonelikten Çık" butonuna tıklar
5. Abonelik pasif hale gelir

### Unsubscribe Link Formatı

```
https://yoursite.com/newsletter/unsubscribe/ABC123TOKEN/
```

**Güvenlik:**
- Her abone için benzersiz token
- Tahmin edilemez (32 karakter)
- Veritabanında saklanır

### Admin Tarafından Yönetim

Abonelikten çıkan kullanıcılar:
- `is_active` = False
- `unsubscribed_date` = İptal tarihi
- Listede "Pasif" olarak görünür
- Yeniden aktifleştirilebilir

---

## 🎨 Popup Kullanıcı Deneyimi

### Popup Açılma Senaryosu

```
1. Kullanıcı siteye girer
   ↓
2. 3 saniye bekler (ayarlanabilir)
   ↓
3. Popup açılır
   ↓
4. Kullanıcı seçenekleri görür:
   - Ad Soyad
   - E-posta
   - ☐ Bir daha gösterme
   - [Abone Ol] butonu
```

### "Bir Daha Gösterme" Özelliği

```
Checkbox işaretlenirse:
├─ Cookie oluşturulur
├─ Süre: 365 gün
├─ Ad: newsletter_dismissed
└─ Değer: true

Sonraki ziyaretlerde:
├─ Cookie kontrol edilir
├─ Varsa popup gösterilmez
└─ Yoksa popup açılır
```

### Mobil Uyumluluk

```
Admin panelden kontrol:
└─ "Mobilde Göster" = ✓
   ├─ Tüm cihazlarda açılır
   └─ Mobil optimize edilmiş

└─ "Mobilde Göster" = ✗
   ├─ Sadece desktop'ta açılır
   └─ Mobil kullanıcılar görmez
```

---

## 💡 En İyi Uygulamalar

### Bülten İçeriği

#### ✅ YAPIN:
- Kısa ve öz tutun (max 500 kelime)
- Başlıklar kullanın (H2, H3)
- Bullet point'ler ekleyin
- Call-to-action (CTA) ekleyin
- Görseller kullanın (ama fazla değil)
- Mobil uyumlu yazın

#### ❌ YAPMAYIN:
- Çok uzun metinler
- Sadece metin (görsel yok)
- Spam kelimeler (ÜCRETSİZ!!!, TIKLA!!!)
- Çok fazla link
- Küçük font boyutu

### E-posta Konusu

```
✅ İyi Örnekler:
- "Şubat Ayı Özel Fırsatları 🏠"
- "Yeni İnşaat Projemiz Açıldı!"
- "Kadıköy'de Satılık 3+1 Daireler"

❌ Kötü Örnekler:
- "ÜCRETSİZ KONUT!!!"
- "HEMEN TIKLA"
- "Newsletter #47"
```

### Gönderim Zamanı

```
📅 En İyi Günler:
- Salı: ⭐⭐⭐⭐⭐
- Çarşamba: ⭐⭐⭐⭐⭐
- Perşembe: ⭐⭐⭐⭐

⏰ En İyi Saatler:
- 10:00-11:00: ⭐⭐⭐⭐⭐
- 14:00-15:00: ⭐⭐⭐⭐
- 20:00-21:00: ⭐⭐⭐

❌ Kaçınılması Gereken:
- Pazartesi sabahı (inbox dolu)
- Cuma akşamı (hafta sonu)
- Gece yarısı
```

### Gönderim Sıklığı

```
📧 Önerilen Sıklık:
├─ Haftada 1 kez: İdeal
├─ Ayda 2 kez: Kabul edilebilir
├─ Ayda 4+ kez: Çok fazla (spam riski)
└─ Özel durumlar: Kampanyalar için ekstra

🚫 Dikkat:
- Çok sık mail → Unsubscribe artar
- Çok seyrek mail → Unutulursunuz
```

---

## 🔧 Teknik Bilgiler

### Veritabanı Modelleri

#### NewsletterSubscriber
```python
- email: Unique, EmailField
- name: CharField
- is_active: Boolean (aktif/pasif)
- subscribed_date: Otomatik
- unsubscribed_date: İptal tarihi
- ip_address: Kayıt IP'si
- unsubscribe_token: Güvenlik tokeni
```

#### Newsletter
```python
- title: Başlık
- subject: E-posta konusu
- content: İçerik (HTML destekli)
- status: draft/scheduled/sending/sent/failed
- scheduled_date: Zamanlama
- sent_date: Gönderim tarihi
- total_recipients: Toplam alıcı
- sent_count: Gönderilen
- failed_count: Başarısız
```

#### PopupSettings (Singleton)
```python
- enabled: Popup aktif mi?
- title: Popup başlığı
- description: Açıklama
- delay_seconds: Gecikme süresi
- show_on_mobile: Mobilde göster
- button_text: Buton metni
- button_color: Buton rengi
```

### API Endpoints

```
POST /newsletter/subscribe/
├─ Form verisi: name, email, dont_show_again
├─ Response: JSON {success, message}
└─ Cookie: newsletter_dismissed (eğer işaretliyse)

GET /newsletter/unsubscribe/<token>/
├─ Token validation
├─ Onay sayfası göster
└─ POST ile işlem tamamla
```

---

## 📋 Kontrol Listesi

### İlk Kurulum
- [x] Migration çalıştırıldı
- [x] Popup settings oluşturuldu
- [x] Admin panelde görünüyor
- [ ] SMTP ayarları yapılandırıldı
- [ ] Test bülteni gönderildi
- [ ] Unsubscribe linki test edildi

### Düzenli Kontroller
- [ ] Abone sayısı kontrol et
- [ ] Pasif aboneleri incele
- [ ] Gönderim istatistiklerini gözden geçir
- [ ] Başarısız gönderimleri kontrol et
- [ ] SMTP ayarlarının çalıştığını doğrula

---

## 🐛 Sorun Giderme

### Popup Gösterilmiyor

```
Kontrol listesi:
1. Admin panelde "Popup Aktif" ✓ mi?
2. Cookie silindi mi? (newsletter_dismissed)
3. Tarayıcı geliştirici araçları → Console'da hata var mı?
4. JavaScript çalışıyor mu?
5. Bootstrap 5 yüklü mü?
```

### E-posta Gönderilmiyor

```
Kontrol listesi:
1. SMTP ayarları doğru mu? (Site Ayarları)
2. SMTP kullanıcı adı/şifre doğru mu?
3. Gmail kullanıyorsanız → App Password kullanıyor musunuz?
4. Port numarası doğru mu? (587 veya 465)
5. Sunucu loglarını kontrol edin
```

### Unsubscribe Linki Çalışmıyor

```
Kontrol listesi:
1. Token veritabanında var mı?
2. URL doğru formatlanmış mı?
3. Django URL routing yapılandırıldı mı?
4. CSRF token sorunu var mı?
```

---

## 📚 İleri Düzey Özelleştirme

### Custom Email Template

`templates/newsletter/email_template.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; }
        .header { background: #007bff; color: white; padding: 20px; }
        .content { padding: 30px; }
        .footer { background: #f8f9fa; padding: 20px; font-size: 12px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>{{ newsletter.subject }}</h1>
    </div>
    <div class="content">
        {{ newsletter.content|safe }}
    </div>
    <div class="footer">
        <p>Bu e-postayı almak istemiyorsanız, 
        <a href="{{ unsubscribe_url }}">buraya tıklayın</a>.</p>
    </div>
</body>
</html>
```

### Segmentasyon (İleri Seviye)

Gelecekte eklenebilecek özellikler:
- Konum bazlı segmentasyon
- İlgi alanlarına göre gruplandırma
- A/B testing
- Click tracking
- Open rate tracking

---

## 📞 Destek

Sorularınız için:
- Admin panelindeki yardım ikonlarına tıklayın
- Bu dokümantasyonu okuyun
- Teknik destek: [destek@yoursite.com]

**Son Güncelleme:** 2025-10-14
