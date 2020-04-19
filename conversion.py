# Python program to convert infix expression to postfix 
import re
# Class to convert the expression 
class Conversion: 
	
	# Constructor to initialize the class variables 
	def __init__(self, query): 
		self.query = query
		self.top = -1
		self.array = [] #buat isi stack nya
		self.postfix = [] 
		self.prioritas = {'not':1, 'and':2, 'or':2}

	# check if the stack is empty 
	def isEmpty(self): 
		return self.top == -1
	
	# Return the value of the top of the stack 
	def peek(self): 
		return self.array[-1] 
	
	# Pop the element from the stack 
	def pop(self): 
		if self.isEmpty() == False: 
			self.top -= 1
			return self.array.pop() 
	
	# Push the element to the stack 
	def push(self, el): 
		self.top += 1
		self.array.append(el) 

	# A utility function to check is the given character 
	# is operand

	def isChars(self, cha):
		ops = {"not", "and", "or", "(", ")"}
		return cha not in ops

	# Check if the precedence of operator is strictly 
	# less than top of stack or not 
	def notGreater(self, i): 
		try: 
			return self.prioritas[i] <= self.prioritas[self.peek()]
		except KeyError:  
			return False

	def splitted(self, word):
		return list(filter(lambda x : x != " ", re.split(r"\b",word)))

	# def infixToPostfix(self, query): 
		
	# 	# Iterate over the expression for conversion
	# 	words = self.splitted(query)
	# 	print(words)
	# 	for word in words: 
	# 		if self.isChars(word): 
	# 			self.postfix.append(word) #kalo bukan operator masukin ke postfix
	# 		elif word == '(': 
	# 			self.push(word) #masukin ke stack nya 
	# 		elif word == ')': #kalo ketemu ini pop semua sampe ketemu (
	# 			while(self.isEmpty() == False and self.peek() != '('): 
	# 				x = self.pop() 
	# 				self.postfix.append(x) 
	# 			if (self.isEmpty() == False and self.peek() != '('): #apaini???
	# 				return -1
	# 			else: 
	# 				self.pop() 

	# 		else: #ngecek operator nya
	# 			while(not self.isEmpty() and self.notGreater(word)): 
	# 				self.postfix.append(self.pop()) 
	# 			self.push(word) 

	# 	# pop all the operator from the stack 
	# 	while self.isEmpty() == False: 
	# 		self.postfix.append(self.pop()) 

	# 	print(" ".join(self.postfix)) 


	def infixToPostfix(self, query):
		words = self.splitted(query)
#         print(words)
		for word in words:
			if self.isChars(word): 
				self.postfix.append(word) #kalo bukan operator masukin ke postfix
			elif word == '(': 
				self.push(word) #masukin ke stack nya 
			elif word == ')': #kalo ketemu ini pop semua sampe ketemu (
				while(self.isEmpty() == False and self.peek() != '('): 
					x = self.pop() 
					self.postfix.append(x) 
				if (self.isEmpty() == False and self.peek() != '('): #apaini???
					return -1
				else: 
					self.pop() 
			else: #ngecek operator nya
				while(self.isEmpty() == False and self.notGreater(word)): 
					self.postfix.append(self.pop()) 
				self.push(word)
		while self.isEmpty() == False: 
			self.postfix.append(self.pop())
		
#         return self.array
		return print(" ".join(self.postfix))

query = "nasi and ayam not(daging or telur)"
query2 = "(ayam and goreng)and ijo"
obj = Conversion(query)
obj.infixToPostfix(query2)

# This code is contributed by Nikhil Kumar Singh(nickzuck_007) mix bela
