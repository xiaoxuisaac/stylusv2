from lib.ngrams import *
from stylus.models import *
from time import sleep
import random
import math
from numpy import power,arctan

def replace(ww):
    w=Word.objects.get(word=ww)
    try:
        wl=w.wordlist.all()[0]
    except:
        pass
    w.delete()
    w=Word(word=ww,ngramsfreq=0)
    w.save()
    try:
        w.wordlist.add(wl)
        w.save()
    except:
        pass

def update_ngram(words):
 words_list=[]
 easybase=6e-4
 diffbase=1e-7
 factor=10/math.log(diffbase/easybase,10)
 flag=True
 for j in range(20):
  if flag == False:
      break     
  i=0
  query = []
  words_list=[]
  for word in words:
      if Word.objects.get(word=word).ngramsfreq==None or Word.objects.get(word=word).ngramsfreq==0:
       words_list.append(Word.objects.get(word=word))
  if len(words_list)==0: break
  for word in words_list:
     if i<8:
         query.append(word.word)
     else:
         break
     i+=1
  freq_dic=Ngrams(query)
  random.shuffle(query)
  sleep(2)
  test_dic=Ngrams(query)
  for w in freq_dic:
         word=Word.objects.get(word=w)
         if freq_dic[w] == test_dic[w] and freq_dic[w]!=0:
          word.ngramsfreq=freq_dic[w]
          try:
           if float(word.ngramsfreq) > easybase:
            word.difficulty=0
            word.calc_diff=0
           else:
            word.difficulty=math.log(float(word.ngramsfreq)/easybase,10)*factor
            x=word.difficulty
            word.calc_diff=x*(arctan(x-8)+1.447)
           word.save()
          except:
              pass
          print word.word, word.ngramsfreq, word.difficulty
         else:
          print word.word, freq_dic[w], test_dic[w], "Biu!!!!!!!"
          flag = False



def update_ngram_all():
 for j in range(20000):
    query = []
    i=0
    for word in Word.objects.filter(ngramsfreq=None):
        if i<6:
            query.append(word.word)
        else:
            break
        i+=1

#    print ','.join(query)

    freq_dic=Ngrams(query)
#    print query
#    print freq_dic
    random.shuffle(query)
    sleep(5)
    test_dic=Ngrams(query)
#    print test_dic

    for w in freq_dic:
        try:
            word=Word.objects.get(word=w)
            if freq_dic[w] == test_dic[w] and freq_dic[w] != 0:
             word.ngramsfreq=freq_dic[w]
             word.save()
             print word, word.ngramsfreq
            else:
             print word, freq_dic[w], test_dic[w], "Biu!!!!!!!"
        except:
            print w

#f=0.1

#for word in Word.objects.all():
#    if word.ngramsfreq == 0 or word.ngramsfreq ==None:
#        temp=f
#        f=Ngrams(word.word)
#        if f == 0 and temp ==0:
#            print "Break!"
#            break
#        if f!=0:
#            word.ngramsfreq=f
#            print word, f
#            word.save()
#print "Done!"
