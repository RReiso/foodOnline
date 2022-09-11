from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User, UserProfile

# signals
# one way how to conncet receiver with a sender (using decorator)
# this function will run after user is created/updated


@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    print(sender)
    print(instance)
    print(created)
    print(kwargs)
    if created:
        UserProfile.objects.create(user=instance)
    else:
        try:
            # when changes are made to user, find associated userprofile and save?
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            # when updating a user but userprofile does not exist (maybe deleted profile)
            UserProfile.objects.create(user=instance)
        print('user is updated')

    # post_save.connect(post_save_create_profile_receiver, sender=User) -- another way how to connect receiver with a sender


# this function is triggered just before a user is created/updated
@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):
    print(instance.username, '-- user is being saved')
