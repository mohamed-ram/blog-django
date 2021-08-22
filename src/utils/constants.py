from django.db import models


class PublishState(models.TextChoices):
    PUBLISHED = "PUBLISHED", "Published"
    DRAFT = "DRAFT", "Draft"
    PRIVATE = "PRIVATE", "Private"


class RatingValues(models.IntegerChoices):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    
    __empty__ = "Unknown"



