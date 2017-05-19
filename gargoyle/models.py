from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import MaxValueValidator, MinValueValidator

from lexicon.models import EntryPointer
from ums.models import Profile
import lxml.etree as ET
from lxml.etree import tostring
from itertools import chain

# Create your models here.
import copy
import re
import os


class Comment(models.Model):
    day = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=30,blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    content = models.CharField(max_length=10000)


class TempFile(models.Model):
    saved_date = models.DateTimeField(editable=False, default=timezone.now)
    request_id = models.CharField(max_length=200,blank=True, null=True)
    owner = models.ForeignKey(Profile, blank=True, null=True, related_name='temp_files')
    upload = models.FileField(upload_to='temp/%Y/%m/')
    

def _delete_file(path):
   """ Deletes file from filesystem. """
   if os.path.isfile(path):
       os.remove(path)


@receiver(models.signals.post_delete, sender=TempFile)
def delete_file(sender, instance, *args, **kwargs):
    """ Deletes image files on `post_delete` """
    if instance.upload:
        _delete_file(instance.upload.path)

class VocabPreference(models.Model):
    DICT_PREF = (
        (1,1),
        (2,2),
     )
    owner = models.OneToOneField(Profile, blank=True, null=True, related_name='vocab_preference',on_delete=models.CASCADE)
    show_cutoff = models.FloatField(default=4.3, validators = [MinValueValidator(-2.0), MaxValueValidator(10)])
    diff_cutoff = models.FloatField(default=6, validators = [MinValueValidator(-2.0), MaxValueValidator(10)])
    learner_pref = models.IntegerField(choices=DICT_PREF, default=1)
    webster_pref = models.IntegerField(choices=DICT_PREF, default=2)
    
    def _get_dict_pref(self):
        return {'learner':self.learner_pref, 'collegiate':self.webster_pref}
    dict_pref = property(_get_dict_pref)

@receiver(post_save, sender=Profile)
def create_vocab_preference(sender, instance, created, **kwargs):
    if created:
        VocabPreference.objects.create(owner=instance)    
    
@receiver(post_save, sender=Profile)
def save_vocab_preference(sender, instance, **kwargs):
    instance.vocab_preference.save()

class SessionVariables(models.Model):
    request_id = models.CharField(max_length=125, primary_key=True)
    saved_date = models.DateTimeField(editable=True, default=timezone.now)
    name = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(Profile, blank=True, null=True, related_name='session_variables')
    glossary_dict = models.TextField(blank=True, null=True)
    initial_select_table = models.TextField(blank=True, null=True)
    select_table = models.TextField(blank=True, null=True)
    quiz_select_table = models.TextField(blank=True, null=True)
    progress = models.FloatField(blank=True, null=True,default=3)
    def save(self, *args, **kwargs):
        self.saved_date = timezone.now()
        super(SessionVariables, self).save(*args, **kwargs)


class EntryPointerQuery(EntryPointer):
    class Meta:
        proxy = True
        
    def get_def_vi(self,sense):
        return self.webster_get_def_vi(sense)
        if self.dict_type == 'learner':
            #return 'NOT IN Collegiate', '', '-1', False
            return  self.learner_get_def_vi(sense)
        return self.collegiate_get_def_vi(sense)
    
    def webster_get_def_vi(self, sense, un = True):
        sense = str(sense)
        root = ET.fromstring(self.data.encode('utf-8'))
        if sense == '-1':
            if root.find('def') == None: return 'NO DEF','', sense, True
            flag= True
            vi = ''
            def_ = ''
            sense = -1
            high_light = True
            while flag:
                sense = sense + 1
                def_, vi, sense, high_light = self.webster_get_def_vi(sense)
                sense = int(sense)
                flag = def_[:6] == '<dt><s' and sense+1 < len(root.findall('def/dt')) 
            high_light = sense!=0
            try:
                flag = False
                psense = root.xpath('def/sn[count(preceding-sibling::dt)='+str(sense)+']')
                flag = psense == [] or psense[-1].text[-1:].isdigit()
                if flag and root.xpath('def/sn[count(preceding-sibling::dt)='+str(sense+1)+']')[0].text[0].isalpha():
                    defe, vi, sensee, high_light = self.webster_get_def_vi(sense+1)
                    def_ = def_+' '+defe
                    sense = str(sense) + ',' + str(sensee)
                    high_light = True
            except:
                pass
            def_, vi, sense, high_lighte = self.webster_get_def_vi(sense)
            return def_, vi, str(sense), high_light
        if ',' not in sense:
            try:
                dt = root.findall('def/dt')[int(sense)]
            except:
                return self.webster_get_def_vi('-1')
            high_light = False
            def_ = stringify_children(dt)
            if def_[0]==' ':def_=def_[1:]
            if def_[0]==':':def_=def_[1:]
            vie = dt.find('.//vi')
            vi = stringify_children(vie) if vie != None else ''
            high_light = def_[0]=='<'
            return '<dt>'+def_ +'</dt>', vi, str(sense) , high_light
        else:
            senses = map(int, sense.split(','))
            cluster_list = []
            vi = ''
            cluster={'psense':[],'def':'','sd':[],'sn':'','snp':'','csn':''}
            psense = []
            for n in range(0,senses[0]+1):
                psense = root.xpath('def/sn[count(preceding-sibling::dt)='+str(n)+']')
                for s in psense:
                    cluster['psense'].append('<sn>'+stringify_children(s)+'</sn>')
            if psense !=[]:
                cluster['csn']='<sn>'+stringify_children(psense[-1])+'</sn>'
            for i, isense in enumerate(senses):
                def_, vii, s , high_light = self.webster_get_def_vi(isense)
                cluster['def'] = '<dt>'+def_+'</dt>'
                if vi == '': vi = vii
                acluster=copy.deepcopy(cluster)
                cluster_list.append(acluster)
                cluster={'psense':[],'def':'','sd':[],'sn':'','snp':'','csn':''}
                if i < len(senses)-1:
                    for n in range(isense+1, senses[i+1]+1):
                        nsense = root.xpath('def/sn[count(preceding-sibling::dt)='+str(n)+']')
                        for s in nsense:
                             cluster['psense'].append('<sn>'+stringify_children(s)+'</sn>')
                             if n == senses[i+1]: cluster['csn']='<sn>'+stringify_children(s)+'</sn>'
                    nsd = root.xpath('def/sd[count(preceding-sibling::dt)='+str(senses[i+1])+']')
                    for s in nsd:
                        cluster['sd'].append('<sd>'+stringify_children(s)+'</sd>')
            for i in range(len(cluster_list)-1):
                if cluster_list[i+1]['psense']!=[]:
                    cluster_list[i+1]['sd']=[]
            
            sn_counter = 0
            sn_list = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
            csn_flag = False
            ppsn_flag = False
            psn_flag = False
            
            for s in cluster_list[0]['psense']:
                sensex = ET.fromstring(s.encode('utf-8'))
                if sensex.text!=None and re.search('[a-zA-Z]',sensex.text): psn_flag = True
            for i in range(len(cluster_list)-1):
                nsn_flag = False
                nsn_no = True
                for j in range(i+1,len(cluster_list)):
                    for s in cluster_list[j]['psense']:
                        nsn_no = False
                        sensex = ET.fromstring(s.encode('utf-8'))
                        if sensex.text is not None and re.search('[a-zA-Z]',sensex.text): nsn_flag = True
                for s in cluster_list[i]['psense']:
                    sensex = ET.fromstring(s.encode('utf-8'))
                    if sensex.text is not None and re.search('[a-zA-Z]',sensex.text): psn_flag = True
                print psn_flag, nsn_flag, nsn_no, ppsn_flag
                #if  psn_flag and (nsn_flag or (nsn_no and ppsn_flag)): # sphere; despair
                if  psn_flag and (nsn_flag or (ppsn_flag)): 
                    cluster_list[i]['sn']=sn_list[sn_counter]
                    sn_counter+=1
                    ppsn_flag = True
                psn_flag = False
                csn_flag = False
            for s in cluster_list[i+1]['psense']:
                sensex = ET.fromstring(s.encode('utf-8'))
                if sensex.text is not None and re.search('[a-zA-Z]',sensex.text): psn_flag = True
            if psn_flag and ppsn_flag: 
                cluster_list[i+1]['sn']=sn_list[sn_counter] 
            
            snp_counter = 1
            csnp_flag = False
            if cluster_list[0]['csn']!='':
                sensex = ET.fromstring(cluster_list[0]['csn'].encode('utf-8'))
                if sensex.find('snp') is not None: csnp_flag = True

            psnp_flag = False
            for i in range(len(cluster_list)-1):
                if cluster_list[i]['sn']!='': psnp_flag = False
                nsnp_flag = False
                for j in range(i+1,len(cluster_list)):
                    if cluster_list[j]['sn']!='':break
                    if cluster_list[j]['csn']!='':
                        sensex = ET.fromstring(cluster_list[j]['csn'].encode('utf-8'))
                        if sensex.find('snp') is not None: nsnp_flag = True
                
                csnp_flag = False
                if cluster_list[i]['csn']!='':
                    sensex = ET.fromstring(cluster_list[i]['csn'].encode('utf-8'))
                    if sensex.find('snp') is not None: csnp_flag = True
                                
                if (csnp_flag and psnp_flag) or (csnp_flag and nsnp_flag):
                    cluster_list[i]['snp'] = str(snp_counter)
                    snp_counter+=1
                    psnp_flag = True
            if nsnp_flag and psnp_flag:
                cluster_list[i+1]['snp'] = str(snp_counter)
            
            defs=''
            for cluster in cluster_list:
                if cluster['sn']!='' or cluster['snp']!='':
                    defs += ' <sn>'+cluster['sn']
                    if cluster['snp']!='':
                        defs += ' <snp>('+cluster['snp']+')</snp>'
                    defs += '</sn> '
                for sd in cluster['sd']: defs += sd
                defs += ' '+cluster['def']
            return defs, vi, sense, False
        return 'NO DEF', '', sense, True
        
    def group_sense(self, senses):
        root = ET.fromstring(self.data.encode('utf-8'))
        new_senses = []
        flag = False
        for n, sense in enumerate(senses):
            try: sense = int(sense)
            except: break
            if n == 0: 
                new_senses.append(str(sense))
            else:
                psense = root.xpath('def/sn[count(preceding-sibling::dt)='+str(int(senses[n]))+']')
                flag = flag or psense == [] or (psense[0].text is None) or psense[0].text[0].isalpha()
                ps = int(senses[n-1])
                for i in xrange(ps, sense):
                    isenses = root.xpath('def/sn[count(preceding-sibling::dt)='+str(i+1)+']')
                    for isense in isenses:
                        flag =  flag and (isense.text is None or isense.text[0].isalpha())
                if flag: 
                    new_senses[-1]=new_senses[-1]+','+str(sense)
                else:
                    new_senses.append(str(sense))                    
        return new_senses


def stringify_children(node, ignore_tags=[]):
    parts = [node.text if node.text else None]
    for c in node.getchildren():
        if c.tag in ignore_tags: break
        parts.append(tostring(c,encoding='unicode'))
    return ''.join(filter(None, parts))

    
def stringify_learner_def(node):
    ignore_tags=['vi','un','snote','wsgram','dx']
    #ignore_tags = []
    return stringify_children(node, ignore_tags)