import time
from pprint import pprint


class EventSchema(object):
    def __init__(self, event_name):
        self.event_name = event_name
        self.data_validators = {}
        self.context_validators = {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def _create_validators(self, validators, kind=None, choices=None, validator=None):
        """ `validators` is a list of validation functions """
        if kind != None:
            validators.append(lambda x: isinstance(x, kind))
        if choices != None:
            validators.append(lambda x: x in choices)
        if validator != None:
            validators.append(validator)
        return validators

    def require_data(self, field_name, kind=None, choices=None, validator=None):
        self.data_validators[field_name] = self._create_validators(
            self.data_validators.get(field_name, []),
            kind=kind,
            choices=choices,
            validator=validator,
        )

    def require_context(self, field_name, kind=None, choices=None, validator=None):
        self.context_validators[field_name] = self._create_validators(
            self.context_validators.get(field_name, []),
            kind=kind,
            choices=choices,
            validator=validator,
        )

    def validate(self, evt):
        for field_name in self.data_validators:
            for validator in self.data_validators[field_name]:
                if not field_name in evt['data']:
                    return False
                if not validator(evt['data'][field_name]):
                    return False

        for field_name in self.context_validators:
            if not field_name in evt['context']:
                return False
            for validator in self.context_validators[field_name]:
                if not validator(evt['context'][field_name]):
                    return False

        return True


class Track(object):
    def __init__(self):
        self.context = {}
        self.registered_events = {}

    def set_context(self, new_context):
        self.context = new_context

    def clear_context(self):
        self.context = {}

    def event(self, event_name, event_data):
        evt = self._encapsulate_event(event_name, event_data)
        if event_name in self.registered_events:
            schema = self.registered_events[event_name]
            if schema.validate(evt):
                evt['validated'] = True
            else:
                print("WARN: Invalid event.")
        else:
            print("WARN: Unregistered event.")
        pprint(evt)

    def register(self, event_name):
        schema = EventSchema(event_name)
        self.registered_events[event_name] = schema
        return schema

    def _encapsulate_event(self, event_name, event_data):
        return {
            'name': event_name,
            'timestamp': int(time.time() * 1000),
            'validated': False,
            'context': self.context,
            'data': event_data,
        }


default = Track()
