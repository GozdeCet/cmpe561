#!/usr/bin/python

from __future__ import division
import sys
import re
import math

readfile_test = open(sys.argv[1], 'r')
output1 = open(sys.argv[2], 'w')


 #  ---------------------------------------------- 1) ESTIMATING THE HMM PARAMETERS FROM TRAINING FILE --------------------------------------------------------

args_read = open('args.txt', 'r')

for lines in args_read:
	args_col = lines.split('\t')
	train = args_col[0]
	flag = args_col[1]

readfile_train = open(train, 'r')
word_count = []
forms = []
ctags = []

if flag == '--cpostag':
	ctags_list = ['Noun', 'Adj', 'Adv', 'Verb', 'Pron', 'Conj', 'Det', 'Postp', 'Ques', 'Interj', 'Num', 'Dup', 'Punc']
elif flag == '--postag':
	ctags_list = ['Noun', 'Adj', 'Adv', 'Verb', 'Pron', 'Conj', 'Det', 'Postp', 'Ques', 'Interj', 'Num', 'Dup', 'Punc', 'NInf','NPastPart', 'APastPart', 'AFutPart', 'NFutPart', 'Prop', 'Zero', 'APresPart', 'DemansP', 'QuesP', 'ReflexP', 'Card', 'Range', 'Real', 'Distrib', 'Ord', 'Prop']


for lines in readfile_train:
		if lines != '\n':
			cols = lines.split('\t')
			word_count.append(cols[0])
			forms.append(cols[1])
			if flag == '--cpostag':
				ctags.append(cols[3])
			elif flag == '--postag':
				ctags.append(cols[4])

# Number of the (NN),(Adj) vs in text -----

CC_TagsNumber = []
for j in range(len(ctags_list)):
	num = 0
	for i in range(len(ctags)):
		if forms[i] != '_':
			if ctags_list[j] == ctags[i]:
				num = num + 1
	CC_TagsNumber.append(num + len(ctags_list))


# Number of the (NN),(Adj) for the start -----

CC_TagStart = []
for j in range(len(ctags_list)):
	num = 0
	for i in range(len(ctags)):
		if forms[i] != '_' and word_count[i] == '1':
			if ctags_list[j] == ctags[i]:
				num = num + 1
	CC_TagStart.append(num + 1)	


# Number of the (NN),(Adj) for the end -----

CC_TagEnd = []
for j in range(len(ctags_list)):
	num = 0
	for i in range(len(ctags)):
		if forms[i] != '_' and i != len(word_count)-1 and word_count[i+1] == '1':
			if ctags_list[j] == ctags[i]:
				num = num + 1
	CC_TagEnd.append(num + 1)	


# Number of the (NN->NN), (NN->Adj) vs. -----

dummy_list = []                                                             
for i in range (0, len(ctags_list)):                              
	new = []                  
	for j in range (0, len(ctags_list)):    
		new.append(0)       
	dummy_list.append(new)
			
for i in range(len(word_count)):
	if forms[i] != '_' and i != len(word_count)-1 and ctags_list.count(ctags[i]) > 0: #'Zero'appears two time, but not in the ctags_list so last and to avoid it
		temp1 = ctags_list.index(ctags[i])
		j = 1
		while forms[i+j] == '_':    # if form is '_', do not count the next, but remember the numbers of '_' to calculate next 
			j = j + 1
		if word_count [i + j] != '1' and ctags_list.count(ctags[i + j]) > 0:
			temp2 = ctags_list.index(ctags[i + j])
			dummy_list[temp1][temp2] = dummy_list[temp1][temp2] + 1


# Calculation of the transition propabilities ----------------------------------------------



# for P(nn|<s>) vs. -----

P_start_transition = []   
for i in range(len(CC_TagsNumber)):
	if CC_TagsNumber[i] != 0 and CC_TagStart[i] != 0:
		P_start_transition.append(CC_TagStart[i] / CC_TagsNumber[i])
	else:
		P_start_transition.append(0)

# for P(nn|</s>) vs. -----

P_end_transition = []   
for i in range(len(CC_TagsNumber)):
	if CC_TagsNumber[i] != 0 and CC_TagEnd[i] != 0:
		P_end_transition.append(CC_TagEnd[i] / CC_TagsNumber[i])
	else:
		P_end_transition.append(0)

# for P(nn|nn) vs. -----  

P_transition = []                                                     
for i in range (0, len(ctags_list)):                              
	new = []                  
	for j in range (0, len(ctags_list)):    
		new.append(0)       
	P_transition.append(new)		
			
for i in range(13):
	for j in range(13):
		if CC_TagsNumber[i] != 0:
			P_transition[i][j] = (dummy_list[i][j] +1) / CC_TagsNumber[i]
		else:
			P_transition[i][j] = 0


# for P(NN|forms) ------

P_word_emission = {}
for i in range(len(ctags)):
	if forms[i] != '_' and ctags_list.count(ctags[i]) > 0:
		temp = (ctags[i], forms[i])
		if temp not in P_word_emission:
			P_word_emission[temp] = 1 / CC_TagsNumber[ctags_list.index(ctags[i])]
		else:
			P_word_emission[temp] = P_word_emission[temp] + 1/ CC_TagsNumber[ctags_list.index(ctags[i])]
	

#------------------------------------------------------- 2) TAGGING THE UNSEEN TEST DATA --------------------------------------------------------------------------

# Start transition probability -> P_start_transition
# End transition probability -> P_end_transition
# Transition probabilities -> P_transition
# Word emission probabilities -> P_word_emission


#readfile_test = open('test_file', 'r')

Test_word_count = []
Test_forms = []
for lines in readfile_test:
	if lines != '\n':
		Test_cols = lines.split('\t')
		Test_word_count.append(Test_cols[0])
		Test_forms.append(Test_cols[1])

Pos_first_word = []
for i in range(Test_word_count.count('1')):
	if len(Pos_first_word) == 0:
		Pos_first_word.append(Test_word_count.index('1'))
	else:
		Pos_first_word.append(Test_word_count.index('1', Pos_first_word[i-1]+1))

Pos_first_word.append(int(Test_word_count[-1]) + Pos_first_word[-1])

#output1 = open('output.txt', 'w')


for i in range(Test_word_count.count('1')):
	best_score_word = []
	min_path = []
	for j in range(Pos_first_word[i], Pos_first_word[i+1]):
		temp_list = []
		min_path_list = []
		if Test_forms[j] != '_':
			if len(best_score_word) == 0:
				for k in range(len(ctags_list)):
					if (ctags_list[k], Test_forms[j]) in P_word_emission and P_start_transition[k] != 0:
						temp_list.append( (-1)*(math.log10(P_start_transition[k])) + (-1)*(math.log10(P_word_emission[ctags_list[k], Test_forms[j]])) )
					elif (ctags_list[k], Test_forms[j]) in P_word_emission and P_start_transition[k] == 0:
						temp_list.append( (-1)*(math.log10(P_word_emission[ctags_list[k], Test_forms[j]])) )
					elif (ctags_list[k], Test_forms[j]) not in P_word_emission and P_start_transition[k] != 0:
						temp_list.append( (-1)*(math.log10(P_start_transition[k])) + 100 )
					else:
						temp_list.append(100)
				best_score_word.append(temp_list)			
			else:
				for k in range(len(ctags_list)):
					temp_list2 = []
					for m in range(len(ctags_list)):
						if (ctags_list[k], Test_forms[j]) in P_word_emission and P_transition[k][m] != 0:
							temp_list2.append( best_score_word[-1][m] + (-1)*(math.log10(P_transition[k][m])) + (-1)*(math.log10(P_word_emission[ctags_list[k], Test_forms[j]])) )
						elif (ctags_list[k], Test_forms[j]) in P_word_emission and P_transition[k][m] == 0:
							temp_list2.append( best_score_word[-1][m] + (-1)*(math.log10(P_word_emission[ctags_list[k], Test_forms[j]])) )
						elif (ctags_list[k], Test_forms[j]) not in P_word_emission and P_transition[k][m] != 0:
							temp_list2.append( best_score_word[-1][m] + (-1)*(math.log10(P_transition[k][m])) + 100 )
						else:
							temp_list2.append(100)
					temp_list.append(min(temp_list2))
					min_path_list.append(temp_list2.index(min(temp_list2)))
				best_score_word.append(temp_list)
				min_path.append(min_path_list)
	temp_list = []
	min_path_list = []
	temp_list2 = []

	for k in range(len(ctags_list)):		
		if P_end_transition[k] != 0:
			temp_list2.append( best_score_word[-1][k] + (-1)*(math.log10(P_end_transition[k])) )
		else:
			temp_list2.append(best_score_word[-1][k])
	temp_list.append(min(temp_list2))
	min_path_list.append(temp_list2.index(min(temp_list2)))
	best_score_word.append(temp_list)
	min_path.append(min_path_list)	

	tags = []
	next_edge = min_path[-1][0]
	tags.append(next_edge)
	for a in range(len(min_path)-1):	
		next_edge = min_path[-2 - a][next_edge]
		tags.append(next_edge)
	tags.reverse()


	t = 0
	for j in range(Pos_first_word[i], Pos_first_word[i+1]):
		if Test_forms[j] != '_':
			output1.write("%s|" % (Test_forms[j])) 
			output1.write("%s\n" % (ctags_list[tags[t]] ))
			t = t + 1
	if i < Test_word_count.count('1') - 1:
		output1.write("\n") 



