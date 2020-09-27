from model import *


logging.basicConfig(filename='app.log', level=logging.INFO)
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler(sys.stdout))

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
    logger.info(f'Added quote for book: {quote.book}; author: {quote.author}')

for quote in quotes:
    logger.info(f'Do something with this quote')
