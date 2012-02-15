import ystockquote
import numpy
from datetime import *
from pylab import figure, show
from matplotlib.ticker import Formatter


def stock_plot(symbol, start, end):

	# Fetch data
	raw = ystockquote.get_historical_prices(symbol, start, end)

	# First row is header
	headers = tuple(raw.pop(0))

	# Some funly sort
	raw.sort(key=lambda x: x[0])

	# Convert first column to datetime
	for row in raw:
		row[0] = datetime.strptime(row[0], '%Y-%m-%d')

	# Create records
	r = numpy.core.records.fromrecords(raw, names=headers)

	class MyFormatter(Formatter):
		def __init__(self, dates, fmt='%Y-%m-%d'):
			self.dates = dates
			self.fmt = fmt

		def __call__(self, x, pos=0):
			'Return the label for time x at position pos'
			ind = int(round(x))
			if ind>=len(self.dates) or ind<0: return ''

			return self.dates[ind].strftime(self.fmt)

	formatter = MyFormatter(r.Date)

	fig = figure()
	ax = fig.add_subplot(111)
	ax.grid()
	ax.set_title(symbol)
	ax.xaxis.set_major_formatter(formatter)
	ax.plot(numpy.arange(len(r)), r.Close, '-')
	fig.autofmt_xdate()
	show()

stock_plot('ERIC-B.ST', '20100101', '20120101')
