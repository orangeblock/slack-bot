def generate_counter(start_at=0):
    """Creates a counter function that increments by 1 every time it is called"""
    d = {'counter': start_at}
    def inc():
        d['counter'] += 1
        return d['counter']
    return inc
