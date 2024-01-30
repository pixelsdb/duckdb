import os
import argparse
import pyarrow.parquet as pq

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--input', dest='input_path', default="", help='the path of input parquet file')
    parser.add_argument('--output', dest='output_path', default="", help='the path of output parquet file')
    args = parser.parse_args()
    parquet_path = args.input_path

    for file in os.listdir(parquet_path):
        file_path = os.path.join(parquet_path, file)
        output_file_path = os.path.join(args.output_path, file)
        parquet_file = pq.ParquetFile(file_path)
        table = parquet_file.read()
        pq.write_table(table, output_file_path, use_dictionary=False, compression="NONE", column_encoding="PLAIN")
        print(file_path)
        print(output_file_path)

if __name__ == "__main__":
    main()
