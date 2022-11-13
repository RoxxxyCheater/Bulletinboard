from django.apps import AppConfig
from django.db.models.signals import post_save


class BulletinboardappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bulletinboardapp'

    def ready(self):
        import bulletinboardapp.signals
        # post_save.connect(comment_email_sender)