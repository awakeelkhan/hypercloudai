from src.core.events import AgentEvent
from src.core.event_stream import EventStream

def test_agent_state():
    stream = EventStream()

    event = AgentEvent("run_started", {"message": "test"})
    stream.emit(event)

    assert len(stream.getEvents()) == 1
    assert stream.getEvents()[0].eventType == "run_started"
    assert stream.getEvents()[0].data["message"] == "test"