import json
class Question:
	def __init__(self, question, answer):
		self.question = question
		self.answer_valid = answer
		self.answer = None
		self.valid = None

	def set_answer(self, answer):
		self.answer = answer

	def set_answer_valid(self, answer_valid):
		self.answer_valid = [0] * len(answer_valid)
		for i in range(len(answer_valid)):
			self.answer_valid[i] = answer_valid[i]
	
	def print_all(self):
		print(f"Question: {self.question}")
		print(f"Answer valid: {self.answer_valid}")
		print(f"Answer: {self.answer}")
		print(f"Valid: {self.valid}")
		print("")

	def evaluate(self):
		if self.answer is None:
			return False
		elif type(self.answer) is float:
			return self.answer - 0.05 <= self.answer_valid <= self.answer + 0.05
		else:
			ret = True 
			for i in range(len(self.answer)):
				if not (self.answer[i] - 0.05 <= self.answer_valid[i] <= self.answer[i] + 0.05):
					ret = False 
					break
			return ret
	
	def set_valid(self, valid):
		self.valid = valid
	
	def to_json(self):
		return {
			'question': self.question,
			'answer_valid': self.answer_valid,
			'answer': self.answer,
			'valid': self.valid
		}