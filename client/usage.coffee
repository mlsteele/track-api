# -- window shim --
global.window =
  '$': ajaxWithPrefix: -> console.log arguments
  location: href: 'http://localhost/'

setTimeout (-> window.onunload), 500

require './track'
track = window.track


# -- event emission --
track.update_context username: 'Miles'

track.event "Viewed sequential",
  seq_name: 'electrons'
  referrer: 'prev'
  seq_index: 4

window.onunload = ->
  track.event_sync 'page_close',
    msg: 'byebye'
