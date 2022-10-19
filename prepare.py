

#pdf plumber
#csv.preview
import pandas as pd
#import unicode character database
import unicodedata
#import regular expression operations
import re

#import natural language toolkit
import nltk
from nltk.corpus import words
#import our aquire
from acquire import *


#import our stopwords list
from nltk.corpus import stopwords
from copy import deepcopy


# # Note:   Be aware the following two functions need to have a section commented out after the first run details are provided within each function  
# # def lemmatizor(text,regexfilter=r'[^a-z0-9\'\s]'):
# # def stemmed(text,regexfilter=r'[^a-z0-9\'\s]'):
# #
# #





def split_apply_join(funct,listobj):
    'helperfuction letters'

    mapped=map(funct, listobj)
    mapped=list(mapped)
    mapped=''.join(mapped)
  
    return mapped






def stopfilter(text,stop_words_extend_reduce=["'"]):
    'we use symmetric difference so if a is already in stop words then it will be added to our third set else our third set will be missing it'
    #create oujr english stopwords list

    stops = set(stopwords.words('english'))
    stop_words_extend_reduce=set(stop_words_extend_reduce)
    stops=stops.symmetric_difference(stop_words_extend_reduce)

    # stops=(stops|stop_words_extend)-exclude_words
    #another way
    
    filtered=list(filter((lambda x: x not in stops), text.split()))
    filtered=' '.join(filtered)

    return filtered









def basic_clean(text,regexfilter=r'[^a-z0-9\'\s]'):
    '''   
    Filters out all special characters if you need to edit then supply a new regex filter 
    
    
    
    
    '''
    #make a copy and begin to transform it
    newtext = text.lower()

    #encode into ascii then decode
    newtext = unicodedata.normalize('NFKD', newtext)\
    .encode('ascii', 'ignore')\
    .decode('utf-8')

    #use re.sub to remove special characters
    newtext = re.sub(fr'{regexfilter}', ' ', newtext)

    
    


    return newtext

 


def tokenizer(text,regexfilter=r'[^a-z0-9\'\s]'):
    ''' 
    For a large file just save it locally
    
    
    
    
    
    '''
    newtext=basic_clean(text,regexfilter=regexfilter)
    #make ready tokenizer object
    tokenize = nltk.tokenize.ToktokTokenizer()
    #use the tokenizer
    newtext = tokenize.tokenize(newtext, return_str=True)
    return newtext





    
    
 


def stemmed(text,regexfilter=r'[^a-z0-9\'\s]'):
    '''    
      Takes text, tokenizes it, stems it
      stemfiltered=list(filter(lambda x: (len(x)>1 and len(x)<9 and x.isalpha()==True),  stemmedlist.split()))
      needs to be commented out after the first run (up to modeling)
      # stemfiltered=list(filter(lambda x: (len(x)>1 and len(x)<9 and x.isalpha()==True and (x in  total)), stemmedlist.split()))
      needs to be un commented commented
    
    
    
    
    
    
    '''
    total=list(pd.read_pickle('words.pkl'))


    
    #make ready porter stemmer object
    newtext=tokenizer(text,regexfilter=regexfilter)
    ps = nltk.porter.PorterStemmer()
    stemmedlist=split_apply_join(ps.stem,newtext)
    # since the average word lenght in English is 4.7 characters we will apply a conservative estimate and drop any word that is larger than 8 characters as it is likely not a word
    # we also recursivley took the set of all words generated then compared that to nltk.corpus.words.words() and used that list as filter this is where total comes from

    # stemfiltered=list(filter(lambda x:(len(x)>1 and len(x)<9 and x.isalpha()==True and (x in  total)), stemmedlist.split()))

    stemfiltered=list(filter(lambda x: (len(x)>1 and len(x)<9 and x.isalpha()==True),  stemmedlist.split()))
    stemfiltered=' '.join(stemfiltered)
 
    stemfiltered=basic_clean(stemfiltered,regexfilter=regexfilter)

    return stemfiltered




def lemmatizor(text,regexfilter=r'[^a-z0-9\'\s]'):
    '''    
    
      Takes text, tokenizes it, lemmatizes it
      lemmafiltered=list(filter(lambda x: (len(x)>1 and len(x)<9 and x.isalpha()==True),  lemmatized.split()))
      needs to be commented out after the first run (up to modeling)
      # lemmafiltered=list(filter(lambda x: (len(x)>1 and len(x)<9 and x.isalpha()==True and (x in  total)), lemmatized.split()))
      needs to be un commented commented
    
    
    
    
    
    '''
    total=list(pd.read_pickle('words.pkl'))
    

    #make ready the lemmatizer object
    newtext=tokenizer(text,regexfilter=regexfilter)
    wnl = nltk.stem.WordNetLemmatizer()
    lemmatized=split_apply_join(wnl.lemmatize,newtext)

    # since the average word lenght in English is 4.7 characters we will apply a conservative estimate and drop any word that is larger than 8 characters as it is likely not a word
    # we also recursivley took the set of all words generated then compared that to nltk.corpus.words.words() and used that list as filter this is where total comes from

    # lemmafiltered=list(filter(lambda x: (len(x)>1 and len(x)<9 and x.isalpha()==True and (x in  total)), lemmatized.split()))

    lemmafiltered=list(filter(lambda x: (len(x)>1 and len(x)<9 and x.isalpha()==True),  lemmatized.split()))

    lemmafiltered=' '.join(lemmafiltered)
  
    lemmafiltered=basic_clean(lemmafiltered,regexfilter=regexfilter)

    return lemmafiltered




def dictlist_super_NLP_comp(dictlist,regexfilter=r'[^a-z0-9\'\s]',stop_words_extend_reduce=["'"]):
    ''
    ndictlist=deepcopy(dictlist)
    mapper=[]
    interestingkeys=list(ndictlist.keys())
    for i in range(0,len(ndictlist)):           
            k=interestingkeys[i]
            text=ndictlist.get(k)         
            org={f'org':text}
            clean=basic_clean(text,regexfilter=regexfilter)
            cleaned=({f'cleaned':clean})
            lemmatized=lemmatizor(text,regexfilter)
            stopfilteredlemitezed=stopfilter(lemmatized,stop_words_extend_reduce=stop_words_extend_reduce)
            lemma={f'lemmatized':stopfilteredlemitezed}
            stem=stemmed(text,regexfilter)
            stopfilteredstem=stopfilter(stem,stop_words_extend_reduce=stop_words_extend_reduce)
            stemma={f'stemmed':stopfilteredstem}
            mapper.append({k:dict(**org,**cleaned,**lemma,**stemma)})              
               


  
       
    return mapper