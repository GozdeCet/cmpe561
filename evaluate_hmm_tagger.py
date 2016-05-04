#!/usr/bin/python

from __future__ import division
import sys
import re
import math

readfile_output = open(sys.argv[1], 'r')
readfile_gold = open(sys.argv[2], 'r')

args_read = open('args.txt', 'r')

for lines in args_read:
	args_col = lines.split('\t')
	flag = args_col[1]


if flag == '--cpostag':
	ctags_list = ['Noun', 'Adj', 'Adv', 'Verb', 'Pron', 'Conj', 'Det', 'Postp', 'Ques', 'Interj', 'Num', 'Dup', 'Punc']
elif flag == '--postag':
	ctags_list = ['Noun', 'Adj', 'Adv', 'Verb', 'Pron', 'Conj', 'Det', 'Postp', 'Ques', 'Interj', 'Num', 'Dup', 'Punc', 'NInf','NPastPart', 'APastPart', 'AFutPart', 'NFutPart', 'Prop', 'Zero', 'APresPart', 'DemansP', 'QuesP', 'ReflexP', 'Card', 'Range', 'Real', 'Distrib', 'Ord', 'Prop']


word_count = []
forms = []
ctags = []
for lines in readfile_gold:
		if lines != '\n':
			cols = lines.split('\t')
			word_count.append(cols[0])
			forms.append(cols[1])
			if flag == '--cpostag':
				ctags.append(cols[3])
			elif flag == '--postag':
				ctags.append(cols[4])

words_output = []
cols_output = []
tags_output = []
for lines in readfile_output:
	if lines != '\n':
		cols_output = lines.split('|')
		words_output.append(cols_output[0])
		tags_output.append(cols_output[1].rstrip('\n'))




words_gold = []
tags_gold = []
for i in range(len(word_count)):
	if forms[i] != '_':
		words_gold.append(forms[i]) 
		tags_gold.append(ctags[i])



CC_TagsNumber = []
for j in range(len(ctags_list)):
	num = 0
	for i in range(len(words_output)):
		if ctags_list[j] == tags_output[i]:
			num = num + 1
	CC_TagsNumber.append(num)


total_accuracy = 0
num = 0

for i in range(len(words_gold)):
	if words_gold[i] == words_output[i]:
		if tags_gold[i] == tags_output[i]:
			num = num + 1 
			total_accuracy = num  / len(tags_gold)


total_true = []
tag_accuracy = []
num = 0
for j in range(len(ctags_list)):
	num = 0
	for i in range(len(words_gold)):
		if ctags_list[j] == tags_gold[i]:
			if tags_gold[i] == tags_output[i]:
				if words_gold[i] == words_output[i]:
					num = num + 1 
	total_true.append(num)


#print total_true
#print CC_TagsNumber

num = 0
for j in range(len(CC_TagsNumber)):
	if CC_TagsNumber[j] != 0 and total_true[j] != 0:
		num = total_true[j] / CC_TagsNumber[j]
		tag_accuracy.append(num)

#print tag_accuracy
			
exist_tag_index = []
exist_tag_name = []
for j in range(len(ctags_list)):
	if CC_TagsNumber[j] != 0:
		exist_tag_index.append([j])
		exist_tag_name.append(ctags_list[j])

#print exist_tag_name	

output1 = open('accuracy_and_confisuon.txt', 'w')
output1.write("Total accuracy of the tagger : %s\n"  % (total_accuracy) )
output1.write("\n\n")
output1.write("Individual accuracy of the tags : \n")
for i in range(len(exist_tag_name)):
	output1.write("%s\t %s\n" % (exist_tag_name[i],tag_accuracy[i]) )

output1.write("\n\n")	
output1.write("Confisuon matrix : \n\n")
output1.write("\t\t\tOutput file\t\tGold file \n")
for i in range(len(words_output)):
	output1.write("%s\t\t\t%s\t\t%s\n" % (words_output[i],tags_output[i],tags_gold[i]))
		

			
		
		




