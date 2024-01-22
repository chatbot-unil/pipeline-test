class Assistant:
    def __init__(self, client, name, instructions, tools, model, assistant_id=None, file_ids=None):
        self.client = client
        self.assistant_id = assistant_id
        self.name = name
        self.instructions = instructions
        self.tools = tools
        self.model = model
        self.file_ids = file_ids

    def create(self):
        assistant = self.client.beta.assistants.create(
            name=self.name,
            instructions=self.instructions,
            tools=self.tools,
            file_ids=self.file_ids,
            model=self.model
        )
        self.assistant_id = assistant.id

    def update(self, file_ids):
        self.client.beta.assistants.update(
            assistant_id=self.assistant_id,
            file_ids=file_ids
        )

    def delete(self):
        self.client.beta.assistants.delete(assistant_id=self.assistant_id)

