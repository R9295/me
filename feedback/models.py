import uuid

from django.db import models
from django.utils.timezone import now

from accounts.models import User

FEEDBACK_TYPES = (
    ('BUG', 'Bug'),
    ('FEEDBACK', 'Feedback'),
)


class Feedback(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    message = models.TextField()
    type = models.CharField(choices=FEEDBACK_TYPES,
                            max_length=8)
    date = models.DateTimeField(default=now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{0} : {1}'.format(self.user.email, self.type)
