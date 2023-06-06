from django.db import models
from django.utils.translation import gettext as _


class StatusChoices(models.TextChoices):
    APPROVED = _('approved')
    REJECTED = _('rejected')
    WAITING_FOR_APPROVAL = _('waiting_for_approval')

class PayChoices(models.TextChoices):
    CASH = _('Cash')
    CARD = _('Card')
