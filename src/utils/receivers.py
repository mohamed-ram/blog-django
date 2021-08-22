from django.utils.datetime_safe import datetime
from django.utils.text import slugify

from utils.constants import PublishState


def slug_pre_save_receiver(sender, instance, **kwargs):
    if instance.title:
        instance.slug = slugify(instance.title)


def publish_state_pre_save_receiver(sender, instance, **kwargs):
    draft = PublishState.DRAFT
    if instance.state == draft:
        instance.timestamp = None
    else:
        instance.timestamp = datetime.now()


def post_author_pre_save_receiver(sender, instance, **kwargs):
    pass