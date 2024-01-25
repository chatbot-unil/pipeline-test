import json
import time
from .thread import Thread

class Run:
    def __init__(self, client, thread_id, assistant_id):
        self.client = client
        self.thread_id = thread_id
        self.assistant_id = assistant_id
        self.run_id = None
        self.status = None

    def start(self):
        run = self.client.beta.threads.runs.create(
            thread_id=self.thread_id,
            assistant_id=self.assistant_id
        )
        self.run_id = run.id
        self.status = run.status

    def execute_and_monitor(self, functions_to_handle):
        while self.status in ["in_progress", "queued", "requires_action"]:
            time.sleep(1)
            self.update_status()

            if self.status == "completed":
                break

            if self.status == "requires_action":
                self.handle_required_actions(functions_to_handle)

    def update_status(self):
        run = self.client.beta.threads.runs.retrieve(
            thread_id=self.thread_id,
            run_id=self.run_id
        )
        self.status = run.status

    def handle_required_actions(self, functions_to_handle):
        run = self.client.beta.threads.runs.retrieve(
            thread_id=self.thread_id,
            run_id=self.run_id
        )
        tools_output = []
        print(run.required_action.submit_tool_outputs.tool_calls)
        for tool_call in run.required_action.submit_tool_outputs.tool_calls:
            function_name = tool_call.function.name
            function_to_handle = functions_to_handle.get(function_name)
            if function_to_handle:
                arguments = json.loads(tool_call.function.arguments)
                arguments['assistant_id'] = self.assistant_id
                result = function_to_handle(**arguments)
                tools_output.append({
                    "tool_call_id": tool_call.id,
                    "output": result,
                })

        self.client.beta.threads.runs.submit_tool_outputs(
            thread_id=self.thread_id,
            run_id=self.run_id,
            tool_outputs=tools_output
        )
