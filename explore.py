import re
import unicodedata
import pandas as pd
import nltk


from nltk.corpus import words
from wordcloud import WordCloud,ImageColorGenerator
from matplotlib_venn import venn3, venn3_circles
from matplotlib_venn_wordcloud import venn3_wordcloud

import matplotlib.pyplot as plt
import seaborn as sns




from matplotlib import pyplot as plt
import numpy as np

def wordset(df):
    dflist=list(df['stemmed'])
    dflist=' '.join(dflist)
    dflist=dflist.split()
    dflist=set(dflist)
    return dflist


def wordslist(df):
    dflist=list(df['stemmed'])
    dflist=' '.join(dflist)
    dflist=dflist.split()
    return dflist

def combinedwordlist(df_C,df_Py,df_Java):
    combined=[]
    c_wordlist=wordslist(df_C)
    combined.extend(c_wordlist)

    py_wordlist=wordslist(df_Py)
    combined.extend(py_wordlist)

    java_wordlist=wordslist(df_Java)
    combined.extend(java_wordlist)
    combined.sort()
    return combined




def combinedwordcountdf(df_C,df_Py,df_Java):
   combined=[]
   c_wordlist=wordslist(df_C)  
   py_wordlist=wordslist(df_Py)
   java_wordlist=wordslist(df_Java)

   c_wordlist.sort()
   py_wordlist.sort()
   java_wordlist.sort()

   combined.extend(c_wordlist)   
   combined.extend(py_wordlist)   
   combined.extend(java_wordlist)
   combined.sort()
   serieslist=[combined,c_wordlist,py_wordlist,java_wordlist]
   serieslist=[pd.Series(freq).value_counts() for freq in serieslist]
   word_counts_df = (pd.concat(serieslist, axis=1, sort=True)
               .set_axis(['all', 'c', 'py','java'], axis=1, inplace=False)
               .fillna(0)
               .apply(lambda s: s.astype(int)))
   return word_counts_df









  
def wordclouddict(df_C,df_Py,df_Java):
    c_words_list=wordslist(df_C)
    py_words_list=wordslist(df_Py)
    java_words_list=wordslist(df_Java)

    c_words_list=' '.join(c_words_list)
    py_words_list=' '.join(py_words_list)
    java_words_list=' '.join(java_words_list)

    langlists=[c_words_list,
    py_words_list,
    java_words_list]


    landdict=dict(zip(['c','py','java'],langlists))

    return   landdict


def wordclouds(df_C,df_Py,df_Java):
    landdict=wordclouddict(df_C,df_Py,df_Java)
    for i in list(landdict.keys()):
        x=landdict.get(i)
        img = WordCloud(background_color='black',collocations=False).generate(x)
        # WordCloud() produces an image object, which can be displayed with plt.imshow
        plt.imshow(img)
        # axis aren't very useful for a word cloud
        plt.axis('off')
        plt.title(f'Word Cloud for {i}')
        plt.show()
