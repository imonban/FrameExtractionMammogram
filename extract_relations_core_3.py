import re
import pickle
import string
################ Loading Stanford Parser from NLTK ################################
import os
from stanford_corenlp_pywrapper import CoreNLP
proc = CoreNLP("parse", corenlp_jars=["/usr0/home/gelern/nlp/mammo/packages/stanford-corenlp-full-2015-04-20/*"], raw_output=True)


##############################################################################################


##########################################################

###### Load Stanford Tokeniser #################
from nltk.tokenize.stanford import StanfordTokenizer



####################### Constructing Phrase List ########################################

folder_path = '/usr0/home/gelern/nlp/mammo/dict/8_classes_others/'
dict_folder_name = {}
folder_names = list()
phrase_list = list()

for subfolders in os.listdir(folder_path) :

	#print subfolders
        #print "\n"
	name = subfolders.lower()
	folder_names.append(name)
	
	
	for files in os.listdir( folder_path + subfolders ) :
		#print files
		fp = open(os.path.join(folder_path + subfolders + "/" + files ))
		data = fp.readlines()

		for phrase in data :
			#print phrase
			phrase = phrase.lower()				
			#exclude = set(string.punctuation)			               
    			#phrase = ''.join(ch for ch in phrase if ch not in exclude)
			phrase = phrase.strip()
			if( phrase == "" or phrase == " " ) :
				continue

			#phrase = phrase.replace(' ', '_' )
			phrase = " ".join(phrase.split())
				
			#print phrase		
			if( phrase in phrase_list ) :	
				continue
			else :
				#print phrase
				phrase_list.append(phrase)
				#folder_list.append(phrase)
				#folder_list.append(subfolders.lower())
				dict_folder_name[phrase] = name
				



####### Return true if the string consists of a numerical unit ######

def find_num( tokens, index ) :
	
	ans = tokens[index]

	while(1) :
	     index -= 1
	     if( index < 0 ) :
		return ans
	
	     if( tokens[index] == " " ):
		continue

	     if( contains_digits(tokens[index]) or tokens[index] == "X" or tokens[index] == "x" ) :
			ans = tokens[index] + " " + ans
	     else :
		return ans

	
####### check if a string has atleast one digit ###################		
_digits = re.compile('\d')
def contains_digits(d):
    return bool(_digits.search(d))		
	
####### Return the numerical quantity from a string ######

def is_numerical_unit( word ) :
	
	
	unit_list = [ " cm", " mm", "clock", " c.m."]
	for i in unit_list :
		if( i in word ) :
			return 1
	return 0



####### Return true if current list elements are already present in one of the group of lists ######

def is_same( subject_list, group_of_lists ) :
	
	for group in group_of_lists :

		count = 0 
		for ele in subject_list :
			if( ele in group ) :
				count += 1

		if( count == len(subject_list ) ):
			return 1

	return 0
				


##### Check if given word is a coref word ####################

def is_coref_word ( word ) :

	coref_list = ["this", "that", "it", "these", "those", "which" ]
	if( word in coref_list ) :
		return 1
	return 0

###### Defining a class to store attributes in a relation and denote relation name with a boolean flag ##########################################
class Char_value(object):
    def __init__(self,name,relation_flag):
       self.name=name
       self.relation_flag=relation_flag

    def __eq__(self, n):
    	return ( self.name == n  )

##################### Sort Phrase_list according to the number of words in the phrases ##################
phrase_list.sort(key=lambda x: ( len(x.split()), len(x) ) , reverse=True)
#####################################################################################

def find_compound( subject_index, dep, tokens, compound_list, compound_index_list, subject_list ) :

	repeat_list = set()
	for sublist in dep :

		index = 1
				

		if( sublist[0] == "compound" or sublist[0] == "conj:and" or sublist[0] == "conj:or" ) :
			clubbed = tokens[sublist[2]]+" "+ tokens[sublist[1]]
			index = 2

		elif( sublist[0] == "advmod" ) :
			clubbed = tokens[sublist[1]]+" "+ tokens[sublist[2]]	
		else :
			continue		
			
		if( clubbed in repeat_list or tokens[sublist[2]] == tokens[sublist[1]] or (
		    (tokens[sublist[2]] in dict_folder_name and dict_folder_name[tokens[sublist[2]]] in exclude_class_list) or
                    (tokens[sublist[1]] in dict_folder_name and dict_folder_name[tokens[sublist[1]]] in exclude_class_list) and has_abnormality(subject_list) ) ) :
			continue

		repeat_list.add(clubbed)
		print "compound = ", clubbed
	
		if( is_numerical_unit(clubbed) or clubbed in dict_folder_name ) :
			print "appending in compound list = " , clubbed
			compound_list.append(clubbed)
			compound_index_list.append(sublist[index])

		else :

			string_1 = tokens[sublist[1]]
			if( sublist[1] in ann_dict ) :
				string_1 = ann_dict[sublist[1]]

			print "appending = " , string_1

			compound_list.append(string_1)
			compound_index_list.append(sublist[1])

			string_2 = tokens[sublist[2]]
			if( sublist[2] in ann_dict ) :
				string_2 = ann_dict[sublist[2]]


			print "appending = " , string_2, " index = ", sublist[2]

			compound_list.append(string_2)
			compound_index_list.append(sublist[2])



################ Check if the subject list till now has an abonormality in it or not ##########################3
def has_abnormality(subject_list) :
	
	for i in subject_list :
		if( i in dict_folder_name and 
		     ( dict_folder_name[i] == "is_abnormality"  or dict_folder_name[i] == "breastdensity" or dict_folder_name[i] == "specialcase" ) ) :

		    #( dict_folder_name[i] == "is_abnormality" or dict_folder_name[i] == "specialcase" or dict_folder_name[i] == "breastdensity") ) :
			return 1

	return 0


############################################################################################################	

############# Print attributes of subject ######################

exclude_class_list = [ "is_abnormality", "breastdensity", "are_others", "specialcase"]

def attributes( init_index, dep, related, root_index, subject_list, negation_list, subject_indices, rel_indices ) :


	print "init index = " , init_index

	if( not init_index in phrase_ann_index ) :
		print "return = ",init_index
		return

	
	phrase_index = phrase_ann_index[init_index]
	list_offset = phrase_ann_list[phrase_index]
	
	begin = list_offset[0]
	end = list_offset[1]

	list_of_indices = list()

	while (begin <= end) :
		list_of_indices.append(begin)
		begin += 1

	#print list_of_indices
	#related = list()

	list_of_recurs = list()
	

	for sublist in dep :

		#if( "subj" in sublist[0] ) :
		#	continue

		
		
			
		if( sublist[1] in list_of_indices or sublist[2] in list_of_indices) :
			if( sublist[1] in list_of_indices and sublist[2] in list_of_indices) :
				continue
			if( sublist[1] in list_of_indices ) :
				index = 2
			else :
				index = 1
			
			if( "neg" in sublist[0] ) :
				negation_list.append( "present" )

			#if( sublist[index] in rel_indices ) :
			#	continue

			#print sublist[0], " and ", sublist[2], " and ", sublist[1]

			 

			if( sublist[index] in ann_dict ) :
				words = ann_dict[sublist[index]]
				repeat_flag = 0
				

				print "words = " , words
				#for r in repeat :
				#	if( words == r ) :
				#		repeat_flag = 1
				#		break
				#if( repeat_flag == 1 ) :
				#	continue
				if( not words in related ) :
				    
					
				        root_word = ann_dict[root_index]
					is_main = 0
					#print "root = ", root_word , " type = ", dict_folder_name[root_word]
					#if( not dict_folder_name[root_word] == "of_type" and not sublist[0] == "cc" and not sublist[0] == "conj:and" ) :

					for c in exclude_class_list :
						if( c == dict_folder_name[root_word] ) :
							is_main = 1

					if( not dict_folder_name[root_word] == "of_type" and is_main ) :
						if( dict_folder_name[words] in exclude_class_list ) :
								repeat_flag = 1
								
					#print "****" , dict_folder_name[root_word]
					if( (repeat_flag == 1 and not "subj" in sublist[0]) and has_abnormality(subject_list)  ) :
						print "repeat", " and ", sublist[0]
						continue						
					
					if( ("subj" in sublist[0] or "obj" in sublist[0]) and subject_list[0] == "NIL" ) :
						subject_list.append(words)
						subject_indices.append(sublist[index])
						#if( words == "NIL" ) :
							#print "ADDED NIL "

					print "## appending ", words, " by ", sublist[0], " with index = ", sublist[index]
					if( words not in subject_list and not sublist[index] in rel_indices ) :
						print "appending = ", words, " with index = ", sublist[index]
						subject_list.append(words)
						subject_indices.append(sublist[index])

						
					
						
					print "class = ", dict_folder_name[words] 

					related.append(words)
					list_of_recurs.append(sublist[index])

	for i in list_of_recurs :
		print "checking for ", i
		attributes(i, dep, related, root_index, subject_list, negation_list, subject_indices, rel_indices ) 
	


	

###### Clear numbers in a sentence and replace with x #######
def clearup(s, chars):
    return re.sub('[%s]' % chars, 'x', s).lower()


#### check if relation consists of negation words no, not #####
def is_negation(sublist, tokens) :
   neg_list = [ "no", "not" ]
	
   for n in neg_list :
	if( n == tokens[sublist[1]] or  n == tokens[sublist[2]] ) :
		return 1

   return 0
	
		


################# Extract seed terms for information frames through dependency parsing of VERBS/ADVERBS #########################

import nltk.data
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

report_path = '/usr0/home/gelern/nlp/mammo/data/Reports/'

unique_phrase_set = set()



############ to reverse order of joining #################
reverse_list = [ "mwe", "dep", "dobj", "xcomp"]

count_sent = 0
count_folder = 0

############ Creating dictionary to store freq of phrases #############
dict_freq = {}
dict_pos = {}


########### Constructing filtered frames list #############

			
#frame_file = '/usr0/home/gelern/nlp/mammo/data/raw_frames_11.txt'
frame_list = list()

dict_freq = pickle.load( open( "/usr0/home/gelern/nlp/mammo/dict/frames_13.p", "rb" ) )
dict_pos =  pickle.load( open( "/usr0/home/gelern/nlp/mammo/dict/pos_13.p", "rb" ) )

unwanted = [ "of_clustered", "of_scattered", "do", "remaining", "obscure", "could_obscure"]
	
import operator
sorted_dict = sorted(dict_freq.items(), key=operator.itemgetter(1), reverse=True)
			
for l in sorted_dict :

	if( l[0] in unwanted or ( l[0] in phrase_list and not dict_folder_name[l[0]] == "are_others" ) ) :
		print "removing ", l[0]
		continue

	if( "NN" in dict_pos[l[0]] or "CC" in dict_pos[l[0]] or "CD" in dict_pos[l[0]] or  "DT" in dict_pos[l[0]] ) :
		continue
	
	name = l[0]
	name = name.replace("_", " ")

	#if( name in dict_folder_name and not dict_folder_name[name] == "are_others") :
	#	print "exclude = ", name, " class = ", dict_folder_name[name]
	#	continue

	frame_list.append(name)

			
##################### Sort frame_list according to the number of words in the frames ##################
frame_list.sort(key=lambda x: len(x.split()), reverse=True)
###########################################################################	



for subfolders in os.listdir(report_path) :

	 if( subfolders == "new" ) :
		continue

	 if( not subfolders == "P7230" ) :
		continue

	
	 print "folder count = ", count_folder
	 count_folder += 1

	 print subfolders 

 
	 obs_list = []
	 ### Storing list of characteristics for each observation ######
	 char_list = {}
	 common_index = {}

	 for files in os.listdir(report_path+subfolders) :
                            
	     if( not files == "1.txt" ) :
		continue
   
             fp = open(os.path.join(report_path + subfolders + "/" + files ))
	     print fp
	     data = fp.read()
	     sent_list = tokenizer.tokenize(data.strip())

	     sent_flag = 0

	     #print data
	     prev_subject = "NIL"
	     prev_subject_index = -1
	     
	     group_of_lists = []
	     sent_offset = 0
	     

	     for sentence in sent_list :
    
			
			############## Remove irrelevant sentences ########################
	     		''' if( "Comparison" in sentence ) :
				sent_flag = 1
				continue
			if( sent_flag == 0 ) :
				continue '''

			#####################################################		

			count_sent += 1
			

			############### Copy setences to a file to run the Parsing Algo #############################
			#print "sent = " , sentence

			#### remving extra white spaces #####
			sentence = " ".join(sentence.split())
			sentence = sentence.lower()
			new_sent = clearup(sentence, string.digits)
			#new_sent = sentence

			print sentence
			count_sent += 1
			new_sent_flag = 1
			prev_flag = 0

			parser_out = proc.parse_doc(sentence)

			dd = parser_out['sentences'][0]
			tags = dd['pos']
			dep = dd['deps_cc']

			sentence = new_sent
			#print dep 
			print tags
			tokens = dd['tokens']
			new_tokens = list()	
			for t in tokens :
				new_tokens.append(t.lower())
			tokens = new_tokens			
						
			
			subj_list = list()
			obj_list = list()

				

			#word_list = sentence.split()
			new_sent = sentence.lower()
			print new_sent
			rel_frame_list = list()
			#repeat_frame = list()

			print "len of frame list ", len(frame_list)
			#for f in frame_list :
			#	if( "present" in f ) :
   			#		print f

			begin_index_list = list()
			end_index_list = list()

			##### storing frame offsets found in the sentence #########
			for f in frame_list :				

				f = f.replace("_", " ")
				list_of_indices = [m.start() for m in re.finditer(f, new_sent)]
				if( len(list_of_indices) == 0 ) :
					continue


				list_index = 0

				#print f

				while( list_index < len(list_of_indices) ) :

					
					#print list_index
					target_index = list_of_indices[list_index] 
					curr_index = list_index
					list_index += 1
	
					
					flag = 0			
					if( not( (target_index-1 < 0 or new_sent[target_index-1]  == " " or new_sent[target_index-1]  == "." ) and 
				          (target_index+len(f) >= len(new_sent) or new_sent[target_index+len(f)] == " " or new_sent[target_index+len(f)] == "." ) )  ) :
				   		continue						

                                        

					for i in range(len(begin_index_list)) :
						if( (target_index >= begin_index_list[i] and target_index <= end_index_list[i]) or 
					    	(target_index+len(f) >= begin_index_list[i] and target_index+len(f) <= end_index_list[i]) ) :
							flag = 1

					if( flag == 1 ) :
						continue

				
					begin_index_list.append( target_index )
					end_index_list.append( target_index + len(f) - 1 )


					#if( f in repeat_frame ) :
					#	continue
					#repeat_frame.append(f)
					pos = list_of_indices[curr_index]
					subsent = sentence[:pos]
					num_spaces = subsent.count(' ')
					frame_offset_begin = num_spaces 
					frame_offset_end = num_spaces + f.count(' ') 

					#print frame_offset_begin
					#print frame_offset_end
				
					new_list = list()
					new_list.append(frame_offset_begin)
					new_list.append(frame_offset_end)
				
					#print f
			
					rel_frame_list.append(new_list)
					

			phrase_ann_list = list()
			phrase_ann_index = {}
			ann_dict = {}
			

			phrase_index = -1
			##### storing phrase offsets found in the sentence #########
			for p in phrase_list :

				
				p = p.replace("_", " ")
				list_of_indices = [m.start() for m in re.finditer(p, new_sent)]
				if( len(list_of_indices) == 0 ) :
					continue

				#print (list_of_indices)
				list_index = 0
				while ( list_index < len(list_of_indices) ) :
					
					pos = list_of_indices[list_index] 
					
					list_index += 1


					if( not( (pos-1 < 0 or new_sent[pos-1]  == " " or new_sent[pos-1]  == "." ) and 
				          (pos+len(p) >= len(new_sent) or new_sent[pos+len(p)] == " " or new_sent[pos+len(p)] == "." ) )  ) :
				   		continue 

					phrase_index += 1
					#print list_index
					
					#list_index += 1
					subsent = new_sent[:pos]
					num_spaces = subsent.count(' ')
					phrase_offset_begin = num_spaces 
					phrase_offset_end = num_spaces + p.count(' ') 

		
					#print phrase_offset_begin
					#print phrase_offset_end
				
					new_list = list()
					new_list.append(phrase_offset_begin)
					new_list.append(phrase_offset_end)
			
					phrase_ann_list.append(new_list)
				
					begin_index = phrase_offset_begin 
					if ( begin_index in ann_dict ) :
						continue
					
					#print p
					#print begin_index , " and ", phrase_offset_end
					init_index = begin_index
					while begin_index <= phrase_offset_end :
                                                
						ann_dict[begin_index] = p
						common_index[begin_index] = init_index
						phrase_ann_index[begin_index] = phrase_index								
						begin_index += 1		


		
			#print tokens
			
                        
                      

			for rel in rel_frame_list :
			
				dep_index = -1
				rel_indices = list()

				#print "yooooo prev = ", prev_subject
				print "rel = ", rel

				#### If it is a single word relation and not a verb then continue #####
				if( rel[0] == rel[1] ) :
					#print "yes"
					if( not "VB" in tags[rel[0]] ) :
						#print "yooooo3 prev = ", prev_subject
						continue

				
				#### print relation #####
				print "Relation = ",
				start_index = rel[0]

				 
				relation_name = ""
				while start_index <= rel[1] :
					print tokens[start_index],
					relation_name += tokens[start_index] + " "
					rel_indices.append(start_index)
					start_index += 1
					

				flag = 0
				for obs_index in obs_list :
					for ch in char_list[obs_index] :
						if( not ch.relation_flag == 1 and ( relation_name in ch.name and len(relation_name)  > 5 ) ) :
							flag = 1

				if( flag == 1 ) :
					continue


				print rel_indices
				print ""
				subject = "NIL"
				subject_index = -1
				object = "NIL"
				negation = "NIL"
				modifier = "NIL"
				other = "NIL"
				modifier_index = -1
				other_index = -1

				
				negation_list = list()
				object_list = list()
				other_list = list()


				neg_flag = 0					
				coref_flag = 0

				for sublist in dep :
					

					if( not ( sublist[2] in rel_indices or sublist[1] in rel_indices ) ) :
						continue

					if( sublist[2] in rel_indices and sublist[1] in rel_indices ) :
							continue

					if(  ("neg" in sublist[0] ) or is_negation(sublist, tokens) ) :
						neg_flag = 1
	
					
					#if( ( ("subj" in sublist[0] ) or ("obj" in sublist[0] ) or ("mod" in sublist[0] ) or (neg_flag == 1) ) ) :
					if(1) :
						

						if( neg_flag == 1 ) :
							negation = "PRESENT"
							negation_list.append( "PRESENT")
						

						#### store subject or object by referring phrase_ann_list ########
						if( sublist[1] in rel_indices ) :
							target_index = sublist[2]
						else :
							target_index = sublist[1]

					        #print "Subject = ", tokens[target_index]
						#print target_index
						
						if( "subj" in sublist[0] ) :


							if( target_index in ann_dict ) :
								subject = ann_dict[target_index]
								
								
							else :
								#print "yo", tokens[target_index]
								subject = tokens[target_index]
								#coref_flag = 1

							#prev_subject = subject
							#prev_subject_index = target_index
							subject_index = target_index
							print " subject = ", subject, " at index = ", subject_index
							#if( subject not in subject_list ) :
							#	subject_list.append(subject)

					
						if( ("obj" in sublist[0])  ) :
							if( target_index in ann_dict ) :
								object = ann_dict[target_index]
								prev_object = object
						        else :
								object = tokens[target_index]

							object_index = target_index
							if( object not in object_list ) :
								object_list.append(object)
							

						if( ("mod" in sublist[0])  ) :
							if( target_index in ann_dict ) :
								modifier = ann_dict[target_index]
								modifier_index = target_index

							#else :
							#	modifier = tokens[target_index]	

							
						else :
							#print "other = ", other
							if( target_index in ann_dict ) :
								other = ann_dict[target_index]
								other_index = target_index
							if( other not in other_list ) :
								other_list.append(other)	
								
						
						
						#print "\n"
								
				#### Printing Subject ######
				print "Subject = ", subject
				subject_list = [subject]
				subject_indices = [subject_index]
                                

				
				repeat = list()
				repeat.append(subject)
				repeat.append(object)
				repeat.append(other)

				#repeat.append(object_index)

				print "previous subject = ",  prev_subject, " with index = ", prev_subject_index		
				

				compound_list = list()

			        if( subject != "NIL"  ) :		                             					
							
					attributes(subject_index, dep, repeat, subject_index, subject_list, negation_list, subject_indices, rel_indices )

					compound_index_list = list()
					find_compound(subject_index, dep, tokens, compound_list, compound_index_list, subject_list )	
				

				if( subject == "NIL" and object == "NIL" ) :
				#if( subject == "NIL" and object == "NIL" and not other == "NIL") :
					print "for rel", " other = ", other
					
                                        if( other in dict_folder_name ) :
                                        	print "class = ", dict_folder_name[other]
					print "previous subject = ",  prev_subject, " with index = ", prev_subject_index
					
                                            
					if( not other == "NIL" ) :
						print "other class = ", dict_folder_name[other]
						if( other not in subject_list ) :
							#print "ADDING OTHERS = ", other
							
							subject_list.append(other)
							subject_indices.append(other_index)
						attributes(other_index, dep, repeat, other_index, subject_list, negation_list, subject_indices, rel_indices)

					#if( ( dict_folder_name[other] == "is_abnormality" 
					 #   or dict_folder_name[other] == "breastdensity" or dict_folder_name[other] == "specialcase" )):

					
					

				

				#### Printing Object ######
				print "Object = ", object

				if( object != "NIL") :
					print "for object"
					if( object not in subject_list ) :
						subject_list.append(object)
						subject_indices.append(object_index)

					attributes(object_index, dep, repeat, object_index, subject_list, negation_list, subject_indices, rel_indices)


				

				
				

				#### Printing Modifier ######
				print "Modifier = ", modifier," with index = ", modifier_index

				
				if( modifier != "NIL") :
					print "for modifier"
					if( modifier not in subject_list ) :
						subject_list.append(modifier)
						subject_indices.append(modifier_index)

					attributes(modifier_index, dep, repeat, modifier_index, subject_list, negation_list, subject_indices, rel_indices)




				######### Finding attributes for compound subjects ###########

					index = 0
					for c in compound_list :

						if( compound_index_list[index] in ann_dict ) :
							c = ann_dict[compound_index_list[index]]
						else :
							c = tokens[compound_index_list[index]]

						
						if( not c == subject ) :
						    print "c = ", c
						    attributes(subject_index, dep, repeat, subject_index, subject_list, negation_list, subject_indices, rel_indices )
						index += 1

 
				#### Printing Negation ######
				if( len(negation_list) > 0 ) :
					print "NEGATION is present"

				
				##### Sorting subject_list based on their indices in subject_indices ( to get the correct main subject ######
				subject_list = [x for (y,x) in sorted(zip(subject_indices, subject_list))]
				subject_indices.sort()

				coref_signal = 0
				##### resolving direct coreference ########################################
				if( (is_coref_word(subject) and prev_subject not in subject_list) or (prev_subject not in subject_list and new_sent_flag == 0) ) :
						subject = prev_subject
						subject_index = prev_subject_index
	                                      	subject_list = [prev_subject] + subject_list 
						subject_indices = [prev_subject_index] + subject_indices 
						coref_signal = 1
						coref_flag = 1
						print "SIGNAL", " with index = ", subject_index

				

				
				##### finding the main subject ( deciding by its class ) in the current list of subjects ######
				if( coref_signal == 0 ) :
					
					folder_name_order = ["is_abnormality", "specialcase", "breastdensity" ]
					flag = 0
					
					print "INSIDE"					

					''' for f in folder_name_order :
					
						#print "CLASSS = ", dict_folder_name[i]
						index_count = -1
	
						for i in subject_list :
						
							index_count += 1

							if( i in dict_folder_name and ( dict_folder_name[i] == f )  ) :
								subject = i
								subject_index = index_count
								flag = 1
								break

						if( flag == 1 ):
							break '''
						
					index_count = -1
					for i in subject_list :
						index_count += 1
						if( i in dict_folder_name and dict_folder_name[i] in folder_name_order ) :
							subject = i
							subject_index = index_count
							print "subject = ", i
							flag = 1
							break							
						

					prev_word = "NIL"
					sec_word = "NIL"
					third_word = "NIL"

                                	if( subject != "NIL" ) :
						print "current subject =  ", subject, " and ", new_sent
					

					first_subject_word = subject.split(' ', 1)[0]
					if( first_subject_word in tokens ) :
                                		prev_word = tokens[tokens.index(first_subject_word) - 1]
						sec_word = tokens[tokens.index(first_subject_word) - 2]
				        	third_word = tokens[tokens.index(first_subject_word) - 3]

                                		print "PREV TOKEN = ", prev_word

					#if( (subject == "NIL" or is_coref_word ( prev_word ) or is_coref_word(subject) ) and prev_subject != "NIL" ) :
					if( ( is_coref_word ( prev_word ) or is_coref_word(subject)  or is_coref_word(sec_word)  
				      	or is_coref_word(third_word) ) and prev_subject != "NIL" ) :
						print "coref sub = ", prev_subject
						if( prev_subject not in subject_list ) :
							subject_list.append( prev_subject )
							subject_indices.append( prev_subject_index )
						else :
							#target_index = 0
							#if( prev_subject in subject_list ) :
							target_index = subject_list.index(prev_subject)

							subject_indices[target_index] = prev_subject_index
							#print " at index 0 sub is = ", subject_indices[0]
						subject = prev_subject
						subject_index = prev_subject_index
						coref_flag = 1


                               # print "yooooo2 subject = ", subject
				print "\n"
				print " LIST ====== "

				#if( subject_list[0] == "NIL" and prev_subject != "NIL" ) :
				#	subject_list.append( prev_subject )
				#	subject_indices.append(prev_subject_index)				
				
				
				observation = "NIL"
				observation_index = -1

				index_count = -1
			
				

				##### finding the abnormality in the current list of subjects ######

				for i in subject_list :

					index_count += 1

					#print "CLASSS = ", dict_folder_name[i]
					if( coref_flag == 1 or ( i in dict_folder_name and ( dict_folder_name[i] == "is_abnormality" or
					    dict_folder_name[i] == "specialcase" or dict_folder_name[i] == "breastdensity") ) ) :


						if( coref_flag == 1 ) :
							i = subject
							observation_index = subject_index 
							
						else :
							observation_index = index_count
						
						observation = i
						print "ABNORMALITY FOUND" , " and observation = ", i, " index_count = ", observation_index
						
						if( observation_index  in common_index ) :
							observation_index = common_index[observation_index] 

						if( i == prev_subject and ( coref_flag == 1 or new_sent_flag == 0  ) ) :

							if( new_sent_flag == 0 ) :
							   observation_index = prev_subject_index
							   subject_list.remove(prev_subject)
						           subject = prev_subject
							   subject_index = prev_subject_index

							final_index = observation_index
							print "COREF FOUND !"
						else :
						       final_index  = observation_index + sent_offset

						if( len(negation_list) > 0 ) :
								relation_name = "not " + relation_name

						if( not final_index in char_list ) :
							print "index for ", i , " = ", final_index

							
							c = Char_value(relation_name,1)
							
							char_list[final_index] = [c]
							obs_list.append( final_index )
						
						if( relation_name not in char_list[final_index] ) :
							print "yo", " subject = ", subject
							c = Char_value(relation_name,1)
							char_list[final_index].append(c)
							if( subject in char_list[final_index] and subject in subject_list) :
								subject_list.remove(subject)
								print "sub index = ", subject_index
								subject_indices.remove(subject_index)


						observation_index = final_index	
						if( new_sent_flag == 1 or prev_flag == 0 ) :
							prev_subject = i
                                			prev_subject_index = observation_index 
							prev_flag = 1

						break
			

				

				print "prev subject = ", prev_subject , " with index = ", prev_subject_index

                                #### If all the characteristics are already present then continue ##############
				if( is_same( subject_list, group_of_lists) ) :
					continue
				

				group_of_lists.append(subject_list)

				###########################################################

				

				###### Checking if abnormality is present or not #####
				if( observation == "NIL" ) :

					##### NON ######
					for i in subject_list :
						print i ,  " || "

					print "NO ABNORMALITY"
					continue

				index_count = -1


				############## Adding compound relation arguments ######################
				for c in compound_list :
					index_count += 1

					flag = 1
					compound_index = compound_index_list[index_count]
					for s in subject_indices :
						if( compound_index == s or ( compound_index in common_index and s == common_index[compound_index] ) ) :
							flag = 0
							print "withdrawing " , compound_index , " = ", c
							break

					if( flag == 0 ) :	
						continue
		
					if( ( c in dict_folder_name and dict_folder_name[c] in exclude_class_list) and has_abnormality(subject_list) ) :
						continue
					
					subject_list.append(c)
					subject_indices.append( compound_index )
					if ( c in dict_folder_name ) :
						print "appending " , c , " with class = ", dict_folder_name[c]
				

				index_count = -1


					
				##### Printing subjects and their corresponding indices ########
				for i in subject_list :

				   index_count += 1

				   print " i = ", i
				   print " index = ", subject_indices[index_count]
			
				index_count = -1


				

				for i in subject_list :

				   index_count += 1

				   print " i = ", i
				   print " index = ", subject_indices[index_count]

				   if( observation == i ) :
					print "observation = ", i

				   
				   if( not i in char_list[observation_index] or ( i in dict_folder_name and dict_folder_name[i] in exclude_class_list ) ) :

						if( is_numerical_unit(i) ) :

							print " i = ", i
							token_index = subject_indices[index_count]
							print "index = ", token_index
							if( token_index  in common_index ) :
								token_index = common_index[token_index] 

						       	i = find_num( tokens, token_index ) + " " + tokens[token_index+1]
							print " numeric ", i

						c = Char_value(i,0)
						char_list[observation_index].append(c)
						#print c.name
	              				print i ,  " || ", " at index = ", subject_indices[index_count]					
						
						new_sent_flag = 0
				


			sent_offset += new_sent.count(' ')
			
                                  

         #### Printing abnormalities and their characteristics ########
	 print "ABNORMALITIES = \n"
	 for obs_index in obs_list :
		#print obs_index
		for ch in char_list[obs_index] :
			if( ch.relation_flag == 1 ) :
				print "\n"
				
			

			elif( not contains_digits(ch.name) and ( is_coref_word(ch.name) or ch.name not in dict_folder_name or
				( ch.name in dict_folder_name and dict_folder_name[ch.name] == "are_others") ) ) :
				continue

			#if( ch.name in ] and ( ch.name in dict_folder_name   ) ) :
			#	continue

			
			print ch.name, " with freq = ", char_list[obs_index].count(ch.name)		 

		print "\nOVER" 
	     #break

	 #break

          



	