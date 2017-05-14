import sys
import os
import unicodecsv as csv
from lexicon.models import LearnerRaw, CollegiateRaw, CocaFreq, CocaDict, WordPointer, Ngrams
import string
import random
from collegiate_api_query import add_collegiate
from learner_api_query import add_learner

csv.field_size_limit(sys.maxsize)

def export():
    export_learner()
    print('\n')
    export_collegiate()
    print('\n')
    export_ngrams()

def export_learner():
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    print("Exporting Webster Learner Dictionary Data...")
    os.rename(os.path.join(__location__,'raw_data/learner.csv'),os.path.join(__location__,'raw_data/learner_'+id_generator(4)+'.csv'))
    with open(os.path.join(__location__,'raw_data/learner.csv'), 'wb+') as csvfile:
        learnerwriter = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        i = 0
        n =LearnerRaw.objects.all().count()
        for raw in LearnerRaw.objects.all():
            i+=1
            if i % 100 == 0:
                p =i*100.0/n
                sys.stdout.write("\r%.1f%%" % p)
                sys.stdout.flush()
            learnerwriter.writerow([raw.alpha, raw.data])

def export_collegiate():
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))        
    print("Exporting Webster Collegiate Dictionary Data...")
    os.rename(os.path.join(__location__,'raw_data/collegiate.csv'),os.path.join(__location__,'raw_data/collegiate_'+id_generator(4)+'.csv'))
    with open(os.path.join(__location__,'raw_data/collegiate.csv'), 'wb+') as csvfile:
        collegiatewriter = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        i = 0
        n =CollegiateRaw.objects.all().count()
        for raw in CollegiateRaw.objects.all():
            i+=1
            if i % 100 == 0:
                p =i*100.0/n
                sys.stdout.write("\r%.1f%%" % p)
                sys.stdout.flush()
            collegiatewriter.writerow([raw.alpha, raw.data])
 
def export_ngrams():
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))        
    print("Exporting Google Ngrams Data...")
    os.rename(os.path.join(__location__,'raw_data/ngrams.csv'),os.path.join(__location__,'raw_data/ngrams_'+id_generator(4)+'.csv'))
    with open(os.path.join(__location__,'raw_data/ngrams.csv'), 'wb+') as csvfile:
        nrgamswriter = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        i = 0
        n =Ngrams.objects.all().count()
        for ngrams in Ngrams.objects.all():
            i+=1
            if i % 100 == 0:
                p =i*100.0/n
                sys.stdout.write("\r%.1f%%" % p)
                sys.stdout.flush()
            nrgamswriter.writerow([ngrams.word, float(ngrams.raw_freq)])                   
#////////////////////////////////////////////////////////////
# Import Each Dataset
#//////////////////////////////////////////////////////////// 
def import_all():
    import_learner()
    import_collegiate()
    import_coca()
    import_ngrams()

def import_learner():
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    print("Importing Webster Learner Dictionary Data...")
    with open(os.path.join(__location__,'raw_data/learner.csv'), 'r') as csvfile:
       learnerwriter = csv.reader(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
       data = list(learnerwriter)
       n = len(data)
       i = 0
       for row in data:
           i+=1
           if i % 100 == 0:
               p =i*100.0/n
               sys.stdout.write("\r%.1f%%" % p)
               sys.stdout.flush()
               
           raw, created = LearnerRaw.objects.get_or_create(alpha=row[0].lower())
           if(created):
               #print("New Word: "+row[0].lower())
               raw.data=row[1]
               raw.save()
               add_learner(raw.alpha)
               
def import_collegiate():
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    print("Importing Webster Collegiate Dictionary Data...")
    with open(os.path.join(__location__,'raw_data/collegiate.csv'), 'r') as csvfile:
       collegiatewriter = csv.reader(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
       data = list(collegiatewriter)
       n = len(data)
       i = 0
       for row in data:
           i+=1
           if i % 100 == 0:
               p =i*100.0/n
               sys.stdout.write("\r%.1f%%" % p)
               sys.stdout.flush()
               
           raw, created = CollegiateRaw.objects.get_or_create(alpha=row[0].lower())
           if(created):
               raw.data=row[1]
               raw.save()
               add_collegiate(raw.alpha)

def import_coca(number = 1000000):
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    print("Importing COCA Data...")
    with open(os.path.join(__location__,'raw_data/coca.csv'), 'rU') as csvfile:
        cocawriter = csv.reader(csvfile, dialect=csv.excel_tab)
        data = list(cocawriter)
        n = len(data)
        for row in data:
            if int(row[0]) > number: break
            if int(row[0]) % 100 == 0:
                i =int(row[0])*100.0/n
                sys.stdout.write("\r%.1f%%" % i)
                sys.stdout.flush()
            try:
                coca = CocaFreq.objects.get(rank=int(row[0]))
            except:
                coca = CocaFreq(rank=int(row[0]))
                coca.headword = row[1].lower()
                word_pointer,created = WordPointer.objects.get_or_create(word=coca.headword)
                coca.word_pointer = word_pointer
                coca.lemma = row[2].lower()
                word_pointer,created = WordPointer.objects.get_or_create(word=coca.lemma)
                coca.lemma_pointer = word_pointer
                coca.pos = row[3]
                try:
                    coca.cap_freq = float(row[4])
                except:
                    pass
                if row[5]!= '  ': coca.us_uk = row[5]
                coca.raw_freq = int(row[7])
                #print row[8:26]
                coca.freq_dict = add_coca_dict(row[8:26])
                #print row[27:45]
                coca.text_dict = add_coca_dict(row[27:45])
                #print [row[7]]+row[46:63]
                coca.raw_freq_dict = add_coca_dict([row[7]]+row[46:63])
                #print row[64:]
                coca.raw_text_dict = add_coca_dict(row[64:])
                coca.save()
                coca.word_pointer.update_lemmas()
                coca.word_pointer.save()
                
def add_coca_dict(data):
    d = CocaDict()
    d.coca=float(data[0])
    d.bnc=float(data[1])
    d.soap=float(data[2])
    d.y1950_89=float(data[3])
    d.y1900_49=float(data[4])
    d.y1800s=float(data[5])
    d.coca_spok=float(data[6])
    d.coca_fic=float(data[7])
    d.coca_mag=float(data[8])
    d.coca_news=float(data[9])
    d.coca_acad=float(data[10])
    d.bnc_spok=float(data[11])
    d.bnc_fic=float(data[12])
    d.bnc_mag=float(data[13])
    d.bnc_news=float(data[14])
    d.bnc_noAc=float(data[15])
    d.bnc_acad=float(data[16])
    d.bnc_misc=float(data[17])
    d.save()
    return d
 
def import_ngrams():
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    print("Importing Google Ngrams Data...")
    with open(os.path.join(__location__,'raw_data/ngrams.csv'), 'r') as csvfile:
       ngramswriter = csv.reader(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
       data = list(ngramswriter)
       n = len(data)
       i = 0
       for row in data:
           i+=1
           if i % 100 == 0:
               p =i*100.0/n
               sys.stdout.write("\r%.1f%%" % p)
               sys.stdout.flush()
               
           ngrams, created = Ngrams.objects.get_or_create(word=row[0].lower())
           ngrams.raw_freq=row[1]
           ngrams.save()
           if(created):
               ngrams.raw_freq=row[1]
               wp, created = WordPointer.objects.get_or_create(word=row[0].lower())
               ngrams.word_pointer = wp
               ngrams.save()
               if created: print wp
               
#////////////////////////////////////////////////////////////
# Utilities
#//////////////////////////////////////////////////////////// 

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
