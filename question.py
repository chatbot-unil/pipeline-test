import json
class Question:
	def __init__(self, question, answer):
		self.question = question
		self.answer_valid = answer
		self.answer = None
		self.valid = None

	def set_answer(self, answer):
		self.answer = answer
	
	def print_all(self):
		print(f"Question: {self.question}")
		print(f"Answer valid: {self.answer_valid}")
		print(f"Answer: {self.answer}")
		print(f"Valid: {self.valid}")
		print("")

	def evaluate(self):
		if self.answer_valid - 0.05 <= self.answer <= self.answer_valid + 0.05:
			return True
		return False
	
	def set_valid(self, valid):
		self.valid = valid
	
	def to_json(self):
		return {
			'question': self.question,
			'answer_valid': self.answer_valid,
			'answer': self.answer,
			'valid': self.valid
		}