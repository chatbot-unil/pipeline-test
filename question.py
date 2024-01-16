class Question:
	def __init__(self, question, answer):
		self.question = question
		self.answer_valid = answer
		self.answer = None

	def set_answer(self, answer):
		self.answer = answer
	
	def print_all(self):
		print(f"Question: {self.question}")
		print(f"Answer valid: {self.answer_valid}")
		print(f"Answer: {self.answer}")
		print("")