
################ Loading CoreNLP Stanford Parser  ###############################################
import os
from stanford_corenlp_pywrapper import CoreNLP
proc = CoreNLP("parse", corenlp_jars=["/usr0/home/gelern/nlp/mammo/packages/stanford-corenlp-full-2015-04-20/*"], raw_output=True)

##############################################################################################

################### Extract seed terms for information frames through dependency parsing of VERBS/ADVERBS #########################

import nltk.data
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

report_path = '/usr0/home/gelern/nlp/mammo/data/Reports/'

unique_phrase_set = set()


############ to reverse order of joining #################
reverse_list = [ "mwe", "dep", "dobj", "xcomp", "nmod"]

count_sent = 0
count_folder = 0

#### Find if the candidate verb has a subject or object in the dependency ##############

def has_subj_or_obj( index, dep ) :

	for sublist in dep :
		if( ( "subj" in sublist[0] or "obj" in sublist[0] ) and  ( index in sublist ) ) :
			return 1
	return 0

################################################################################
		
	

############ Creating dictionary to store freq of phrases #############
dict_freq = {}
dict_pos = {}

for subfolders in os.listdir(report_path) :

	 print "folder count = ", count_folder
	 count_folder += 1

	 print subfolders 

	 for files in os.listdir(report_path+subfolders) :
                               
             fp = open(os.path.join(report_path + subfolders + "/" + files ))
	     print fp
	     data = fp.read()

	     data = ''.join(i for i in data if ord(i)<128)

	     if( subfolders == "mammo_all" or  subfolders == "mammo_body") :
	     	finding_list = re.findall(r'FINDINGS:(.*?)IMPRESSION:', data)		
        	if( finding_list ) :
			sent_list = tokenizer.tokenize(finding_list[0].strip())
		else :
			continue
	     else :
	     	sent_list = tokenizer.tokenize(data.strip())
	     
	     sent_flag = 0	     

	     #print sent_list
	     for sentence in sent_list :
    
			############## Remove irrelevant sentences ########################
		   if( not (subfolders == "mammo_all" or  subfolders == "mammo_body") ) :

	     		if( "Comparison" in sentence ) :
				sent_flag = 1
				continue
			if( sent_flag == 0 ) :
				continue

			#####################################################		

			print sentence
			count_sent += 1

			parser_out = proc.parse_doc(sentence)

			dd = parser_out['sentences'][0]
			tags = dd['pos']
			dep = dd['deps_cc']

			
			tokens = dd['tokens']
			new_tokens = list()	
			for t in tokens :
				new_tokens.append(t.lower())
			tokens = new_tokens	

			#print tags
			#print dep

			phrase_list = list()
			pos_list = list()

			############### Starting off with a list of all verbs obtained from POS tags ###################################
			candidate_verbs = list()
			unique_frames = set()
			index = 0
			while (index < len(tags)) :
				if(  "VB" in tags[index] and has_subj_or_obj (index, dep) and ( not "." in tokens[index] ) ) :
					candidate_verbs.append(index)
					unique_frames.add(tokens[index])
					if( tokens[index] not in dict_freq ) :
						dict_freq[tokens[index]] = 0
						dict_pos[tokens[index]] = tags[index]
					else :
						dict_freq[tokens[index]] += 1

					phrase_list.append(tokens[index])
					pos_list.append(tags[index])
					unique_phrase_set.add(tokens[index])
				index += 1
							
			
			##### Concatenating the VERB to build meaningful combinations ################

			for sublist in dep :
				if( not abs(sublist[1] - sublist[2]) == 1  or (tokens[sublist[1]] == "." or tokens[sublist[2]] == ".") ) :
					continue
				for c in candidate_verbs :

					if( c in sublist ) :

						relation = sublist[0]
						pos_flag = 0				

						if( (relation in reverse_list) or ( relation == "advmod" and ("NN" in tags[0] ) or  ("CD" in tags[0]) ) ) :
							clubbed = tokens[sublist[1]] + "_" + tokens[sublist[2]]
							pos_flag = 1
						else :
							clubbed = tokens[sublist[2]] + "_" + tokens[sublist[1]]

						clubbed = clubbed.lower()
						#clubbed.strip()

						if( not clubbed in dict_freq ) :
							dict_freq[clubbed] = 0
							if( pos_flag == 1 ) :
								dict_pos[clubbed] = tags[sublist[1]] + "," + tags[sublist[2]]
							else :
								dict_pos[clubbed] = tags[sublist[2]] + "," + tags[sublist[1]] 
												
						else :
							dict_freq[clubbed] += 1

						if( clubbed in phrase_list ):
							continue

						phrase_list.append(clubbed)
						if( pos_flag == 0 ) :
							pos_list.append( tags[sublist[2]] + "," + tags[sublist[1]] )
						else :
							pos_list.append( tags[sublist[1]] + "," + tags[sublist[2]] )

						
						print clubbed
						#target.write(clubbed + "\n")
						unique_phrase_set.add(clubbed) 

						
					
			########## Clubbing common parts to form n-grams once ( can be done recursively )  ####################

			#count_instance = 0
			#while ( count_instance < 3 ) :
			#	count_instance += 1
			
			first_part = list()
			last_part = list()

			for phrase in phrase_list:
				p = phrase.split('_')
				first_part.append(p[0])
				i = len(p)-1
				last_part.append(p[i])
			
			last_index = -1	

		        for l in last_part :

				last_index += 1
				first_index = -1

				for f in first_part :
					first_index += 1
					if( l == f ) :
							
						if( "_" not in phrase_list[first_index] or "," not in pos_list[first_index] ) :
							continue
						else :
							begin_index = (phrase_list[first_index]).index('_') + 1
						clubbed = phrase_list[last_index] + "_" + (phrase_list[first_index])[begin_index:]
										
							#if( clubbed in unique_phrase_set ) :
								#continue

						unique_phrase_set.add(clubbed)	
						phrase_list.append(clubbed)
						
						if( not clubbed in dict_freq ) :
							dict_freq[clubbed] = 0
							begin_index = (pos_list[first_index]).index(',') + 1
							dict_pos[clubbed] = pos_list[last_index] + "," + (pos_list[first_index])[begin_index:]

						else :
							dict_freq[clubbed] += 1

						print clubbed 
					
				 

			

			

	     #break
         #break


target = open("/usr0/home/gelern/nlp/mammo/data/raw_frames_12.txt", 'w')
	
for u in unique_phrase_set :
	target.write(u+"\n")

target.close()

target = open('/usr0/home/gelern/nlp/mammo/files/depend_12.txt','w')

print "no of sentences = ", count_sent
print "no of phrases = ", len(unique_phrase_set)

target.write( "no of sentences \n")
target.write(str(count_sent))
target.write( "\n no of phrases \n")
target.write(str(len(unique_phrase_set)))

target.close()

#############Save a dictionary into a pickle file ###################
import pickle
pickle.dump( dict_freq, open( "/usr0/home/gelern/nlp/mammo/dict/frames_12.p", "wb" ) )
pickle.dump( dict_pos, open( "/usr0/home/gelern/nlp/mammo/dict/pos_12.p", "wb" ) )

############################

