from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from utils.constants import RatingValues

User = get_user_model()

class Rate(models.Model):
    value = models.IntegerField(choices=RatingValues.choices, null=True, blank=True)
    comment = models.TextField(max_length=400, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='rates')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    




# user = User.objects.first()
# post= Post.objects.last()

# Rate.objects.create(user=user, content_object=post, value=3)
# Rate.objects.first().aggregate(Avg("value")) >>> 3.2/5

# post.ratings.aggregate(Avg("value"))
