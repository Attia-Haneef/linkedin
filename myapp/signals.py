from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Member


@receiver(pre_save, sender=Member)
def create_version(sender, instance, **kwargs):
    position_qs = Member.objects.filter(id=instance.id)
    if position_qs and position_qs[0].job_poistion != instance.job_position:
        instance.positionversion_set.create(job_position=position_qs[0].job_position)
