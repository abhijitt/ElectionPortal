import random

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords
from django.core.validators import MaxValueValidator
from django.conf import settings


class Election(models.Model):
    name = models.CharField(max_length=64, db_index=True)
    creator = models.ForeignKey(User, related_name='elections', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False, db_index=True)
    is_temporary_closed = models.BooleanField(default=False, help_text='Election temporary closed')
    is_finished = models.BooleanField(default=False, db_index=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    is_key_required = models.BooleanField(default=True)
    session_timeout = models.PositiveSmallIntegerField(default=120,
                                                       validators=[
                                                            MaxValueValidator(600),
                                                        ],
                                                       help_text='Seconds after which session will be timed out')
    _history_ = HistoricalRecords()

    @property
    def has_activated(self):
        return self.is_active or self.is_finished

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.is_finished and self.finished_at is None:
            self.finished_at = timezone.now()
        if not self.is_finished:
            self.finished_at = None

        return super().save(force_insert=False, force_update=False, using=None, update_fields=None)

    def __str__(self):
        return self.name


class Tag(models.Model):
    tag = models.SlugField(max_length=16, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User)

    def __str__(self):
        return self.tag


def generate_random_voter_key():
    return ''.join(random.choice('0123456789ABCDEF') for _ in range(settings.VOTER_KEY_LENGTH))


class Voter(models.Model):
    roll_no = models.CharField(max_length=10, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    election = models.ForeignKey(Election, related_name='voters', db_index=True)
    key = models.CharField(max_length=settings.VOTER_KEY_LENGTH, default=generate_random_voter_key)
    voted = models.BooleanField(default=False, db_index=True)
    voted_at = models.DateTimeField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        unique_together = ['roll_no', 'election']

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.pk is None and self.voted:
            self.voted_at = timezone.now()
        return super().save(force_insert=force_insert, force_update=force_update, using=using,
                            update_fields=update_fields)

    def __str__(self):
        return self.roll_no
