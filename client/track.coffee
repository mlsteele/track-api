class Track
  constructor: ->
    @context = {}

  set_context: (new_context) ->
    @context = new_context

  add_context: (more_context) ->
    @context[k] = v for k, v of more_context

  clear_context: ->
    @context = {}

  event: (event_name, event_data) ->
    @_event(event_name, event_data, true)

  # synchronous version of @event
  event_sync: (event_name, event_data) ->
    @_event(event_name, event_data, false)

  _event: (event_name, event_data, async) ->
    evt_obj =
      name: event_name
      data: event_data
      context: @context
      client_timestamp: new Date().getTime()
      client_validated: no

    $.ajaxWithPrefix
      url: "/event"
      data: event: JSON.stringify evt_obj
      async: async

default_track = new Track
window?.track.add_context url: window.location.href

if exports?
  exports.track = default_track
else
  window.track = default_track
