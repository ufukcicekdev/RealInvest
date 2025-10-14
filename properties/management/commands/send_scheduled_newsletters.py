from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives, get_connection
from django.urls import reverse
from properties.models import Newsletter, NewsletterSubscriber, SiteSettings, NewsletterLog


class Command(BaseCommand):
    help = 'Send scheduled newsletters that are ready to be sent'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        
        # Get newsletters that are scheduled and ready to send
        newsletters = Newsletter.objects.filter(
            status='scheduled',
            scheduled_date__lte=now
        )
        
        if not newsletters.exists():
            self.stdout.write(self.style.SUCCESS('No scheduled newsletters ready to send.'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'Found {newsletters.count()} newsletter(s) to send.'))
        
        for newsletter in newsletters:
            self.stdout.write(f'\n{"="*60}')
            self.stdout.write(f'Processing: {newsletter.title}')
            self.stdout.write(f'Scheduled for: {newsletter.scheduled_date}')
            self.stdout.write(f'{"="*60}\n')
            
            # Log newsletter processing start
            NewsletterLog.log_info(
                newsletter, 
                f'Zamanlanmış bülten işleniyor (Cron Job): {newsletter.title}'
            )
            
            # Get active subscribers
            subscribers = NewsletterSubscriber.objects.filter(is_active=True)
            newsletter.total_recipients = subscribers.count()
            
            if newsletter.total_recipients == 0:
                self.stdout.write(self.style.WARNING('No active subscribers found. Skipping...'))
                NewsletterLog.log_warning(
                    newsletter,
                    'Aktif abone bulunamadı. Bülten gönderimi atlandı.'
                )
                newsletter.status = 'failed'
                newsletter.save()
                continue
            
            # Update status to sending
            newsletter.status = 'sending'
            newsletter.save()
            
            sent_count = 0
            failed_count = 0
            
            # Get SMTP settings from SiteSettings
            site_settings = SiteSettings.objects.first()
            
            if not site_settings:
                self.stdout.write(self.style.ERROR('Site settings not found!'))
                NewsletterLog.log_error(
                    newsletter,
                    'Site ayarları bulunamadı. SMTP konfigürasyonu yüklenemedi.',
                    error_details='SiteSettings.objects.first() returned None'
                )
                newsletter.status = 'failed'
                newsletter.save()
                continue
            
            # Check if SMTP settings are configured
            if not site_settings.smtp_host or not site_settings.smtp_username:
                self.stdout.write(self.style.ERROR('SMTP settings not configured!'))
                NewsletterLog.log_error(
                    newsletter,
                    'SMTP ayarları yapılandırılmamış. Site ayarlarından SMTP bilgilerini kontrol edin.',
                    error_details=f'smtp_host: {site_settings.smtp_host}, smtp_username: {site_settings.smtp_username}'
                )
                newsletter.status = 'failed'
                newsletter.save()
                continue
            
            # Create custom email connection with SiteSettings SMTP config
            try:
                connection = get_connection(
                    backend='django.core.mail.backends.smtp.EmailBackend',
                    host=site_settings.smtp_host,
                    port=site_settings.smtp_port,
                    username=site_settings.smtp_username,
                    password=site_settings.smtp_password,
                    use_tls=site_settings.smtp_use_tls,
                    fail_silently=False,
                )
                self.stdout.write(self.style.SUCCESS('SMTP connection established.'))
                NewsletterLog.log_success(
                    newsletter,
                    f'SMTP bağlantısı kuruldu: {site_settings.smtp_host}:{site_settings.smtp_port}'
                )
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'SMTP connection failed: {str(e)}'))
                NewsletterLog.log_error(
                    newsletter,
                    f'SMTP bağlantısı başarısız: {site_settings.smtp_host}:{site_settings.smtp_port}',
                    error_details=str(e)
                )
                newsletter.status = 'failed'
                newsletter.save()
                continue
            
            # Send to each subscriber
            for subscriber in subscribers:
                try:
                    # Generate unsubscribe URL (we need request object for full URL)
                    # For cron jobs, we'll use site domain from settings
                    from django.conf import settings
                    site_domain = getattr(settings, 'SITE_DOMAIN', 'localhost:8000')
                    site_protocol = getattr(settings, 'SITE_PROTOCOL', 'http')
                    
                    unsubscribe_path = reverse('newsletter_unsubscribe', args=[subscriber.unsubscribe_token])
                    unsubscribe_url = f"{site_protocol}://{site_domain}{unsubscribe_path}"
                    
                    # Prepare HTML content
                    html_content = f"""
                    <html>
                    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                            <h2>{newsletter.subject}</h2>
                            <div>{newsletter.content}</div>
                            <hr style="margin: 30px 0; border: none; border-top: 1px solid #ddd;">
                            <p style="font-size: 12px; color: #666;">
                                Bu e-postayı almak istemiyorsanız, 
                                <a href="{unsubscribe_url}" style="color: #007bff;">buraya tıklayarak</a> 
                                aboneliğinizden çıkabilirsiniz.
                            </p>
                        </div>
                    </body>
                    </html>
                    """
                    
                    # Send email using custom SMTP connection
                    email = EmailMultiAlternatives(
                        subject=newsletter.subject,
                        body=newsletter.content,  # Plain text version
                        from_email=site_settings.email_from if site_settings.email_from else site_settings.email,
                        to=[subscriber.email],
                        connection=connection
                    )
                    email.attach_alternative(html_content, "text/html")
                    email.send()
                    
                    sent_count += 1
                    self.stdout.write(f'  ✓ Sent to: {subscriber.email}')
                    NewsletterLog.log_success(
                        newsletter,
                        'Email başarıyla gönderildi',
                        subscriber_email=subscriber.email
                    )
                    
                except Exception as e:
                    failed_count += 1
                    error_msg = f'Email gönderimi başarısız: {subscriber.email}'
                    self.stdout.write(self.style.ERROR(f'  ✗ Failed to send to {subscriber.email}: {str(e)}'))
                    NewsletterLog.log_error(
                        newsletter,
                        error_msg,
                        subscriber_email=subscriber.email,
                        error_details=str(e)
                    )
            
            # Close connection
            try:
                connection.close()
            except:
                pass
            
            # Update newsletter stats and status
            newsletter.sent_count = sent_count
            newsletter.failed_count = failed_count
            newsletter.sent_date = timezone.now()
            
            # Determine final status
            if sent_count == 0:
                newsletter.status = 'failed'
                self.stdout.write(self.style.ERROR(f'\n✗ Newsletter failed: No emails sent ({failed_count} failed)'))
                NewsletterLog.log_error(
                    newsletter,
                    f'Bülten gönderimi başarısız: Hiçbir email gönderilemedi ({failed_count} başarısız)'
                )
            elif failed_count == 0:
                newsletter.status = 'sent'
                self.stdout.write(self.style.SUCCESS(f'\n✓ Newsletter sent successfully: {sent_count}/{newsletter.total_recipients} emails sent'))
                NewsletterLog.log_success(
                    newsletter,
                    f'Bülten başarıyla gönderildi: {sent_count}/{newsletter.total_recipients} email gönderildi'
                )
            else:
                newsletter.status = 'sent'
                self.stdout.write(self.style.WARNING(f'\n⚠ Newsletter sent with errors: {sent_count}/{newsletter.total_recipients} sent ({failed_count} failed)'))
                NewsletterLog.log_warning(
                    newsletter,
                    f'Bülten hatalarla gönderildi: {sent_count}/{newsletter.total_recipients} gönderildi ({failed_count} başarısız)'
                )
            
            newsletter.save()
        
        self.stdout.write(self.style.SUCCESS(f'\n{"="*60}'))
        self.stdout.write(self.style.SUCCESS('Scheduled newsletter processing completed.'))
        self.stdout.write(self.style.SUCCESS(f'{"="*60}\n'))
