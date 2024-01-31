import os
import argparse
import subprocess
import re
import matplotlib.pyplot as plt
import numpy as np
import csv


result_dict = {}

def clean_page_cache():
    cmd = "sudo /usr/local/etc/vm-drop_caches.sh"
    print(cmd)
    os.system(cmd)


def run_benchmark(benchmark_abs_path, query, benchmark_name):
    global result_dict

    cmd = os.path.join(pixels_home, "cpp/build/release/benchmark/benchmark_runner") + " " + benchmark_abs_path

    print(cmd)
    results =  subprocess.getoutput(cmd)
    pattern = '^[0-9]+\.[0-9]+$'
    found = False
    for result in results.split("\n"):
        if(re.match(pattern, result)):
            # if previously is already found, this means your benchmark might run the query several times
            if found:
                raise Exception("The benchmark is already run. Please make sure that DEFAULT_NRUNS in benchmark.hpp is 0 (which means the benchmark only runs 1 time) ")
            found = True
            print(benchmark_name + " " + query + " " + result)
            result = float(result)

            if benchmark_name not in result_dict.keys():
                result_dict[benchmark_name] = {}
            result_dict[benchmark_name][query] = result

    if not found:
        print("----------------------------------")
        print(results)
        raise Exception("The output is not expected!")

def generate_result(output_path, query_type):
    with open(os.path.join(output_path, 'result.csv'), 'w', newline='') as file:
        writer = csv.writer(file)
        field = [""]
        cols = []
        i = 0
        width = 0.6 / len(result_dict)

        for benchmark_name, result in result_dict.items():
            field.append(benchmark_name)

            x = list(result.keys())
            if len(cols) == 0:
                cols.append(x)

            y = list(result.values())
            cols.append(y)

            x_axis = np.arange(len(x))
            if i == 0:
                plt.figure().set_figwidth(max(5, len(x) * 0.25 * len(result_dict)))
                plt.bar(x_axis + width * i, y, width = width, tick_label = x, label = benchmark_name)
            else:
                plt.bar(x_axis + width * i, y, width = width, label = benchmark_name)
            i += 1

        print(cols)
        plt.legend()
        plt.title(query_type + " Performance of Pixels and Parquet")
        plt.xlabel(query_type + " query")
        plt.ylabel("execution time/s")
        plt.savefig(os.path.join(output_path, 'plot.png'))
        plt.clf()

        print(cols)
        rows = [list(i) for i in zip(*cols)]
        print(field)
        print(rows)

        writer.writerow(field)
        for row in rows:
            writer.writerow(row)

def main():
    global verbose
    global pixels_home
    pixels_home = os.environ.get('PIXELS_HOME')
    if pixels_home == None:
        print("You need to set $PIXELS_HOME first.")
        return

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-o', '--output_path', dest='output_path', default="", help='output path')
    parser.add_argument('-b','--benchmark', dest='benchmarks', nargs='+', help='benchmark name', required=True)
    parser.add_argument('-p','--path', dest='benchmarks_path', nargs='+', help='benchmark path', required=True)
    parser.add_argument('-t','--type', dest='query_type', help='the type of query', required=True)
    parser.add_argument('-l','--limit', dest='limit', default="-1", help="limit the query number to be compared. It is used for debug. ")

    args = parser.parse_args()

    os.makedirs(args.output_path, exist_ok=True)
    limit = int(args.limit)
    assert(len(args.benchmarks_path) == len(args.benchmarks))

    first_benchmark_path = args.benchmarks_path[0]
    first_files = os.listdir(first_benchmark_path)
    first_files = sorted(first_files)
    processed_query = 0
    for query_name in first_files:
        query_id = re.search(r'q[0-9]+', query_name).group(0)
        for i in range(len(args.benchmarks_path)):
            benchmark_path = args.benchmarks_path[i]
            benchmark_name = args.benchmarks[i]
            clean_page_cache()
            run_benchmark(os.path.join(benchmark_path, query_name), query_id, benchmark_name)
        processed_query += 1
        if limit >= 0 and processed_query >= limit:
            break
    print(result_dict)

    generate_result(args.output_path, args.query_type)


if __name__ == "__main__":
    main()
