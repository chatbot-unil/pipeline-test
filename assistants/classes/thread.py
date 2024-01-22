import json

class Thread:
    def __init__(self, client, thread_id=None):
        self.client = client
        self.thread_id = thread_id

    def create(self):
        thread = self.client.beta.threads.create()
        self.thread_id = thread.id

    def send_message(self, message, role):
        self.client.beta.threads.messages.create(
            thread_id=self.thread_id,
            role=role.value,
            content=message
        )

    def get_messages(self):
        if self.thread_id:
            return self.client.beta.threads.messages.list(
                thread_id=self.thread_id
            )
        else:
            raise ValueError("Thread ID is not set. Create or set a thread ID first.")