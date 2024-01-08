import os
from python_helpers import open_utf8

def format_tpch_queries(target_dir, tpch_in, comment):
	with open_utf8(tpch_in, 'r') as f:
		text = f.read()

	for i in range(1, 44):
		qnr = '%02d' % (i,)
		target_file = os.path.join(target_dir, 'q' + qnr + '.benchmark')
		new_text = '''# name: %s
# description: Run query %02d from the clickbench benchmark (%s)

template %s
QUERY_NUMBER=%d
QUERY_NUMBER_PADDED=%02d''' % (target_file, i, comment, tpch_in, i, i)
		with open_utf8(target_file, 'w+') as f:
			f.write(new_text)

# generate the clickbench benchmark files
single_threaded_dir = os.path.join('benchmark', 'clickbench')
single_threaded_in = os.path.join(single_threaded_dir, 'clickbench-parquet.benchmark.in')
format_tpch_queries(os.path.join(single_threaded_dir, 'parquet'), single_threaded_in, '')
