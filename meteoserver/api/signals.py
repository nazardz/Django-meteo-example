from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, Source, SourceAccess

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

        public_access = SourceAccess.objects.get(name="Public")
        public_sources = Source.objects.filter(access=public_access)
        instance.profile.sources.add(*public_sources)
