import gensim
import logging
import os
import string
import nltk.data
#from nltk.corpus import stopwords

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

#stopset = set(stopwords.words('english'))
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

class MySentences(object):
     def __init__(self, dirname):
         self.dirname = dirname
 
     def __iter__(self):
       for subdirname in os.listdir(self.dirname): 
         prefix = self.dirname+subdirname
         print prefix
         for fname in os.listdir( prefix ):
             
             fp = open(os.path.join(prefix, fname))
             #print os.path.join(prefix, fname)
             data = fp.read()
             sent_list = tokenizer.tokenize(data)
             #stopset = set(stopwords.words('english'))


	     for sent in sent_list :
    
    		exclude = set(string.punctuation)
    		cleaned_sent = ''.join(ch for ch in sent if ch not in exclude)
   		cleaned_lower_sent = cleaned_sent.lower()
    		sent_tokens = cleaned_lower_sent.split()
		final_tokens = [ x.lower() for x in sent_tokens if ( not x.isdigit() ) ]
                yield final_tokens
        

                 
sentences = MySentences('/usr0/home/gelern/nlp/mammo/data/Reports/') 
 

#bigram_transformer = gensim.models.Phrases(sentences, min_count = 5)
#model = gensim.models.Word2Vec(bigram_transformer[sentences], min_count = 5, workers = 32)

model = gensim.models.Word2Vec(sentences, min_count = 5, workers = 32, size = 300)
model.save('/usr0/home/gelern/nlp/mammo/models/unigram_min5_300d')



