from src.core.agent import askAgent
from src.state.thread import Thread

def test_agent_run():
    thread = Thread()
    thread.addMessage("user", "Say hello")
    result = askAgent(thread)
    assert result is not None