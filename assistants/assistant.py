import enum

class Role(enum.Enum):
	ASSISTANT = 'assistant'
	USER = 'user'

class Thread:
	def __init__(self):
		self.thread_id = None

class Assistant:
	def __init__(self):
		self.assistant_id = None
		self.assistant_name = None
		self.instructions = None
		self.tools = None
		self.file_ids = None

class Message:
	def __init__(self):
		self.message_id = None
		self.thread_id = None
		self.role = None
		self.content = None
		self.assistant_id = None
		self.run_id = None
		self.file_ids = None
	
class Run:
	def __init__(self):
		self.run_id = None
		self.thread_id = None
		self.assistant_id = None
		self.status = None
		self.file_ids = None