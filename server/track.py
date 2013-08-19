import time
from pprint import pprint
from dictstack import DictStack


class Event(object):
    """
    Tracking event.

    Can be converted to json for storage with `.to_json`.
    Includes a boolean `validated` which defaults to False.
    """
    def __init__(self, name, data, context):
        self.name = name
        self.data = data
        self.context = context
        self.timestamp = int(time.time() * 1000)
        self.validated = False
        self.context = self.context

    def to_json(self):
        """ Convert to json. """
        return {
            'name': self.name,
            'timestamp': self.timestamp,
            'validated': self.validated,
            'context': self.context,
            'data': self.data,
        }


class EventSchema(object):
    """
    Schema for an event.

    Contains validators for fields in the event.
    EventSchema is meant to be used by a `with` block like this:
        with track.register("Viewed sequential") as evt:
            evt.require_data('seq_name', kind=str)
    where track.register returns an `EventSchema`.
    """

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
        if kind is not None:
            validators.append(lambda x: isinstance(x, kind))
        if choices is not None:
            validators.append(lambda x: x in choices)
        if validator is not None:
            validators.append(validator)
        return validators

    def require_data(self, field_name, kind=None, choices=None, validator=None):
        """
        Require `field_name` to be present in the data.
        Further validation keywords are optional.
        `kind` is a type of which the value must be `isinstance`.
        `choices` is a collection which the field value must be in.
        `validator` is a function which is passed the field value and must return a boolean.
        """
        self.data_validators[field_name] = self._create_validators(
            self.data_validators.get(field_name, []),
            kind=kind,
            choices=choices,
            validator=validator,
        )

    def require_context(self, field_name, kind=None, choices=None, validator=None):
        """
        Require `field_name` to be present in the context.
        Further validation keywords are optional.
        `kind` is a type of which the value must be `isinstance`.
        `choices` is a collection which the field value must be in.
        `validator` is a function which is passed the field value and must return a boolean.
        """
        self.context_validators[field_name] = self._create_validators(
            self.context_validators.get(field_name, []),
            kind=kind,
            choices=choices,
            validator=validator,
        )

    def validate(self, evt):
        """
        Check whether an event passes validation according to this schema.

        Returns a boolean.
        """
        # validate data
        for field_name in self.data_validators:
            for validator in self.data_validators[field_name]:
                if not field_name in evt.data:
                    return False
                if not validator(evt.data[field_name]):
                    return False

        # validate context
        for field_name in self.context_validators:
            if not field_name in evt.context:
                return False
            for validator in self.context_validators[field_name]:
                if not validator(evt.context[field_name]):
                    return False

        # TODO detect extra fields

        return True


class Track(object):
    """ Event tracking host. """
    def __init__(self):
        self.context = DictStack()
        self.registered_events = {}

    def clear_context(self):
        self.context = DictStack()

    def push_context(self, more_context):
        """ Add additional context or update existing context fields. """
        self.context.push(more_context)

    def pop_context(self):
        self.context.pop()

    def event(self, event_name, event_data):
        """
        Log an event.

        `event_name` is the type of the event as a string.
        `event_data` is the event payload.
        context is from this `Track` is added to the event.
        """
        evt = Event(event_name, event_data, self.context.get_dict())
        if evt.name in self.registered_events:
            schema = self.registered_events[evt.name]
            if schema.validate(evt):
                evt.validated = True
            else:
                print("WARN: Invalid event.")
        else:
            print("WARN: Unregistered event.")
        pprint(evt.to_json())

    def register(self, event_name):
        """
        Register an event type.

        Used by a with block like this:
            with track.register("Viewed sequential") as evt:
                evt.require_data('seq_name', kind=str)
        """
        schema = EventSchema(event_name)
        self.registered_events[event_name] = schema
        return schema


default = Track()
