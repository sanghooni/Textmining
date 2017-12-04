from bs4 import BeautifulSoup
import re
import string
from nltk.corpus import wordnet as wn

def replace(fin_name,srcStr,desStr,fout_name):
	fin = open(fin_name, "r")
	fout = open(fout_name, "w")
	txt = fin.read()
	txtout = re.sub(srcStr,desStr, txt)

	fout.write(txtout)
	fin.close()
	fout.close()

filename = input("Input file name : ")

Total_DATA = []
# pretreatment in html file
replace(filename,">\d+\w*[</\w+>]*</a>","></\w+></a>", "temp2.html")
html_doc = open("temp2.html", encoding = "UTF-8")

# eliminating HTML tags
f = BeautifulSoup(html_doc, 'html.parser')
for i in f(["script","style",'ol','ul','li','table','noscript','option','a']):
	i.extract()
for i in f(["div"]):
	if i.get('class') == ['citationInfo'] or i.get('class') == ['casRecord'] or i.get('class') == ['casContent'] or i.get('class') == ['casTitle'] or i.get('class') == ['casAuthors'] or i.get('class') == ['casAbstract']:
		#print (i.get_text())
		i.extract()
for i in f(['sup','sub']):
	i.unwrap()

g = f.get_text()
# pretreatment2
g = re.sub("\n","",g)
g = re.sub("&thinsp;","",g)
g = re.sub("&nbsp;"," ",g)
g = re.sub("\u2009"," ",g)
g = re.sub("\u2005"," ",g)

# split in sentences and store in array
sentences = []
sentences = g.split(".")
for i in range(len(sentences)):
	sentences[i] += "."

front = re.compile('[^A-Z]\d+.$|\s?Fig.\s?$|\s+\w{1,3}[,.]\s?$|i.e.\s?$')
back = re.compile('^\s?\w?\d+|^g.\s?|^\s?\w+[,.]\s?$|^,')

appended = 0
for i in range(len(sentences)):
	value_find = front.search(sentences[i])
	temp_sentence = sentences[i]
	while value_find != None:
		if back.search(sentences[i+1]) != None:
			temp_sentence += sentences[i+1]
			del sentences[i+1]
			sentences.append('\n')
			appended += 1
			value_find = front.search(temp_sentence)
		else:
			value_find = None
	sentences[i] = temp_sentence

sentences.reverse()
for i in range(appended):
	del sentences[0]
sentences.reverse()

# MOF name candidate - MOF criteria : Need to be modified later
Upper = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
Number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

MOF_in_Paper = [];
words = [];


for i in range(len(sentences)):
	words = sentences[i].split(' ')
	for j in range(len(words)):
		# words pretreatment

		words[j].replace("-","-")
		if len(words[j]) > 2:
			if words[j][-1] == ')':
				words[j] = words[j][:-1]
			if words[j][0] == '(':
				words[j] = words[j][1:]

		if len(words[j]) > 2:
			if words[j][-1] == ',' or words[j][-1] == '.' or words[j][-1] == ';' or words[j][-1] == ':' or words[j][-1] == "\n":
				words[j] = words[j][:-1]
			if words[j][-1] == ')':
				words[j] = words[j][:-1]
			if words[j][0] == '(':
				words[j] = words[j][1:]
		MOF_Crit = 0

		MOF_Crit_Number = 0
		MOF_Crit_Upper = 0

		if words[j].find('-') != -1:
			MOF_Crit += 2
			if words[j][0] == '-':
				MOF_Crit += 1


		for k in range(len(Upper)):
			if words[j].find(Upper[k]) != -1:
				MOF_Crit_Upper += 1

		if MOF_Crit_Upper != 0:
			MOF_Crit += 1

		No_number = 1
		for k in range(len(Number)):
			if words[j].find(Number[k]) != -1:
				MOF_Crit_Number += 1
				No_number = 0

		if MOF_Crit_Number != 0:
			MOF_Crit += 1

		if words[j].find('(') * words[j].find(')') >= 0 and words[j].find('(') >= 0:
			MOF_Crit += 1

		if words[j].find('[') * words[j].find(']') >= 0 and words[j].find('[') >= 0:
			MOF_Crit += 1

		if words[j].find('MOF') != -1 or words[j].find('PCN') != -1:
			MOF_Crit += 1

		Linker_words = ["DOBDC","BTC","bdc","CuBT","13X","TO","DBTO","DTO","BTO","Car","bpe","tftpa"]
		for k in range(len(Linker_words)):
			if words[j].find(Linker_words[k]) != -1:
				MOF_Crit += 2

		if words[j] == 'AT':
			MOF_Crit += 2

		if len(words[j]) > 0:
			if words[j].find("13X") == -1:
				if words[j][0].isdigit() == True or words[j][0] == '+':
					MOF_Crit = 0

# Empirically added no MOF words
		if words[j].find('MJXp') != -1 or words[j].find('PLATON') != -1:
			MOF_Crit = 0

		if words[j].find('=') != -1 or words[j].find('=') != -1:
			MOF_Crit = 0

		if words[j] != '' and words[j][-1] == '-':
			MOF_Crit = 0
		#if MOF_Crit > 2:
			#print (words[j],MOF_Crit)
		Prop_noun = 0
		if words[j].find('-') != -1:
			Prop_noun = 1
			tempword = words[j].split('-')
			for k in range(len(tempword)):
				#print (tempword[k],len(tempword[k]))
				passlist = ["MIL","POST","NU","rho","sod"]
				contin_crit = 0
				for l in range(len(passlist)):
					if tempword[k] == passlist[l]:
						contin_crit = 1
				if contin_crit == 1:
				 	continue
				if len(tempword[k]) <= 1:
					Prop_noun = 0
				if k != 0 and tempword[k].isdigit():
					continue
				#print (wn.lemmas(tempword[k]))
				Atom_word = 0
				if len(tempword[k]) == 2 and tempword[k].isalpha() == True and tempword[k][0].isupper() == True and tempword[k][1].islower() == True and wn.lemmas(tempword[k]) != []:
					Atom_word = 1
					Prop_noun = 0
					continue
				if len(tempword[k]) > 1 and tempword[k].isdigit() == False and wn.lemmas(tempword[k]) != []:
					MOF_Crit = 0
				if len(tempword[k]) > 2 and tempword[k].isalpha() == True and tempword[k][0].isupper() == True and tempword[k][1:].islower() == True:
					MOF_Crit = 0
					break
		#if MOF_Crit > 2:
			#print (words[j])
		if len(words[j]) > 3 and words[j][0].isupper() == True and words[j][1:].islower() == True:
			Prop_noun = 1

		if Prop_noun == 1:
			if No_number == 1 and words[j].find('(') == -1 and words[j].find(')') == -1:
				MOF_Crit = 0

		if wn.lemmas(words[j]) != [] or words[j] == 'D-R':
			MOF_Crit = 0

		if len(words[j]) < 3:
			MOF_Crit = 0

		if MOF_Crit > 2:

			if words[j][0].find('(') != -1:
				if words[j][-1].find(')') != -1:
					words[j] = words[j][1:-1]

			if not words[j][0].islower() or words[j][0:3] == 'sod' or words[j][0:3] == 'rho' or words[j][0:3] == 'bio' or words[j].find('agglomerate') != -1: # first letter big
				if not words[j][0].isdigit(): # first letter not digit
					if len(MOF_in_Paper) != 0:
						for l in range(len(MOF_in_Paper)):
							if MOF_in_Paper.count(words[j])== 0: #double check
								MOF_in_Paper.append(words[j])
					else:
						MOF_in_Paper.append(words[j])
				elif words[j].find('13X') != -1 or Atom_word == 1:
					if len(MOF_in_Paper) != 0:
						for l in range(len(MOF_in_Paper)):
							if MOF_in_Paper.count(words[j])== 0: #double check
								MOF_in_Paper.append(words[j])
					else:
						MOF_in_Paper.append(words[j])

#print (MOF_in_Paper)
# Close file and reopen it to solve BOLD problem
html_doc.close()
html_doc = open("temp2.html", encoding = "UTF-8")
#html_doc = open("ref131.html", encoding = "UTF-8")

# eliminating HTML tags - Reference delete
f = BeautifulSoup(html_doc, 'html.parser')
# extracting non usable tags

for i in f(["script","style",'ol','ul','li','noscript','option']):
	i.extract()
for i in f(["div"]):
	if i.get('class') == ['citationInfo'] or i.get('class') == ['casRecord'] or i.get('class') == ['casContent'] or i.get('class') == ['casTitle'] or i.get('class') == ['casAuthors'] or i.get('class') == ['casAbstract']:
		#print (i.get_text())
		i.extract()





#Treating Bold tag MOFs
bold_tag = ['1','1′','2','3','4','5','6','7','7′','8','(1)','(2)','(3)','1a','1b','1c','2a','2b','2c','3a','3b','3c','a','b','c','d','1 a','2 a','2 b','A','B','C','D','1 d','I','II']
bold_tag_candidate = []
bold_MOF = []
for i in f.find_all(['strong','b']):
	# set bold MOF tag criteria
	bold_tag_Crit = 1
	No_number = 1
	No_letter = 1
	if i.string == None:
		continue
	i.string = i.string.strip()
	for j in range(len(i.string)):
		if i.string[j].isdigit() == True:
			No_number = 0
		if i.string[j].isalpha() == True:
			No_letter = 0
	if No_number == 1:
		if len(i.string) > 2:
			bold_tag_Crit = 0
		elif No_letter == 1:
			bold_tag_Crit = 0
	elif No_number == 0 and i.string.isdigit() == True:
		if int(i.string) > 1000:
			bold_tag_Crit = 0

	if i.string[:3] == 'Fig' or i.string[:6] == 'Scheme':
		bold_tag_Crit = 0

	for j in range(len(MOF_in_Paper)):
		if i.string.find(MOF_in_Paper[j]) != -1:
			bold_tag_Crit = 0
			break

	if bold_tag_Crit == 1:
		if bold_tag_candidate != []:
			for j in range(len(bold_tag_candidate)):
				if len(i.string) < 8:
					if bold_tag_candidate.count(i.string) == 0:
						bold_tag_candidate.append(i.string)
		else:
			bold_tag_candidate.append(i.string)
#print (bold_tag_candidate)
for i in f.find_all(['strong','b']):
	if bold_tag_candidate.count(i.string) == 1:
		store = 0
		MOF = ''
		bold_sentence = i.parent.get_text()

		out = 0
		start_pos = 0
		while out == 0:
			bold_index = bold_sentence.find(i.string,start_pos)
			pass_crit = 0
			if bold_index != -1 and bold_index != 0 and bold_index != len(bold_sentence):
				if bold_sentence[bold_index-1].isdigit() or bold_sentence[bold_index-1].isalpha():
					pass_crit += 1
				if bold_index + len(i.string) <= len(bold_sentence) and bold_sentence[bold_index+len(i.string)].isdigit() or bold_sentence[bold_index+len(i.string)].isalpha():
					pass_crit += 1
			if pass_crit == 2:
			  	start_pos = bold_index + 1
			else:
				out = 1


		bold_sentence = bold_sentence.split()
		#print (bold_sentence)
		for k in range(len(bold_sentence)):
			bold_index = bold_index - len(bold_sentence[k]) - 1
			if bold_index >= 0:
				continue
			#print (bold_sentence[k])
			if store == 0 and bold_sentence[k].find(i.string) != -1:
				#print (k)
				if k != 0 and k != len(bold_sentence) - 1:
					for l in range(len(MOF_in_Paper)):
						if bold_sentence[k-1] == 'MOF' or bold_sentence[k-1] == '(MOF' or bold_sentence[k-1] == 'Compound' or bold_sentence[k-1] == '(Compound':
							if bold_sentence[k-2].find(MOF_in_Paper[l]) != -1:
								store = 1
								MOF = bold_sentence[k-2]
								break
						if bold_sentence[k-1].find(MOF_in_Paper[l]) != -1:
							store = 1
							MOF = bold_sentence[k-1]
							break
						elif bold_sentence[k+1].find(MOF_in_Paper[l]) != -1:
							store = 1
							MOF = bold_sentence[k+1]
							break
				elif k == 0:
					for l in range(len(MOF_in_Paper)):
						if k+1 < len(bold_sentence):
							if bold_sentence[k+1].find(MOF_in_Paper[l]) != -1:
								store = 1
								MOF = bold_sentence[k+1]
								break
				elif k == len(bold_sentence) - 1:
					for l in range(len(MOF_in_Paper)):
						if bold_sentence[k-1] == 'MOF' or bold_sentence[k-1] == '(MOF':
							if bold_sentence[k-2].find(MOF_in_Paper[l]) != -1:
								store = 1
								MOF = bold_sentence[k-2]
								break
						if bold_sentence[k-1].find(MOF_in_Paper[l]) != -1:
							store = 1
							MOF = bold_sentence[k-1]
							break
		if store == 1:
			#print (bold_sentence)
			bold_MOF.append(i.string)
			bold_MOF.append(MOF)
			bold_tag_candidate[bold_tag_candidate.index(i.string)] = ''
#print (bold_MOF)
for i in f.find_all(['strong','b']):
	for j in range(int(len(bold_MOF)/2)):
		if i.string == bold_MOF[2*j]:
			i.string.replace_with(bold_MOF[2*j+1])











# handle table
Pore_table = re.compile('^\w?PV\s?|^V\W{0,3}T\W?|^V\W{0,3}p$|^V\W{0,3}p\W+\W+|^V\W{0,3}meso\W?|^V\W{0,3}micro\W?|^V\W{0,3}total\W?|^V\W{0,3}pore\W?|Pore\s{0,3}Volume', re.IGNORECASE)
Pore = re.compile('Volume\W?\(cm3\s?g\)|mesopore\W?volume|micropore\W?volume|pore\W?volume|\W+PV\s?|V\W?T|V\W?P|V\W?meso|V\W?micro|V\W?total|V\W?pore|effective\W?free\W?volume|permanent\W?porosity', re.IGNORECASE)
BET_table = re.compile('SBET|BET|Brunauer\s?[−-]?\W?Emmett\s?[−-]?\W?Teller|Langmuir|Surface\s?area|m2/g|SA\W|m2 g-1', re.I)
BETLang = re.compile('BET|Brunauer\s?[−-]?\W?Emmett\s?[−-]?\W?Teller|Langmuir|SLang|SALm')
BET = re.compile('BET|Brunauer\s?[−-]?\W?Emmett\s?[−-]?\W?Teller')
Lang = re.compile('Langmuir|SLang|SALm')
digit = re.compile('\d+[.,]?\d*|\d+.\d+[·*]10\d+') # digit criteria





tables = f.find_all('table')
for table in tables:
	if table.find_all('table') != []:
		continue
	data = []
	if table != None:
		table_head = table.thead
		head_crit = 0
		if table_head != None:
			head_crit = 1

			rows = table_head.find_all('tr')
			rownum = 0
			rownow = 0
			for row in rows:
				rownum += 1
				if rownow < rownum:
					data.append([])
					rownow += 1
				cols = row.find_all('th')
				colnum = 0
				colnow = len(data[rownum - 1])
				for col in cols:
					#text pretreatment
					text = col.text.strip()
					text.replace("\n"," ")
					text.replace('&nbsp;',' ')
					text.replace('\u2009',' ')
					text.replace(" ","")
					colnum += 1
					if colnow < colnum:
						data[rownum-1].append([])
						colnow += 1
					while data[rownum-1][colnum-1] != []:
						colnum += 1
						if colnow < colnum:
							data[rownum-1].append([])
							colnow += 1
					colspannum = 1
					#print(col.attrs)
					if col.attrs.get('colspan') != None and col.attrs.get('colspan') != '':
						colspannum = int(col['colspan'])
					rowspannum = 1
					if col.attrs.get('rowspan') != None:
						rowspannum = int(col['rowspan'])
					if rowspannum == 1 and colspannum == 1:
						temp = colnum
						while data[rownum-1][temp-1] != []:
							temp += 1
						data[rownum-1][temp-1].append(text)

					if rowspannum == 1 and colspannum != 1:
						for j in range(colspannum - 1):
							data[rownum-1].append([])
						colnow += colspannum - 1
						for i in range(colspannum):
							if data[rownum-1][colnum-1+i] == []:
								data[rownum-1][colnum-1+i].append(text)
						colnum += colspannum - 1

					if rowspannum != 1 and colspannum == 1:
						if rownow < rownum + rowspannum-1:
							for j in range(rownum + rowspannum - rownow - 1):
								data.append([])
								rownow += 1
						for i in range(rowspannum):
							if len(data[rownum+i-1]) < colnum:
								for j in range(colnum - len(data[rownum+i-1])):
									data[rownum+i-1].append([])

							if data[rownum+i-1][colnum-1] == []:
								data[rownum+i-1][colnum-1].append(text)
					if rowspannum != 1 and colspannum != 1:
						if rownow < rownum + rowspannum-1:
							for j in range(rownum + rowspannum - rownow - 1):
								data.append([])
								rownow += 1
						for i in range(rowspannum):
							if len(data[rownum+i-1]) < colnum + colspannum:
								for j in range(colnum + colspannum - len(data[rownum+i-1])):
									data[rownum+i-1].append([])
							for j in range(colspannum):
								if data[rownum+i-1][colnum+j-1] == []:
									data[rownum+i-1][colnum+j-1].append(text)



		table_body = table.tbody
		if table_body != None:

			rows = table_body.find_all('tr')
			head_row_num = len(data)
			if head_row_num == 0:
				head_row_num = 1 # if there is no thead, top of tbody is head_row
			rownum = len(data)
			rownow = len(data)
			for row in rows:
				rownum += 1
				if rownow < rownum:
					data.append([])
					rownow += 1
				cols = row.find_all('td')
				colnum = 0
				colnow = len(data[rownum - 1])
				for col in cols:
					#text pretreatment
					text = col.text.strip()
					text.replace("\n"," ")
					text.replace('&nbsp;',' ')
					text.replace('\u2009',' ')
					text.replace(" ","")
					colnum += 1
					if colnow < colnum:
						data[rownum-1].append([])
						colnow += 1
					while data[rownum-1][colnum-1] != []:
						colnum += 1
						if colnow < colnum:
							data[rownum-1].append([])
							colnow += 1
					colspannum = 1
					if col.attrs.get('colspan') != None and col.attrs.get('colspan') != '':
						colspannum = int(col['colspan'])
					rowspannum = 1
					if col.attrs.get('rowspan') != None:
						rowspannum = int(col['rowspan'])
					if rowspannum == 1 and colspannum == 1:
						temp = colnum
						while data[rownum-1][temp-1] != []:
							temp += 1;
						data[rownum-1][temp-1].append(text)

					if rowspannum == 1 and colspannum != 1:
						for j in range(colspannum - 1):
							data[rownum-1].append([])
						colnow += colspannum - 1
						for i in range(colspannum):
							if data[rownum-1][colnum-1+i] == []:
								data[rownum-1][colnum-1+i].append(text)
						colnum += colspannum - 1
					if rowspannum != 1 and colspannum == 1:
						if rownow < rownum + rowspannum-1:
							for j in range(rownum + rowspannum - rownow - 1):
								data.append([])
								rownow += 1
						for i in range(rowspannum):
							if len(data[rownum+i-1]) < colnum:
								for j in range(colnum - len(data[rownum+i-1])):
									data[rownum+i-1].append([])
							if data[rownum+i-1][colnum-1] == []:
								data[rownum+i-1][colnum-1].append(text)
						
					if rowspannum != 1 and colspannum != 1:
						if rownow < rownum + rowspannum-1:
							for j in range(rownum + rowspannum - rownow - 1):
								data.append([])
								rownow += 1
						for i in range(rowspannum):
							if len(data[rownum+i-1]) < colnum + colspannum:
								for j in range(colnum + colspannum - len(data[rownum+i-1])):
									data[rownum+i-1].append([])
							for j in range(colspannum):
								if data[rownum+i-1][colnum+j-1] == []:
									data[rownum+i-1][colnum+j-1].append(text)
	for i in range(len(data)):
		for j in range(len(data[i])):
			if data[i][j] == []:
				data[i][j].append('')

	#for i in range(len(data)):
		#print(i,data[i])
	#print ('\n')
	surf_table = 0
	surf_column = []
	head_type = ''
	if data != []:
	
#		if head_row_num != 0:
#			for j in range(head_row_num):
#				for i in range(len(data[j])):
#					if BET_table.search(data[j][i][0]) != None:
#						if BET.search(data[j][i][0]) != None:
#							type = 'BET'
#						elif Lang.search(data[j][i][0]) != None:
#							type = 'Lang'
#						else:
#							type = '*IDK*'
#						head_type = 'top'
#						surf_column.append([i,type,head_type])
#						surf_table = 1
		for i in range(len(data[0])):
			surface_finder = ''
			#print (head_row_num)
			if head_row_num == 1:
				surface_finder = data[0][i][0]
			else:
				for j in range(head_row_num):
					surface_finder += data[j][i][0]+' '
			#print (surface_finder)
			if Pore_table.search(surface_finder) != None:
				if Pore.search(surface_finder) != None:
					type = 'Pore_volume'
				else:
					type = 'Pore_volume'
				head_type = 'top'
				surf_column.append([i,type,head_type])
				surf_table = 1
		for i in range(len(data)):
			#print (i,data[i])
			if data[i] != [] and Pore_table.search(data[i][0][0]) != None:
				if Pore.search(data[i][0][0]) != None:
					type = 'Pore_volume'
				else:
					type = 'Pore_volume'
				head_type = 'left'
				surf_column.append([i,type,head_type])
				surf_table = 1
		if surf_table == 1 and surf_column != []:
			print ('<Pore Volume data in table>\n')
			isMOF = 0
			if head_type == 'top':
				for i in range(len(data)-1):
					for j in range(len(MOF_in_Paper)):
						if data[i+1][0][0].find(MOF_in_Paper[j]) != -1:
							isMOF += 1
				MOF_column = 0
				if isMOF != 0:
					MOF_column = 1
			if head_type == 'left':
				isMOF = 0
				for i in range(head_row_num):
					for j in range(len(data[i])-1):
						for k in range(len(MOF_in_Paper)):
							if data[i][j+1][0].find(MOF_in_Paper[k]) != -1:
								isMOF += 1
				MOF_column = 1


			nowprint = 0
			for i in range(len(surf_column)):
				if surf_column[i][2] == 'top':
					for j in range(len(data) - head_row_num):
						if head_row_num == 0 and nowprint == 0:
							nowprint = 1
							continue
						noprint = 0
						if digit.search(data[j+head_row_num][surf_column[i][0]][0]) == None:
							noprint = 1
						if noprint == 0:
							MOF_name = ''
							MOF_data_in_MOFcol = 0
							temp_list = data[head_row_num - 1][surf_column[i][0]][0].split()
							for l in range(len(temp_list)):
								for m in range(len(MOF_in_Paper)):
									if temp_list[l].find(MOF_in_Paper[m]) != -1:
										MOF_name = temp_list[l]
										MOF_data_in_MOFcol = 1
							if MOF_column == 1:
								Total_DATA.append([data[j+head_row_num][0][0],surf_column[i][1],data[j+head_row_num][surf_column[i][0]][0],'cm3/g'])
								print (data[j+head_row_num][0][0],"|",surf_column[i][1],"|",data[j+head_row_num][surf_column[i][0]][0],"|",'cm3/g')
							elif table.find("caption") != None:
								caption = table.find("caption")
								caption_text = caption.get_text().split(' ')
								for l in range(len(caption_text)):
									for m in range(len(MOF_in_Paper)):
										if caption_text[l].find(MOF_in_Paper[m]) != -1:
											MOF_name = caption_text[l];
								MOF_name = MOF_name+'--'+data[head_row_num - 1][0][0]+':'+data[head_row_num+j][0][0]
								## state word need to be added
								Total_DATA.append([MOF_name, surf_column[i][1],data[j+head_row_num][surf_column[i][0]][0],'cm3/g'])
								print (MOF_name,"|", surf_column[i][1],"|",data[j+head_row_num][surf_column[i][0]][0],"|",'cm3/g')
							elif MOF_data_in_MOFcol == 1:
								Total_DATA.append([MOF_name, surf_column[i][1],data[j+head_row_num][surf_column[i][0]][0],'cm3/g'])
								print (MOF_name,"|", surf_column[i][1],"|",data[j+head_row_num][surf_column[i][0]][0],"|",'cm3/g')
							else:
								Total_DATA.append(['*NO_MOF_data*', surf_column[i][1],data[j+head_row_num][surf_column[i][0]][0],'cm3/g'])
								print ('*NO_MOF_data*',"|", surf_column[i][1],"|",data[j+head_row_num][surf_column[i][0]][0],"|",'cm3/g')


				elif surf_column[i][2] == 'left':
					for j in range(len(data[i]) - 1):
						noprint = 0
						if digit.search(data[surf_column[i][0]][j+1][0]) == None:
							noprint = 1
						if noprint == 0:
							if MOF_column == 1:
								MOF_name = ''
								MOF_data_in_MOFcol = 0
								temp_list = data[surf_column[i][0]][0][0].split()
								for l in range(len(temp_list)):
									for m in range(len(MOF_in_Paper)):
										if temp_list[l].find(MOF_in_Paper[m]) != -1:
											MOF_name = temp_list[l]
											MOF_data_in_MOFcol = 1
								for k in range(head_row_num):
									if MOF_name.find(data[k][j+1][0]) == -1:
										MOF_name += data[k][j+1][0]+' '
								Total_DATA.append([MOF_name, surf_column[i][1], data[surf_column[i][0]][j+1][0], 'cm3/g'])
								print (MOF_name,"|", surf_column[i][1],"|", data[surf_column[i][0]][j+1][0],"|", 'cm3/g')

							elif table.find("caption") != None:
								caption = table.find("caption")
								caption_text = caption.get_text().split(' ')
								for l in range(len(caption_text)):
									for m in range(len(MOF_in_Paper)):
										if caption_text[l].find(MOF_in_Paper[m]) != -1:
											MOF_name = caption_text[l];
								## state word need to be added
								Total_DATA.append([MOF_name, surf_column[i][1],data[surf_column[i][0]][j+1][0],'cm3/g'])
								print (MOF_name,"|", surf_column[i][1],"|",data[surf_column[i][0]][j+1][0],"|",'cm3/g')
							elif MOF_data_in_MOFcol == 1:
								Total_DATA.append([MOF_name, surf_column[i][1],data[surf_column[i][0]][j+1][0],'cm3/g'])
								print (MOF_name,"|", surf_column[i][1],"|",data[surf_column[i][0]][j+1][0],"|",'cm3/g')
							else:
								Total_DATA.append(['*NO_MOF_data*', surf_column[i][1], data[surf_column[i][0]][j+1][0], 'cm3/g'])
								print ('*NO_MOF_data*',"|", surf_column[i][1],"|", data[surf_column[i][0]][j+1][0],"|", 'cm3/g')




for i in f(['table']):
	i.extract()

g = f.get_text()

# pretreatment2
g = re.sub("\n","",g)
g = re.sub("&nbsp;"," ",g)
g = re.sub("&#x2005;"," ",g)
g = re.sub("&thinsp;","",g)
g = re.sub("&minus;","-",g)
# DIgit format change
exp_form = re.compile('\d+.\d+[·*]10\d+')


# split in sentences and store in array
sentences = []
sentences = g.split(".")
for i in range(len(sentences)):
	sentences[i] += "."


appended = 0
for i in range(len(sentences)):
	value_find = front.search(sentences[i])
	temp_sentence = sentences[i]
	while value_find != None:
		if back.search(sentences[i+1]) != None:
			temp_sentence += sentences[i+1]
			del sentences[i+1]
			sentences.append('\n')
			appended += 1
			value_find = front.search(temp_sentence)
		else:
			value_find = None
	sentences[i] = temp_sentence

sentences.reverse()
for i in range(appended):
	del sentences[0]
sentences.reverse()


# Experimental / Simulation expectation
exp_crit = 0
sim_crit = 0
# Exp/Sim words
sim = re.compile('simulat', re.I)
exp = re.compile('experiment', re.I)
com = re.compile('computat', re.I)
ff = re.compile('force\s?-?\s?field', re.I)
mc = re.compile('monte\s?-?\s?carlo', re.I)
md = re.compile('molecular\s?-?\s?dynamics', re.I)

for i in range(len(sentences)):
	if sim.search(sentences[i]) != None:
		sim_crit += 1
	if exp.search(sentences[i]) != None:
		exp_crit += 1
	if com.search(sentences[i]) != None:
		sim_crit += 1
	if ff.search(sentences[i]) != None:
		sim_crit += 1
	if mc.search(sentences[i]) != None:
		sim_crit += 1
	if md.search(sentences[i]) != None:
		sim_crit += 1

#if exp_crit > sim_crit:
#	print ('This paper is Experiment paper\n')
#elif exp_crit == sim_crit:
#	print ('Cannot recongnize Exp/Sim\n')
#else:
#	print ('This paper is Simulation paper\n')

# Surface area search
# m2/g finding - m2/g criteria
unit = re.compile('cm3\s?/\s?g|cm3\s?\W?g\s?[−-]1|/\s?g\W?cm\s?[−-]3|mL\s?/\W?g\s?|mL\s?\W?g\s?[−-]1|cm3\W?cm\s?[−-]3|cm3\s?/\W?cm3\s?') # cm3/g criteria
range_prob = re.compile('\s?range\s?[-]?\s?of\s\d+\s?\W?\s?\d+|\s?excess\s?of\s?\d+|from\s?\d+\s?to\s?\d+\s?|from\s?\d+|over\s?\d+|\d+\s?~\s?\d+|\d+\s?–\s?\d+|as\s?high\s?as\s?\d+|∼\d+|[<>]\d+|\s?exceeding\s?\d+|\s?higher\s?than\s?\d+|\s?larger\s?than\s?\d+|theoretical\s?value\s?of\s?\d+', re.I)

print ('\n<Pore volume data in article>\n')
for i in range(len(sentences)):
	data_sentence = unit.findall(sentences[i])
	#if data_sentence != []:
		#print (sentences[i]) # m2/g sentence
		#print ("\n")
	unit_index = unit.finditer(sentences[i])
	value_list_total = []
	m2count = 0
	start = 0
	end = 0
	for match in unit_index:
		# Range sentence
		start = match.start()
		j = 20
		while (start - j) <= 0:
			j -= 1
		temp = sentences[i][start-j:start]
		range_sentence = range_prob.search(temp)
		if range_sentence != None:
			continue
		#Need Pore volume word!!
		j = 200
		while (start - j) <= 0:
			j -= 1
		temp = sentences[i][start-j:start]
		pore_sentence = Pore.search(temp)
		if pore_sentence == None:
			continue
		m2count += 1

		#print (match.group()) # m2/g
		#print (match.span()) # m2/g index in sentence
		temptext = str(match.group())
		if temptext.find('L') != -1 or temptext.find('l') != -1:
			unittext = 'mL/g'
		elif temptext.find('g'):
			unittext = 'cm3/g'
		else:
		 	unittext = 'cm3/cm3'


		value_count = 0
		value_list = []
		temp = sentences[i][0:match.start()].split()
		#print (temp)
		for j in range(len(temp)):
			if temp[j][-1:] == '\n':
				temp[j] = temp[j][:-1]
		temp.reverse()
		#print(temp)
		value = digit.search(temp[0])
		if value != None:
			if value.group() == '1':
				temp[0] = temp[0][value.end():]
				value = digit.search(temp[0])
		if value != None:
		# Exponental format
			exp_check = exp_form.search(temp[0])
			store_else = 0
			if exp_check != None:
				temp0 = exp_check.group()
				symb = 0
				for k in range(len(temp0)):
					if not temp0[k].isdigit():
						symb += 1
					if symb == 2:
						number_part = float(temp0[:k])
						exp_part = int(temp0[k+3:])
						break
				temp[0] = str(number_part * pow(10,exp_part))
				store_else = 1
			if temp[0].find('±' )== -1 and store_else == 0:
				value_list.append(value.group())
			elif temp[0].find('±' )== -1 and store_else == 1:
			   	value_list.append(temp[0])

			start = 0
			counter = 1
			none_counter=0
			while counter == 1:
				for j in range(2):
					if start + j + 1 < len(temp):
						value = digit.search(temp[start+j+1])
						if value != None:
							exp_check = exp_form.search(temp[start+j+1])
							if exp_check != None:
								temp1 = exp_check.group()
								symb = 0
								for k in range(len(temp1)):
									if not temp1[k].isdigit():
										symb += 1
									if symb == 2:
										number_part = float(temp1[:k])
										exp_part = int(temp1[k+3:])
										break
								temp1 = str(number_part * pow(10,exp_part))
								prt_thing = temp1
							else:
								temp1 = value.group()
								prt_thing = temp1
							not_store = 0
							isdigit = 1
							for l in range(len(temp1)):
								if temp1.find(',') != -1:
									temp2 = temp1.split(",")
									temp1 = ''
									for m in range(len(temp2)):
										temp1 += temp2[m]
									isdigit = 1

							for k in range(len(temp[start+j+1])):
								if temp[start+j+1][k].isalpha() == True:
									not_store = 1
							if not_store == 1:
								none_counter += 1
							else:

								value_list.append(prt_thing)
								t = start+j+1
						else:
							none_counter += 1
					else:
						counter = 0
						t = start
				if none_counter == 2:
					counter = 0
				else:
					none_counter = 0
					start = t
		else:
			print ("No_value before_unit_cm3/g")
		value_list.reverse()
		#print (value_list)
		for l in range(len(value_list)):
			dontadd = 0
			#Do not add same data in same sentence
			#if value_list_total != [] and m2count != 1:
			#	for m in range(len(value_list_total)):
			#		if value_list[l] == value_list_total[m]:
			#			dontadd = 0
			#Do not store data over 50
			if float(value_list[l]) > 50:
				dontadd = 1

			if dontadd == 0:
				if value_list[l][-1] == ',':
					value_list[l] = value_list[l][:-1]
				value_list_total.append(value_list[l])

	if data_sentence != []:
		#print (value_list_total)

		# surface type finding - BET/Langmuir
		Pore_all = Pore.findall(sentences[i])
		Pore_iter = Pore.finditer(sentences[i])
		BET_all = BET.findall(sentences[i])
		BET_iter = BET.finditer(sentences[i])
		Lang_all = Lang.findall(sentences[i])
		Lang_iter = Lang.finditer(sentences[i])
		Type = ['Pore']
		Type_index = []
		BBLL_type = 0
		BBLL = ''

		#print (value_list_total)
		# MOF name counter
		strange = 0
		special_case = 0
		if len(Type) == 0 or len(Type) == 1:
			MOF_name_counter = len(value_list_total);
		elif len(Type) == 2:
			if len(value_list_total) % 2 != 0:
				Type_total = BETLang.findall(sentences[i])
				if len(value_list_total) == len(Type_total):
					BET_count = 0
					Lang_count = 0
					BET_index = []
					Lang_index = []
					for j in range(len(Type_total)):
						if BET.search(Type_total[j]) != None:
							BET_count += 1
							Type_total[j] = 'Pore'
							BET_index.append(j)
						else:
							Lang_count += 1
							Type_total[j] = 'Pore'
							Lang_index.append(j)
					if BET_count > Lang_count:
						MOF_name_counter = BET_count
					else:
						MOF_name_counter = Lang_count
					special_case = 1
					BBLL_type = 0

				else:
					print ("Matching error!! even number of value needed")
					MOF_name_counter = round(len(value_list_total)/2)
					strange = 1
			else:
				if len(value_list_total) <= 2:
					BBLL_type = 0
				MOF_name_counter = int(len(value_list_total)/2);
		else:
			print ("more than two type of surface - Check MOF Type!")
		# Find MOF in sentence
		sentence_count = 0
		temp = []
		MOF_list = []
		MOF_index = []
		while MOF_name_counter != 0 and strange == 0:
			if i-sentence_count > 0:
				temp = sentences[i-sentence_count].split(" ")
				temp.reverse()
			for j in range(len(temp)):
				if temp[j][-1:] == '\n':
					temp[j] = temp[j][:-1]
			for j in range(len(temp)):
				already_stored = 0
				for k in range(len(MOF_in_Paper)):
					if temp[j].find(MOF_in_Paper[k]) != -1 and MOF_name_counter != 0 and already_stored != 1:
						MOF_list.append(temp[j])
						MOF_index.append(j)
						MOF_name_counter -= 1
						already_stored = 1
			if MOF_name_counter != 0:
				sentence_count += 1
				if sentence_count > 5:
					for k in range(MOF_name_counter):
						MOF_list.append("*IDK*")
					break
		MOF_list.reverse()
		MOF_index.reverse()
		for j in range(len(MOF_list)):
			if MOF_list[j][0] == '(' and MOF_list[j][-1] == ')':
				MOF_list[j] = MOF_list[j][1:-1]
			if MOF_list[j].find('(') * MOF_list[j].find(')') < 0:
				if MOF_list[j][0] == '(':
					MOF_list[j] = MOF_list[j][1:]
				if MOF_list[j][-1] == ')':
					MOF_list[j] = MOF_list[j][:-1]


		for j in range(len(MOF_list)):
			if MOF_list[j][-1] == "," or MOF_list[j][-1] == ";":
				MOF_list[j] = MOF_list[j][:-1]

		# additional criteria for BBLL
		for j in range(len(MOF_list) - 1):
			if sentences[i].find(MOF_list[j+1]) - sentences[i].find(MOF_list[j]) > 25:
				BBLL = 'BLBL'

		#print (MOF_list)
		#print (BBLL)
		# print ('\n')
		
		if special_case == 0:
			for k in range(len(value_list_total)):
				if len(Type) == 1 and strange == 0:
					Total_DATA.append([MOF_list[k],Type[0],value_list_total[k],unittext])
					print (MOF_list[k],"|",Type[0],"|",value_list_total[k],"|",unittext)
		elif special_case == 1 and strange == 0:
			if BET_count == len(MOF_list):
				for j in range(Lang_count):
					if Lang_index[j] == 0:
						text = MOF_list[0]
						MOF_list.insert(0,text)
					else:
						text = MOF_list[Lang_index[j]-1]
						MOF_list.insert(Lang_index[j],text)
				for k in range(len(value_list_total)):
					Total_DATA.append([MOF_list[k],Type_total[k],value_list_total[k],unittext])
					print (MOF_list[k],"|",Type_total[k],"|",value_list_total[k],"|",unittext)
			else:
				for j in range(BET_count):
					if BET_index[j] == 0:
						text = MOF_list[0]
						MOF_list.insert(0,text)
					else:
						text = MOF_list[BET_index[j]-1]
						MOF_list.insert(BET_index[j],text)
				for k in range(len(value_list_total)):
					Total_DATA.append([MOF_list[k],Type_total[k],value_list_total[k],unittext])
					print (MOF_list[k],"|",Type_total[k],"|",value_list_total[k],"|",unittext)


mof = ''
Main_MOF = ''
Secondary_MOF = ''
frequency = []

for i in range(len(Total_DATA)):
	mof = Total_DATA[i][0]
	mof_count = 0
	for j in range(len(sentences)):
		words = sentences[j].split()
		for j in range(len(words)):
			if words[j] == mof:
				mof_count += 1

	frequency.append(mof_count)
main_MOF_count = 0
main_MOF_index = []
for i in range(len(Total_DATA)):
	if frequency[i] == max(frequency):
		main_MOF_count += 1
		main_MOF_index.append(i)
#print ("\n")
#print ("<Main MOF of this paper>")
#print ("\n")
#for i in range(main_MOF_count):
#	print (Total_DATA[main_MOF_index[i]][0],Total_DATA[main_MOF_index[i]][1],Total_DATA[main_MOF_index[i]][2],Total_DATA[main_MOF_index[i]][3], frequency[main_MOF_index[i]])
