class Quote:
    def __init__(self, data):
        self._book = data[0]
        self._author = data[0]
        self._metadata = Metadata(data[2])
        self._text = data[3]


class Metadata:
    def __init__(self, data):
        self._page = data[0]
        self._location = data[0]
        self._timestamp = data[0]


block = []
clips = []
f = open('My Clippings.txt', 'r')
for line in f:
    if line.startswith('='):
        clips.append(block)
        block = []
    else:
        block.append(line)

f.close()

quotes = []
for clip in clips:
    quote = Quote(clip)
    quotes.append(quote)
    print(quotes[0]._book)