from __future__ import unicode_literals
from django.db import models
from django.dispatch import receiver


class WordPointer(models.Model):
    word = models.CharField(max_length=100, primary_key=True)
    lemmas = models.ManyToManyField("self", blank=True, related_name='derivations',symmetrical=False)
    
    def entry_number(self):
        return self.dict_entry.filter(has_def=True).count()
    entry_number = property(entry_number) 
    
    def lemma(self, source = 'all'):
        if source == 'all':
            return self.dict_lemmas.all()
        if source == 'learner':
            return self.dict_lemmas.filter(dict_type = source)
        if source == 'collegiate':
            return self.dict_lemmas.filter(dict_type = source)
        return []
    
    def entry(self, source = 'all'):
        if source == 'all':
            return self.dict_entry.all()
        if source == 'learner':
            return self.dict_entry.filter(dict_type = source)
        if source == 'collegiate':
            return self.dict_entry.filter(dict_type = source)
        return []
        
    def update_lemmas(self):
        self.lemmas.clear()
        self.save()
        for ep in self.dict_lemmas.all():
            self.lemmas.add(ep.word_pointer)
        for cf in self.coca.all():
            self.lemmas.add(cf.lemma_pointer)
        self.save()
            
    
    def __unicode__(self):
        return self.word


#////////////////////////////////////////////////////////////
# Data Structure for COCA 
#////////////////////////////////////////////////////////////

class CocaDict(models.Model):
    coca=models.DecimalField(max_digits=15, decimal_places=4)
    bnc=models.DecimalField(max_digits=15, decimal_places=4)
    soap=models.DecimalField(max_digits=15, decimal_places=4)
    y1950_89=models.DecimalField(max_digits=15, decimal_places=4)
    y1900_49=models.DecimalField(max_digits=15, decimal_places=4)
    y1800s=models.DecimalField(max_digits=15, decimal_places=4)
    coca_spok=models.DecimalField(max_digits=15, decimal_places=4)
    coca_fic=models.DecimalField(max_digits=15, decimal_places=4)
    coca_mag=models.DecimalField(max_digits=15, decimal_places=4)
    coca_news=models.DecimalField(max_digits=15, decimal_places=4)
    coca_acad=models.DecimalField(max_digits=15, decimal_places=4)
    bnc_spok=models.DecimalField(max_digits=15, decimal_places=4)
    bnc_fic=models.DecimalField(max_digits=15, decimal_places=4)
    bnc_mag=models.DecimalField(max_digits=15, decimal_places=4)
    bnc_news=models.DecimalField(max_digits=15, decimal_places=4)
    bnc_noAc=models.DecimalField(max_digits=15, decimal_places=4)
    bnc_acad=models.DecimalField(max_digits=15, decimal_places=4)
    bnc_misc=models.DecimalField(max_digits=15, decimal_places=4)
    def __unicode__(self):
        try: 
            return 'Freq Dict of \'' + self.as_freq.headword + '\' [' + self.as_freq.pos + ']'
        except:
            pass
        try: 
            return 'Text Dict of \'' + self.as_text.headword + '\' [' + self.as_text.pos + ']'
        except:
            pass
        try: 
            return 'Raw Freq Dict of \'' + self.as_raw_freq.headword + '\' [' + self.as_raw_freq.pos + ']'
        except:
            pass
        try: 
            return 'Raw Freq Dict of \'' + self.as_raw_text.headword + '\' [' + self.as_raw_text.pos + ']'
        except:
            return "COCA Dict belongs to no word"

class CocaFreq(models.Model): 
    rank = models.IntegerField(primary_key=True)
    headword = models.CharField(max_length=30)
    word_pointer = models.ForeignKey(WordPointer,related_name='coca', null=True)
    lemma = models.CharField(max_length=30)
    lemma_pointer = models.ForeignKey(WordPointer,related_name='coca_as_lemma', null=True)
    pos = models.CharField(max_length=30)
    cap_freq =  models.DecimalField(max_digits=18, decimal_places=17, blank=True, null=True)
    us_uk = models.CharField(max_length=5,blank=True, null=True)
    raw_freq = models.IntegerField()
    freq_dict = models.OneToOneField(CocaDict, related_name='as_freq', on_delete=models.CASCADE)
    text_dict = models.OneToOneField(CocaDict, related_name='as_text', on_delete=models.CASCADE)
    raw_freq_dict = models.OneToOneField(CocaDict, related_name='as_raw_freq', on_delete=models.CASCADE)
    raw_text_dict = models.OneToOneField(CocaDict, related_name='as_raw_text', on_delete=models.CASCADE)
    
    def freq(self, typ = "raw"):
        """docstring for freq"""
        
        #dicty={
        #    "coca":coca, "bnc":bnc, "sopa":sopa,
        #    "1950-89":y1950_89, "1900-49":y1900_49,"1800s":y1800s,
        #    "coca_spok":coca_spok, "coca_fic":coca_fic, "coca_mag":coca_mag, "coca_news":coca_news, "coca_acad":coca_acad,
        #    "bnc_spok":bnc_spok, "bnc_fic":bnc_fic, "bnc_mag":bnc_mag, "bnc_news":bnc_news, "bnc_noAc":bnc_noAc, "bnc_acad":bnc_acad, "bnc_misc":bnc_misc 
       # }
        try:
            return float(getattr(self.freq_dict,typ))
        except:
            #print float(self.raw_freq/450000000)
            return float(self.raw_freq/464)

            
    def __unicode__(self):
         return str(self.rank)+' '+self.headword+' '+str(self.raw_freq)
          
#////////////////////////////////////////////////////////////
# Data Structure for Dictionary Enrty
#//////////////////////////////////////////////////////////// 
 
class EntryPointer(models.Model):
    entry_id = models.CharField(max_length=100, primary_key=True) 
    dict_type = models.CharField(max_length=50, blank=True)
    type_id = models.CharField(max_length=100)#<entry>    
    headword = models.CharField(max_length=100, blank=True)

    pos = models.CharField(max_length=50, blank=True)
    has_def = models.BooleanField(default=False)
    word_pointer = models.ForeignKey(WordPointer,related_name='dict_entry', null=True)
    derivations = models.ManyToManyField(WordPointer,related_name='dict_lemmas')
    
    def _get_data(self):
        return self.data_model.data
    data = property(_get_data)
    def __unicode__(self):
        return self.headword
        
class EntryData(models.Model):
    entry_id = models.CharField(max_length=100, primary_key=True)
    dict_type = models.CharField(max_length=50, blank=True)
    type_id = models.CharField(max_length=100)#<entry>
    headword = models.CharField(max_length=100, blank=True)

    pointer = models.OneToOneField(EntryPointer, related_name='data_model', on_delete=models.CASCADE)
    data = models.TextField(max_length=50000)
    def __unicode__(self):
        return self.headword
    
#////////////////////////////////////////////////////////////////////
# Undefined New Word Structure
#//////////////////////////////////////////////////////////////////// 

class Ngrams(models.Model):
    word = models.CharField(max_length=100, primary_key=True)
    word_pointer = models.ForeignKey(WordPointer,related_name='ngrams', null=True)
    raw_freq = models.DecimalField(null=True,max_digits=15, decimal_places=4)
    def __unicode__(self):
        return self.word, self.raw_freq

#////////////////////////////////////////////////////////////////////
# Undefined New Word Structure
#//////////////////////////////////////////////////////////////////// 

class UndefinedWordPointer(models.Model):
    word = models.CharField(max_length=100, primary_key=True)
    undefined = models.BooleanField(default=False)
    
    def update(self, forced = False):
        if self.undefined and not forced: return
        if not self.word.isalpha() and not forced: 
            self.undefined = True
            self.save()
            return
        from db_backend.learner_api_query import add_learner
        from db_backend.collegiate_api_query import add_collegiate
        token = self.word
        added = False
        added = add_learner(token) or added
        added = add_collegiate(token) or added
        if added and WordPointer.objects.filter(word=token).count()>0 and WordPointer.objects.get(word=token).entry_number !=0:
            self.delete()
        else:
            self.undefined = True
            self.save()
    
    def __unicode__(self):
        return self.word
    @classmethod
    def unprocessed(cls):
        return cls.objects.filter(undefined = False)   
    
#////////////////////////////////////////////////////////////
# Raw Data
#////////////////////////////////////////////////////////////  

class LearnerRaw(models.Model):
    alpha = models.CharField(max_length=40, primary_key=True)
    data = models.TextField(max_length=50000)
    def __unicode__(self):
        return self.alpha

class CollegiateRaw(models.Model):
    alpha = models.CharField(max_length=40, primary_key=True)
    data = models.TextField(max_length=50000)

