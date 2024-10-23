from django.db import models
import django


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )
    

def get_duration(visit):
    enter_time = django.utils.timezone.localtime(visit.entered_at)
    if not visit.leaved_at:
        end_of_visit = django.utils.timezone.localtime()
    else:
        end_of_visit = visit.leaved_at
    delta = end_of_visit-enter_time  
    return delta


def format_duration(delta):
    total_seconds = delta.total_seconds()
    hours_in_store = total_seconds//3600
    minutes_in_store = (total_seconds%3600)//60
    duration = f'{int(hours_in_store):02}ч {int(minutes_in_store):02}мин'
    return duration


def is_visit_long(visit):
    delta = get_duration(visit)
    seconds = delta.total_seconds()
    total_minutes = seconds/60
    is_visit_long = total_minutes > 60
    return is_visit_long
    