from track import default as track


# -- event registration --
with track.register("Lost socks") as evt:
    evt.require_data('color', kind=str)
    evt.require_data('smelly', choices=['nope', 'somewhat', 'very'])
    evt.require_data('days_old', validator=lambda x: x > 1)
    evt.require_context('username')


# -- event emission --
track.set_context({
    'username': 'Miles'
})

track.event("Lost socks", {
    'color': 'blue',
    'smelly': 'somewhat',
    'days_old': 4,
})
