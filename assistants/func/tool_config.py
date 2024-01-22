from .add_file_to_the_assistant import FUNCTION as ADD_FILE_TO_THE_ASSISTANT
from .add_file_to_the_assistant import add_file_to_the_assistant

from .reload_assistant_with_only_proxy_file import FUNCTION as RELOAD_ASSISTANT_WITH_ONLY_PROXY_FILE
from .reload_assistant_with_only_proxy_file import reload_assistant_with_only_proxy_file

FUNCTIONS_TOOLS = [
	ADD_FILE_TO_THE_ASSISTANT,
	RELOAD_ASSISTANT_WITH_ONLY_PROXY_FILE,
]

FUNCTIONS_TO_HANDLE = {
    "add_file_to_the_assistant": add_file_to_the_assistant,
    "reload_assistant_with_only_proxy_file": reload_assistant_with_only_proxy_file,
}

TOOLS = [
    {"type": "code_interpreter"},
    {"type": "retrieval"},
]

TOOLS.extend(FUNCTIONS_TOOLS)
