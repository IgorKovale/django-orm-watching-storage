from datacenter.models import Visit
from django.shortcuts import render
from datacenter.models import get_duration
from datacenter.models import format_duration
import django


def storage_information_view(request):
    visits = Visit.objects.filter(leaved_at=None)
    non_closed_visits = []
    for visit in visits:
        delta = get_duration(visit)
        duration = format_duration(delta)
        non_closed_visits.append({
                'who_entered': visit.passcard.owner_name,
                'entered_at': django.utils.timezone
                .localtime(visit.entered_at),
                'duration': duration
            })
    context = {
            'non_closed_visits': non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
