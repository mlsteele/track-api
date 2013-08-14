# -- window shim --
global.window =
  '$': ajaxWithPrefix: -> console.log arguments
  location: href: 'http://localhost/'

require './track'
track = window.track


# -- event emission --
track.add_context username: 'Miles'

track.event "Viewed sequential",
  seq_name: 'electrons'
  referrer: 'prev'
  seq_index: 4
