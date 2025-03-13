from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import UserProfile, User

@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance) 
        #Il campo user di UserProfile verrà popolato da instance che contiene il valore di user appena creato dal sender
    else: #Nel caso di update per esempio
        try: #Se lo UserProfile esiste già
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except: #Se lo UserProfile per qualche motivo non esiste
            UserProfile.objects.create(user=instance)

@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):
    print(instance.username, 'this user is being saved')

        

#post_save.connect(post_save_create_profile_receiver, sender=User)