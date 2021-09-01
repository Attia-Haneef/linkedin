from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Member

@receiver(pre_save, sender=Member)
def create_version(sender, instance, **kwargs):
    print('me hun signal')
    member_qs = Member.objects.filter(id=instance.id).first()
    if member_qs and member_qs.job_position != instance.job_position:
        instance.positionversion_set.create(job_position=member_qs.job_position)
