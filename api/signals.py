from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, Source, SourceAccess

@receiver(post_save, sender=User)
def create_profile(sender, instance, **kwargs):
    try:
        profile = instance.profile
    except Profile.DoesNotExist:
        profile = Profile(user=instance)

    all_sources = Source.objects.all()
    public_access = SourceAccess.objects.get(name="Public")
    public_sources = Source.objects.filter(access=public_access)

    if instance.is_superuser or instance.is_staff:
        profile.access_level = 3
    else:
        profile.access_level = 1

    profile.save()
    profile.sources.set(all_sources if instance.is_superuser or instance.is_staff else public_sources)


@receiver(post_save, sender=Source)
def create_or_update_source(sender, instance, created, **kwargs):
    # Get all the profiles with the corresponding access level
    access_levels_count = SourceAccess.objects.count()+1

    for access_level in range(1, access_levels_count):
        profiles = Profile.objects.filter(access_level__gte=access_level)

        # Add or remove the source to/from the profile depending on the access level
        if created:
            for profile in profiles:
                if instance.access.level <= access_level:
                    profile.sources.add(instance)
        else:
            for profile in profiles:
                if instance.access.level > access_level:
                    profile.sources.remove(instance)
                elif instance.access.level <= access_level:
                    profile.sources.add(instance)
