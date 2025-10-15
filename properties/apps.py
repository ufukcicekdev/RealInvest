from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)


class PropertiesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "properties"
    
    def ready(self):
        """
        Called when Django starts - initialize the newsletter scheduler and signals
        """
        # Import signals to register them
        import properties.signals  # noqa
        
        # Import here to avoid AppRegistryNotReady error
        from properties.scheduler import start_scheduler
        
        # Start the scheduler (only once)
        try:
            start_scheduler()
            logger.info("Newsletter scheduler initialized successfully")
        except Exception as e:
            logger.error(f"Failed to start newsletter scheduler: {str(e)}")
