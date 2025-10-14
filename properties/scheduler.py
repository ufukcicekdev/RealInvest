"""
Newsletter Scheduler Service
Automatically sends scheduled newsletters using APScheduler
"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django.conf import settings
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler(timezone=str(timezone.get_current_timezone()))


def check_and_send_newsletters():
    """
    Check for scheduled newsletters and send them if time has come
    This function runs every minute
    """
    from properties.models import Newsletter
    
    now = timezone.now()
    
    # Get all scheduled newsletters whose time has come
    newsletters = Newsletter.objects.filter(
        status='scheduled',
        scheduled_date__lte=now
    )
    
    for newsletter in newsletters:
        logger.info(f"Processing scheduled newsletter: {newsletter.title}")
        
        try:
            # Call the background send method
            newsletter._send_newsletter_background()
            logger.info(f"Successfully sent newsletter: {newsletter.title}")
        except Exception as e:
            logger.error(f"Error sending newsletter {newsletter.title}: {str(e)}")


def start_scheduler():
    """
    Start the background scheduler
    This should be called when Django starts
    """
    if scheduler.running:
        logger.info("Scheduler already running")
        return
    
    # Add job to check newsletters every minute
    scheduler.add_job(
        check_and_send_newsletters,
        trigger=IntervalTrigger(minutes=1),
        id='newsletter_check',
        name='Check and send scheduled newsletters',
        replace_existing=True,
    )
    
    scheduler.start()
    logger.info("Newsletter scheduler started - checking every minute")


def stop_scheduler():
    """
    Stop the scheduler (called on app shutdown)
    """
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Newsletter scheduler stopped")
