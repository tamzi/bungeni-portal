import events
import zope.component

def provide_transition_events_check(wf):
    event_map = dict(
        ((t.source, t.destination), False) for t in \
        events.get_workflow_transitions(wf) if t.event)

    for states, iface in events.workflow_transition_event_map.items():
        def generate(key):
            def handler(event):
                event_map[key] = True
            return handler
        zope.component.provideHandler(generate(states), adapts=(iface,))

    return event_map
