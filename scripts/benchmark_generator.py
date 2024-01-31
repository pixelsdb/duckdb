from os import path, mkdir
import os
import argparse
import shutil


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-b', '--benchmark', dest='benchmark', required=True,
                        help='benchmark path. The base root is pixels-duckdb. ')
    parser.add_argument('-o', '--output', dest='output', required=True,
                        help='output path list')
    parser.add_argument('-n', '--num', dest='num', required=True,
                        help='number of query')
    args = parser.parse_args()

    benchmark = args.benchmark
    output_path = args.output
    print(output_path)
    if not path.exists(output_path):
        mkdir(output_path)
    for i in range(1, int(args.num) + 1):
        if i < 10:
            f = open(path.join(output_path, "q0" + str(i) + ".benchmark"), "w")
        else:
            f = open(path.join(output_path, "q" + str(i) + ".benchmark"), "w")

        f.writelines("template " + benchmark + "\n")
        if i < 10:
            f.writelines("QUERY_NUMBER_PADDED=0" + str(i) + "\n")
        else:
            f.writelines("QUERY_NUMBER_PADDED=" + str(i) + "\n")

if __name__ == "__main__":
    main()

