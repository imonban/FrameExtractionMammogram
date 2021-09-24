import numpy as np
from scipy import cluster
from matplotlib import pyplot

####### Loading vectors ########
import pickle

dict_freq = pickle.load( open( "/usr0/home/gelern/nlp/mammo/dict/frames_13.p", "rb" ) )
dict_pos =  pickle.load( open( "/usr0/home/gelern/nlp/mammo/dict/pos_13.p", "rb" ) )

import operator
sorted_dict = sorted(dict_freq.items(), key=operator.itemgetter(1), reverse=True)

count = 0

frame_list = list()

###############################################################3

for l in sorted_dict :

	if( "NN" in dict_pos[l[0]] or "CC" in dict_pos[l[0]] or "CD" in dict_pos[l[0]] or  "DT" in dict_pos[l[0]] ) :
		continue
	if( l[1] <= 1 ) :
		continue

	print l[0], " freq = ", l[1],
	if( l[0] in dict_pos ) :
		print " pos = ", dict_pos[l[0]]
	else :
		print " pos = NIL"
	frame_list.append(l[0])

print count


import gensim
#model = gensim.models.Word2Vec.load('/usr0/home/gelern/nlp/mammo/models/Reports_new_norm_nonstop_bigram_5_min5_300d_augmented_100')
#model = gensim.models.Word2Vec.load('/usr0/home/gelern/nlp/mammo/models/Reports_new_refined_trigram_5_bigram_5_min5_300d')
model = gensim.models.Word2Vec.load('/usr0/home/gelern/nlp/mammo/models/Reports_new_refined_trigram_5_bigram_5_min5_300d_augmented_20')
#model = gensim.models.Word2Vec.load('/usr0/home/gelern/nlp/mammo/models/Reports_new_refined_trigram_5_bigram_5_min5_300d_augmented_20')
#model = gensim.models.Word2Vec.load('/usr0/home/gelern/nlp/mammo/models/Reports_new_refined_bigram_10_min10_300d_thresh_0.1_augmented_20')



import numpy as np
## Find mean vec #####

def find_mean(word_list) :
	mean_vec = np.zeros(300)
	count = 0
	
	for w in word_list :
		if( w in model.vocab ) :
			mean_vec += model[w]
			count += 1

	if( count > 0 ) :
		return mean_vec/count
	else :
		return mean_vec

########################################

########### Finding mean_vec for frames list #############

print "#######################################"
dict_mean = {}
mean_vec_list = list()
limit = -1
label_names = list()


unsure = "/usr0/home/gelern/nlp/mammo/data/unsure_predicates.txt"

fp = open(unsure)
print fp
contents = fp.read().splitlines()   
  
for c in contents :
	print c 

count_direct = 0

for f in frame_list :

	#if( limit >= 160 ) :
	#	break
	limit += 1

	flag = 0

	for c in contents :
		if( f.strip() == c.strip() ) :
			flag = 1
			break

	if( flag == 1 ) :
		continue

	f = f.strip()
	print limit , " = ", f
	word_list = f.split('_')

	#if( f not in model.vocab ) :
	#	continue

	#mean_vec = find_mean(word_list)

	if( f in model.vocab ) :
		mean_vec = model[f]
		count_direct += 1
	else :
		mean_vec = find_mean(word_list)	
	dict_mean[f] = mean_vec

	mean_vec_list.append(mean_vec)
	label_names.append(f)

###########################################################################

print len(label_names)
mean_vec_array = np.vstack(mean_vec_list)
tests = mean_vec_array


#plot variance for each value for 'k' between 1,10
initial = [cluster.vq.kmeans(tests,i) for i in range(1,10)]
pyplot.plot([var for (cent,var) in initial])
pyplot.show()

''' cent, var = initial[4]
#use vq() to get as assignment for each obs.
assignment,cdist = cluster.vq.vq(tests,cent)
pyplot.scatter(tests[:,0], tests[:,1], c=assignment)
pyplot.show() '''