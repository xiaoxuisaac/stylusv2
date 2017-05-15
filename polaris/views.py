from django.shortcuts import render
from models import *
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings


# Create your views here.

@user_passes_test(lambda u: u.is_superuser)
def log_compound(request):
    lds = LogData.objects.order_by('-created_date')
    logs=[]
    for ld in lds:
        if ld.owner == None:
            owner = 'anonymous'
        else:
            owner = ld.owner.user.username
        if ld.owner == None or (ld.owner != None and (not ld.owner.user.is_superuser)) or settings.DEBUG:
         logs.append({'time':ld.created_date, 'ip':ld.ip_addr,'owner':owner, 'info': ld.info})
    return render(request,'log.html',{'logs':logs})
    