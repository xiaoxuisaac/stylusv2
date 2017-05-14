from __future__ import unicode_literals
from django.db import models

class WordPointer(models.Model):
    word = models.CharField(max_length=100, primary_key=True)
    
    def entry_number(self):
        return self.learner.count()+self.collegiate.count()
    entry_number = property(entry_number) 
    
    def delete_entry(self):
        for e in self.learner.all():
            e.delete()
        for e in self.collegiate.all():
            e.delete()
    
    def lemma(self, source = 'learner'):
        if source == 'learner':
            return self.learner_lemmas.all()
        if source == 'collegiate':
            return self.collegiate_lemmas.all()
        return []
    
    def entry(self, source = 'learner'):
        if source == 'learner':
            return self.learner.all()
        if source == 'collegiate':
            return self.collegiate.all()
        return []
        
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
        
        dicty={
            "coca":coca, "bnc":bnc, "sopa":sopa,
            "1950-89":y1950_89, "1900-49":y1900_49,"1800s":y1800s,
            "coca_spok":coca_spok, "coca_fic":coca_fic, "coca_mag":coca_mag, "coca_news":coca_news, "coca_acad":coca_acad,
            "bnc_spok":bnc_spok, "bnc_fic":bnc_fic, "bnc_mag":bnc_mag, "bnc_news":bnc_news, "bnc_noAc":bnc_noAc, "bnc_acad":bnc_acad, "bnc_misc":bnc_misc 
        }
        try:
            return self.freq_dic.dcty[typ] 
        except:
            return self.raw_freq

            
    def __unicode__(self):
         return str(self.rank)+' '+self.headword+' '+str(self.raw_freq)
     
#////////////////////////////////////////////////////////////
# Data Structure for Webster Learner Dictionary 
#////////////////////////////////////////////////////////////  

class LearnerEntry(models.Model):
    entry_id = models.CharField(max_length=100, primary_key=True)#<entry>
    headword = models.CharField(max_length=30) #<hw> may contain *
    hw_status_label = models.CharField(max_length=40, blank=True, null=True) #<hsl> head word status label, "US" or "chiefly US."
    pronunciation = models.CharField(max_length=100, blank=True, null=True) #<pr> may have multiple pronuanciations, noun, verb, B.E.
    alt_pron = models.CharField(max_length=100, blank=True, null=True)#<altpr> sense pronunciation 
    function = models.CharField(max_length=30, blank=True, null=True) #<fl> function lable. slightly different from part of speech in COCA, which doesn't have geographic name
    label = models.CharField(max_length=500, blank=True, null=True) #<lb> e.g. always/usually/not used before a noun and not used in progressive tenses
    raw = models.TextField(blank=True, null=True)
    @classmethod
    def find(LE,word):
        """docstring for find"""
        pass
        
class LearnerVariant(models.Model):
    root_entry = models.ForeignKey(LearnerEntry, related_name='variants', on_delete=models.CASCADE)
    label = models.CharField(max_length=40, blank=True, null=True)#<vl>
    form = models.CharField(max_length=40)#<va>
    pronunciation = models.CharField(max_length=100, blank=True, null=True) #<pr> may have multiple pronuanciations, noun, verb, B.E.
    alt_pron = models.CharField(max_length=100, blank=True, null=True)#<altpr> sense pronunciation 
    def _get_headword(self):
        """docstring for get_headword"""
        pass
    headword=property(_get_headword)
        
class LearnerInflection(models.Model):
    root_entry = models.ForeignKey(LearnerEntry, related_name='inflections', on_delete=models.CASCADE)
    label = models.CharField(max_length=40, blank=True, null=True)#<il> inflected form label
    form = models.CharField(max_length=40)#<if>
    pronunciation = models.CharField(max_length=100, blank=True, null=True)#<pr>
    alt_pron = models.CharField(max_length=100, blank=True, null=True)#<altpr> sense pronunciation
    def get_lemma(self):
        """docstring for get_lemma"""
        pass
          
class LearnerCrossEntry(models.Model):
    root_entry = models.ForeignKey(LearnerEntry, related_name='crossentry', on_delete=models.CASCADE)
    label = models.CharField(max_length=40, blank=True, null=True)#<cl>
    target = models.CharField(max_length=40)#<ct>
    def _get_headword(self):
        """docstring for get_headword"""
        pass
    headword=property(_get_headword)
    
class LearnerDefinition(models.Model):
    root_entry = models.ForeignKey(LearnerEntry, related_name='definitions', on_delete=models.CASCADE)
    d_grammar = models.CharField(max_length=500, blank=True, null=True)#<gram>
    status_label =  models.CharField(max_length=30, blank=True, null=True)#<sl> status/subject label. US, techinical, etc.
    
    #///////
    #below properties are sense specific, but not in <dt> tag
    #//////////
    sense = models.CharField(max_length=10, blank=True, null=True)#<sn>
    sense_pronunciation = models.CharField(max_length=100, blank=True, null=True)#<sp> sense pronunciation 
    sense_label = models.CharField(max_length=500, blank=True, null=True) #<slb> sense specific label, e.g. always/usually/not used before a noun and not used in progressive tenses
    sense_grammar = models.CharField(max_length=500, blank=True, null=True) #<sgram> sense specific. it is not in <dt> tag, but in the same position as <sn>
    sense_status_label = models.CharField(max_length=40, blank=True, null=True) #<ssl> sense status label, "US" or "chiefly US."
    sense_order = models.IntegerField() #order of sense in an entry
    
    #/////////////////
    #in <dt> tag below
    #/////////////////
    text = models.CharField(max_length=500, blank=True, null=True)
    
    def _get_headword(self):
        """docstring for get_headword"""
        pass
    headword=property(_get_headword)
    
class LearnerSenseSynonym(models.Model):#<sx>
    root_def = models.ForeignKey(LearnerDefinition, related_name='synonyms', on_delete=models.CASCADE)
    sense = models.CharField(max_length=10, blank=True, null=True) 
    target = models.CharField(max_length=40)#<ct>
    def _get_root_entry(self):
        """docstring for get_root_entry"""
        pass
    root_entry = property(_get_root_entry)
    
class LearnerIllustration(models.Model):
    root_def = models.ForeignKey(LearnerDefinition, related_name='illustrations', on_delete=models.CASCADE)
    text = models.CharField(max_length=200, blank=True, null=True)
    wsense_grammar = models.CharField(max_length=500, blank=True, null=True) #<wsgram> sense specific. in the sense
    def _get_root_entry(self):
        """docstring for get_root_entry"""
        pass
    root_entry = property(_get_root_entry)
    
    def _get_headword(self):
        """docstring for get_headword"""
        pass
    headword=property(_get_headword)
    
class LearnerSenseVariant(models.Model):
    root_def = models.ForeignKey(LearnerDefinition, related_name='variants', on_delete=models.CASCADE)
    label = models.CharField(max_length=40, blank=True, null=True)#<vl>
    form = models.CharField(max_length=40)#<va>
    pronunciation = models.CharField(max_length=100, blank=True, null=True) #<pr> may have multiple pronuanciations, noun, verb, B.E.
    alt_pron = models.CharField(max_length=100, blank=True, null=True)#<altpr> sense pronunciation
    def _get_root_entry(self):
        """docstring for get_root_entry"""
        return root_def.root_entry
    root_entry = property(_get_root_entry)
    
class LearnerSenseInflection(models.Model):
    root_def = models.ForeignKey(LearnerDefinition, related_name='inflections', on_delete=models.CASCADE)
    label = models.CharField(max_length=40, blank=True, null=True)#<il>
    form = models.CharField(max_length=40)#<if>
    pronunciation = models.CharField(max_length=100, blank=True, null=True) #<pr> may have multiple pronuanciations, noun, verb, B.E.
    alt_pron = models.CharField(max_length=100, blank=True, null=True)#<altpr> sense pronunciation
    def _get_root_entry(self):
        """docstring for get_root_entry"""
        pass
    root_entry = property(_get_root_entry)
    
class LearnerSenseUsageNote(models.Model):  
    root_def = models.ForeignKey(LearnerDefinition, related_name='usage_note', on_delete=models.CASCADE)
    text = models.CharField(max_length=200, blank=True, null=True)
    def __unicode__(self):
         return self.text
         
class LearnerSenseUsageNoteIllustration(models.Model):
    root_note = models.ForeignKey(LearnerSenseUsageNote, related_name='illustrations', on_delete=models.CASCADE)
    text = models.CharField(max_length=200, blank=True, null=True)
    def __unicode__(self):
         return self.text
         
class LearnerSenseSuppNote(models.Model):  
    root_def = models.ForeignKey(LearnerDefinition, related_name='supp_note', on_delete=models.CASCADE)
    text = models.CharField(max_length=200, blank=True, null=True)
    def __unicode__(self):
         return self.text
         
class LearnerSenseSuppNoteIllustration(models.Model):
    root_note = models.ForeignKey(LearnerSenseSuppNote, related_name='illustrations', on_delete=models.CASCADE)
    text = models.CharField(max_length=200, blank=True, null=True)
    def __unicode__(self):
         return self.text
         
class LearnerUndefinedRunOn(models.Model):
    root_entry = models.ForeignKey(LearnerEntry, related_name='uros', on_delete=models.CASCADE)
    form = models.CharField(max_length=200, blank=True, null=True) #<ure> 
    runon_status_label = models.CharField(max_length=40, blank=True, null=True) #<rsl> run-on status label, "US" or "chiefly US."
    pronunciation = models.CharField(max_length=100, blank=True, null=True)#<pr> 
    alt_pron = models.CharField(max_length=100, blank=True, null=True)#<altpr> sense pronunciation 
    function = models.CharField(max_length=30, blank=True, null=True) #<fl> function lable. slightly different from part of speech in COCA, which doesn't have geographic name
    label = models.CharField(max_length=500, blank=True, null=True) #<lb> e.g. always/usually/not used before a noun and not used in progressive tenses
    d_grammar = models.CharField(max_length=500, blank=True, null=True)#<gram>
    status_label =  models.CharField(max_length=30, blank=True, null=True)#<sl> US, techinical, etc.
    
    def _get_headword(self):
        """docstring for get_headword"""
        pass
    headword=property(_get_headword)

class LearnerUROVariant(models.Model):
    root_runon = models.ForeignKey(LearnerUndefinedRunOn, related_name='variants', on_delete=models.CASCADE)
    label = models.CharField(max_length=40, blank=True, null=True)#<vl>
    form = models.CharField(max_length=40)#<va>
    pronunciation = models.CharField(max_length=100, blank=True, null=True) #<pr> may have multiple pronuanciations, noun, verb, B.E.
    alt_pron = models.CharField(max_length=100, blank=True, null=True)#<altpr> sense pronunciation
    def _get_root_entry(self):
        """docstring for get_root_entry"""
        pass
    root_entry = property(_get_root_entry)
    
class LearnerUROInflection(models.Model):
    root_runon = models.ForeignKey(LearnerUndefinedRunOn, related_name='inflections', on_delete=models.CASCADE)
    label = models.CharField(max_length=40, blank=True, null=True)#<il>
    form = models.CharField(max_length=40)#<if>
    pronunciation = models.CharField(max_length=40, blank=True, null=True) #<pr> may have multiple pronuanciations, noun, verb, B.E.
    alt_pron = models.CharField(max_length=40, blank=True, null=True)#<altpr> sense pronunciation
    def _get_root_entry(self):
        """docstring for get_root_entry"""
        pass
    root_entry = property(_get_root_entry)
    
class LearnerDerivationManager(models.Manager):
    def get_queryset(self):
        return super(LearnerDerivation, self).get_queryset().filter()
                
class LearnerDerivation(LearnerUndefinedRunOn):
    objects = LearnerDerivationManager()
    class Meta:
        proxy = True
            
#////////////////////////////////////////////////////////////
# Data Structure for Webster Collegiate Dictionary 
#////////////////////////////////////////////////////////////  

class CollegiateEntry(models.Model):
    entry_id = models.CharField(max_length=100, primary_key=True)#<entry>
    entry_word = models.CharField(max_length=30) #<ew> 
    headword = models.CharField(max_length=30) #<hw> may contain *
    #hw_status_label = models.CharField(max_length=40, blank=True, null=True) #<hsl> head word status label, "US" or "chiefly US."
    pronunciation = models.CharField(max_length=100, blank=True, null=True) #<pr> may have multiple pronuanciations, noun, verb, B.E.
    pron_dig = models.CharField(max_length=40, blank=True, null=True) #<pr mode="dig">
    pron_pr = models.CharField(max_length=40, blank=True, null=True) #<pr mode="pr">
    #alt_pron = models.CharField(max_length=40, blank=True, null=True)#<altpr> sense pronunciation 
    function = models.CharField(max_length=30, blank=True, null=True) #<fl> function lable. slightly different from part of speech in COCA, which doesn't have geographic name
    etymology = models.CharField(max_length=600, blank=True, null=True) #<et>
    label = models.CharField(max_length=500, blank=True, null=True) #<lb> e.g. always/usually/not used before a noun and not used in progressive tenses
    status_label =  models.CharField(max_length=30, blank=True, null=True)#<sl> very rare. 
    raw = models.TextField(blank=True, null=True)
    def __unicode__(self):
        return self.entry_id
        
    @classmethod
    def find(CE,word):
        """docstring for find"""
        pass
            
class CollegiateVariant(models.Model):
    root_entry = models.ForeignKey(CollegiateEntry, related_name='variants', on_delete=models.CASCADE)
    label = models.CharField(max_length=40, blank=True, null=True)#<vl>
    form = models.CharField(max_length=40)#<va>
    pronunciation = models.CharField(max_length=100, blank=True, null=True) #<pr> may have multiple pronuanciations, noun, verb, B.E.
    def _get_headword(self):
        """docstring for get_headword"""
        pass
    headword=property(_get_headword)        
        
class CollegiateInflection(models.Model):
    root_entry = models.ForeignKey(CollegiateEntry, related_name='inflections', on_delete=models.CASCADE)
    label = models.CharField(max_length=40, blank=True, null=True)#<vl>
    form = models.CharField(max_length=40)#<va>
    pronunciation = models.CharField(max_length=40, blank=True, null=True) #<pr> may have multiple pronuanciations, noun, verb, B.E.
    def _get_headword(self):
        """docstring for get_headword"""
        pass
    headword=property(_get_headword)
      
class CollegiateCrossEntry(models.Model):
    root_entry = models.ForeignKey(CollegiateEntry, related_name='crossentry', on_delete=models.CASCADE)
    label = models.CharField(max_length=40, blank=True, null=True)#<cl>
    target = models.CharField(max_length=40)#<ct>
    def _get_headword(self):
        """docstring for get_headword"""
        pass
    headword=property(_get_headword)

class CollegiateDefinition(models.Model):#may contain several <dt>, seperate by <sd> sense driver. see "number".
    root_entry = models.ForeignKey(CollegiateEntry, related_name='definitions', on_delete=models.CASCADE)
    status_label =  models.CharField(max_length=30, blank=True, null=True)#<sl> status/subject label. US, techinical, etc.
    date = models.CharField(max_length=30, blank=True, null=True)#<dt>
    
    #///////
    #below properties are sense specific, but not in <dt> tag
    #//////////
    sense = models.CharField(max_length=10, blank=True, null=True)#<sn>
    sense_parenthesis = models.CharField(max_length=10, blank=True, null=True)#<snp>
    sense_pronunciation = models.CharField(max_length=40, blank=True, null=True)#<sp> sense pronunciation 
    sense_label = models.CharField(max_length=500, blank=True, null=True) #<slb> sense specific label, e.g. always/usually/not used before a noun and not used in progressive tenses
    sense_etymology = models.CharField(max_length=600, blank=True, null=True) #<set>
    sense_status_label = models.CharField(max_length=40, blank=True, null=True) #<ssl> sense status label, "US" or "chiefly US."
    verb_label = models.CharField(max_length=40, blank=True, null=True) #<vt> transitive verb, etc.
    sense_order = models.IntegerField() #order of sense in an entry
    
    #/////////////////
    #in <dt> tag below
    #/////////////////
    text = models.CharField(max_length=500, blank=True, null=True)
    
    def _get_headword(self):
        """docstring for get_headword"""
        pass
    headword=property(_get_headword)
                
class CollegiateSenseSynonym(models.Model):#<sx> this should be include in the definition
    root_def = models.ForeignKey(CollegiateDefinition, related_name='synonyms', on_delete=models.CASCADE)    
    sense = models.CharField(max_length=10, blank=True, null=True) 
    target = models.CharField(max_length=40)#<ct>
    def _get_root_entry(self):
        """docstring for get_root_entry"""
        pass
    root_entry = property(_get_root_entry)
    
class CollegiateSenseVariant(models.Model):
    root_definition = models.ForeignKey(CollegiateDefinition, related_name='variants', on_delete=models.CASCADE)
    label = models.CharField(max_length=40, blank=True, null=True)#<vl>
    form = models.CharField(max_length=40)#<va>
    pronunciation = models.CharField(max_length=100, blank=True, null=True) #<pr> may have multiple pronuanciations, noun, verb, B.E.
    paragraph_label = models.CharField(max_length=100, blank=True, null=True) #<spl>
    
    def _get_headword(self):
        """docstring for get_headword"""
        pass
    headword=property(_get_headword)   
    
class CollegiateSenseInflection(models.Model):
    root_definition = models.ForeignKey(CollegiateDefinition, related_name='inflections', on_delete=models.CASCADE)
    label = models.CharField(max_length=40, blank=True, null=True)#<il>
    form = models.CharField(max_length=40)#<if>
    pronunciation = models.CharField(max_length=100, blank=True, null=True) #<pr> may have multiple pronuanciations, noun, verb, B.E.
    paragraph_label = models.CharField(max_length=100, blank=True, null=True) #<spl>
    def _get_headword(self):
        """docstring for get_headword"""
        pass
    headword=property(_get_headword)    

class CollegiateIllustration(models.Model):
    root_def = models.ForeignKey(CollegiateDefinition, related_name='illustrations', on_delete=models.CASCADE)
    text = models.CharField(max_length=200, blank=True, null=True)
    def _get_root_entry(self):
        """docstring for get_root_entry"""
        pass
    root_entry = property(_get_root_entry)
    
    def _get_headword(self):
        """docstring for get_headword"""
        pass
    headword=property(_get_headword)
     
class CollegiateSenseUsageNote(models.Model):  
    root_def = models.ForeignKey(CollegiateDefinition, related_name='usage_note', on_delete=models.CASCADE)
    text = models.CharField(max_length=200, blank=True, null=True)
    def __unicode__(self):
         return self.text
         
class CollegiateSenseUsageNoteIllustration(models.Model):
    root_note = models.ForeignKey(CollegiateSenseUsageNote, related_name='illustrations', on_delete=models.CASCADE)
    text = models.CharField(max_length=200, blank=True, null=True)
    def __unicode__(self):
         return self.text
         
class CollegiateUndefinedRunOn(models.Model):
    root_entry = models.ForeignKey(CollegiateEntry, related_name='uros', on_delete=models.CASCADE)
    form = models.CharField(max_length=200, blank=True, null=True) #<ure> 
    pronunciation = models.CharField(max_length=100, blank=True, null=True)#<pr> 
    function = models.CharField(max_length=30, blank=True, null=True) #<fl> function lable. slightly different from part of speech in COCA, which doesn't have geographic name
    label = models.CharField(max_length=500, blank=True, null=True) #<lb> e.g. always/usually/not used before a noun and not used in progressive tenses
    status_label =  models.CharField(max_length=30, blank=True, null=True)#<sl> US, techinical, etc.
    
    def _get_headword(self):
        """docstring for get_headword"""
        pass
    headword=property(_get_headword)
       
class CollegiateUROVariant(models.Model):
    root_runon = models.ForeignKey(CollegiateUndefinedRunOn, related_name='variants', on_delete=models.CASCADE)
    label = models.CharField(max_length=40, blank=True, null=True)#<vl>
    form = models.CharField(max_length=40)#<va>
    pronunciation = models.CharField(max_length=40, blank=True, null=True) #<pr> may have multiple pronuanciations, noun, verb, B.E.
    def _get_headword(self):
        """docstring for get_headword"""
        pass
    headword=property(_get_headword)
    
class CollegiateDerivationManager(models.Manager):
    def get_queryset(self):
        return super(CollegiateDerivation, self).get_queryset().filter()
        
class CollegiateDerivation(CollegiateUndefinedRunOn):
    objects = CollegiateDerivationManager()
    class Meta:
        proxy = True

#////////////////////////////////////////////////////////////
# Data Structure for Webster Learner Dictionary Pointer Structure
#////////////////////////////////////////////////////////////  
        
class LearnerEntryPointer(models.Model):
    entry_id = models.CharField(max_length=100, primary_key=True)#<entry>
    headword = models.CharField(max_length=100, blank=True)
    pos = models.CharField(max_length=50, blank=True)
    word_pointer = models.ForeignKey(WordPointer,related_name='learner', null=True)
    derivations = models.ManyToManyField(WordPointer,related_name='learner_lemmas')
    def _get_data(self):
        return self.data_model.data
    data = property(_get_data)
    def __unicode__(self):
        return self.headword
        
class LearnerEntryData(models.Model):
    entry_id = models.CharField(max_length=100, primary_key=True)#<entry>
    headword = models.CharField(max_length=100, blank=True)
    pointer = models.OneToOneField(LearnerEntryPointer, related_name='data_model', on_delete=models.CASCADE)
    data = models.TextField(max_length=50000)
    def __unicode__(self):
        return self.headword
    
#////////////////////////////////////////////////////////////////////
# Data Structure for Collegiate Learner Dictionary Pointer Structure
#//////////////////////////////////////////////////////////////////// 

class CollegiateEntryPointer(models.Model):
    entry_id = models.CharField(max_length=100, primary_key=True)#<entry>
    headword = models.CharField(max_length=100)
    pos = models.CharField(max_length=50, blank=True)
    word_pointer = models.ForeignKey(WordPointer,related_name='collegiate', null=True)
    derivations = models.ManyToManyField(WordPointer,related_name='collegiate_lemmas')
    def _get_data(self):
        return self.data_model.data
    data = property(_get_data)
    def __unicode__(self):
        return self.headword
        
class CollegiateEntryData(models.Model):
    entry_id = models.CharField(max_length=100, primary_key=True)#<entry>
    headword = models.CharField(max_length=100)
    pointer = models.OneToOneField(CollegiateEntryPointer, related_name='data_model', on_delete=models.CASCADE)
    data = models.TextField(max_length=50000)
    def __unicode__(self):
        return self.headword

#////////////////////////////////////////////////////////////////////
# Undefined New Word Structure
#//////////////////////////////////////////////////////////////////// 

class UndefinedWordPointer(models.Model):
    word = models.CharField(max_length=100, primary_key=True)
    undefined = models.BooleanField(default=False)
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
