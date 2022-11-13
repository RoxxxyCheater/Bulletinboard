from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from ignore import DEFAULT_FROM_EMAIL
#Signal.connect(receiver, sender=None, weak=True, dispatch_uid=None)


@receiver(post_save, sender=Comment)
def comment_email_sender(sender, instance, created, **kwargs):
    print(sender, instance, created)
    if instance.Ad.author.email != instance.commAuthor.email:
        if created:
            comment_obj_subject = f'A new comment {instance.content} has been published by {instance.commAuthor.username } on your Ad {instance.Ad} dated {instance.created_at}'
            Recipient = instance.Ad.author.email
        else:
            comment_obj_subject = f'Your comment {instance.content} to the Ad {instance.Ad} was accepted by the Ad author {instance.Ad.author.username}'
            Recipient = instance.commAuthor.email
        html_content = render_to_string(
            'comment_update.html',
            {
                'comment': instance,
            }
        )    
        
        msg = EmailMultiAlternatives(
            subject=comment_obj_subject,
            body= instance.content,
            from_email=DEFAULT_FROM_EMAIL,
            to=[Recipient],
        )
        
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        print(msg)
        print("!!!!!!!!!!!email_sent!!!!!!!!!!")
