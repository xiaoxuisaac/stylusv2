import os
from django.shortcuts import render
import requests
from django.urls import reverse
from requests.auth import HTTPBasicAuth
from django.http import HttpResponse
from django.core.files.uploadedfile import SimpleUploadedFile

import json as simplejson
import urllib2
from models import *
from signals import *

import string
import random

def ocrwebservice(f,p='&pagerange=1-100'):
    code='0410F73C-4778-4AC9-8B5D-AF80E479FA74'
    username='XIAOXUISAAC'
    url='http://www.ocrwebservice.com/restservices/processDocument?gettext=true&outputformat=doc&newline=1'+p
    result=requests.post(url,files={'file':f},auth=HTTPBasicAuth(username, code))
    #print result
    #print result.json()
    return result

def analyze_to_json(request):
    text='None'
    url=''
    notice=''
    file_name = ''
    pages = 0
    if request.method == 'POST':
        f=request.FILES['upload']
        if not request.user.is_authenticated():
            response=ocrwebservice(f,'&pagerange=5')
            notice='You are not loged in, so only the first 5 pages of the file is processed. <a href=\'/accounts/login/\'>Login</a> or <a href=\'/accounts/register/\'>Regsister</a>'
        elif pages_remain(request.user.profile) == 0:
            response=ocrwebservice(f,'&pagerange=5')
            notice='You do not have any pages to process left in you plan, so only the first 5 pages of the file was processed. To add more pages, <a href=\''+reverse('profile')+'get_ocr\''+'target=\'_blank\'>click here</a>'
        else:
            if request.user.is_staff:
                response=ocrwebservice(f)
            else:
                response=ocrwebservice(f,'&pagerange=1-100')
            try:
                remain = pages_deduct(request.user.profile,response.json()['ProcessedPages'])
                notice = str(response.json()['ProcessedPages'])+' pages processed. You have '+str(remain)+' pages remain. To add more pages, <a href=\''+reverse('profile')+'get_ocr\''+'target=\'_blank\'>click here</a>'
            except:
                notice = 'Error occured. If you tried to process more than 100 pages PDF, then try less.'
        pages = response.json()['ProcessedPages']
        try:
            text=response.json()['ErrorMessage']+'\n\n'.join([item for sublist in response.json()['OCRText'] for item in sublist])
            url=response.json()['OutputFileUrl']
        except:
            pass
        if url != '':
            response = requests.get(url)
            #file_to_save = response.read()
            file_name = os.path.splitext(request.FILES['upload'].name)[0] + '.doc'
            word_file = SimpleUploadedFile(file_name, response.content, content_type="application/msword")
            file_field = OcrFile(upload = word_file)
            if request.user.is_authenticated():
                file_field.owner = request.user.profile
            file_field.save()
            url =  file_field.upload.url
    data=simplejson.dumps({
        'text':text,
        'url':url,
        'notice':notice
        })
    file_ocred.send(sender=None, request = request, name = file_name, url = url, pages = pages)
    return HttpResponse(data, content_type='application/json')

def pages_remain(profile):
    page=0
    for ocrbundle in profile.ocrbundles.all():
        page = page + ocrbundle.remain()
    return page
    
def pages_deduct(profile, pages):
    bundles = sorted(profile.ocrbundles.all(),
            key=lambda bundle:bundle.activation_date + datetime.timedelta(bundle.expiration_date))
    for ocrbundle in bundles:
        if ocrbundle.remain() > pages:
            ocrbundle.remains = ocrbundle.remains - pages
            pages=0
            ocrbundle.save()
            break
        else:
            pages = pages - ocrbundle.remain()
            ocrbundle.remains = 0;
            ocrbundle.save()
    return pages_remain(profile)


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for i in range(size))
    
    
    