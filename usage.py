from track import default as track


# -- event registration --
with track.register("Viewed sequential") as evt:
    evt.require_data('seq_name', kind=str)
    evt.require_data('referrer', choices=['prev', 'next', 'other'])
    evt.require_data('seq_index', validator=lambda x: x > 1)
    evt.require_context('username')


# -- event emission --
track.set_context({
    'username': 'Miles'
})

track.event("Viewed sequential", {
    'seq_name': 'electrons',
    'referrer': 'prev',
    'seq_index': 4,
})