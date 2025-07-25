#!/usr/bin/env python
# coding: utf-8

import argparse, os, sys
import pandas as pd
import pyarrow.parquet as pq
from sqlalchemy import create_engine
from time import time


def main(params):
	user = params.user
	password = params.password
	host = params.host
	port = params.port
	db = params.db
	table_name = params.table_name
	url = params.url

	file_name = url.rsplit('/', 1)[-1].strip()
	print(f'Downloading {file_name}...')

	os.system(f"curl {url.strip()} -o {file_name}")
	print("\n")

	engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

	if ".csv" in file_name:
		df = pd.read_csv(file_name, nrows=10)
		df_iter = pd.read_csv(file_name, iterator=True, chunksize=100000)
	elif '.parquet' in file_name:
		file = pq.ParquetFile(file_name)
		df = next(file.iter_batches(batch_size=10)).to_pandas()
		df_iter = file.iter_batches(batch_size=100000)
	else:
		print('Error. Only .csv or .parquet files allowed.')
		sys.exit()


	df.head(0).to_sql(name=table_name, con=engine, if_exists='replace')

	t_start = time()
	count = 0

	for batch in df_iter:
		count += 1

		if ".parquet" in file_name:
			batch_df = batch.to_pandas()
		else:
			batch_df = batch

		print(f"inserting batch {count}...")

		b_start = time()
		batch_df.to_sql(name=table_name, con=engine, if_exists='append')
		b_end = time()

		print(f"Inserted! time taken {b_end - b_start:10.3f} seconds.\n")

	t_end = time()
	print(f"Completed! total time taken {t_end - t_start:10.3f} seconds for {count} batches")



if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='Ingest Parquet data to postgres')

	# user, password, host, port, database name, table name, url of the parquet.

	parser.add_argument('--user', help='user name for postgres')
	parser.add_argument('--password', help='password for postgres')
	parser.add_argument('--host', help='host name for postgres')
	parser.add_argument('--port', help='port for postgres')
	parser.add_argument('--db', help='database name for postgres')
	parser.add_argument('--table_name', help='table name for postgres')
	parser.add_argument('--url', help='url or the parquet')

	args = parser.parse_args()

	main(args)