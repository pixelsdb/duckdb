import os
import argparse
import subprocess
import re
import matplotlib.pyplot as plt
import numpy as np

verbose = True
pixels_home = None
result_from_disk = {}
result_from_page_cache = {}


def clean_page_cache():
    cmd = "sudo /scratch/pixels-external/drop_cache.sh"
    if verbose:
        print(cmd)
    os.system(cmd)


def run_benchmark(benchmark_abs_path, query, engine, from_disk):
    global result_from_disk
    global result_from_page_cache
    cmd = os.path.join(pixels_home, "cpp/build/release/benchmark/benchmark_runner") + " " + benchmark_abs_path
    if verbose:
        print(cmd)
    # os.system(cmd)
    results =  subprocess.getoutput(cmd)
    pattern = '^[0-9]+\.[0-9]+$'
    found = False
    for result in results.split("\n"):
        if(re.match(pattern, result)):
            # if previously is already found, this means your benchmark might run the query several times
            if found:
                raise Exception("The benchmark is already run. Please make sure that DEFAULT_NRUNS in benchmark.hpp is 0 (which means the benchmark only runs 1 time) ")
            found = True
            print(engine + " " + query + " " + result)
            result = float(result)
            if(from_disk):
                if engine not in result_from_disk.keys():
                    result_from_disk[engine] = {}
                if query not in result_from_disk[engine].keys():
                    result_from_disk[engine][query] = []
                result_from_disk[engine][query].append(result)
            else:
                if engine not in result_from_page_cache.keys():
                    result_from_page_cache[engine] = {}
                if query not in result_from_page_cache[engine].keys():
                    result_from_page_cache[engine][query] = []
                result_from_page_cache[engine][query].append(result)

    if not found:
        print("----------------------------------")
        print(results)
        raise Exception("The output is not expected!")

def draw_disk():
    i = 0
    print("----------from disk--------------")

    for engine, result in result_from_disk.items():
        x = list(result.keys())
        y0 = list(result.values())
        y = []
        for result_list in y0:
            y.append(1.0 * sum(result_list) / len(result_list))
        x_axis = np.arange(len(x))
        if i == 0:
            plt.figure().set_figwidth(max(5, len(x) * 0.6))
            plt.bar(x_axis + 0.2 * i, y, width = 0.2, tick_label = x, label = engine)
        else:
            plt.bar(x_axis + 0.2 * i, y, width = 0.2, label = engine)
        i += 1
        print(engine)
        print(y)
    plt.legend()
    plt.title("benchmark performance from disk")
    plt.xlabel("tpch query")
    plt.ylabel("execution time/s")
    plt.savefig(os.path.join(pixels_home, 'cpp/plot/result_from_disk.png'))
    plt.clf()

def draw_page_cache():
    i = 0
    print("----------from page cache--------------")

    for engine, result in result_from_page_cache.items():
        x = list(result.keys())
        y0 = list(result.values())
        y = []
        for result_list in y0:
            y.append(1.0 * sum(result_list) / len(result_list))
        x_axis = np.arange(len(x))
        if i == 0:
            plt.figure().set_figwidth(max(5, len(x) * 0.6))
            plt.bar(x_axis + 0.2 * i, y, width = 0.2, tick_label = x, label = engine)
        else:
            plt.bar(x_axis + 0.2 * i, y, width = 0.2, label = engine)
        i += 1
        print(engine)
        print(y)
    plt.legend()
    plt.title("benchmark performance from page cache")
    plt.xlabel("tpch query")
    plt.ylabel("execution time/s")
    plt.savefig(os.path.join(pixels_home, 'cpp/plot/result_from_page_cache.png'))
    plt.clf()
def main():
    global verbose
    global pixels_home
    pixels_home = os.environ.get('PIXELS_HOME')
    if pixels_home == None:
        print("You need to set $PIXELS_HOME first.")
        return
    os.makedirs(os.path.join(pixels_home, "cpp/plot"), exist_ok=True)
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--pixels', dest='pixels_path', default="", help='benchmark path of pixels')
    parser.add_argument('--parquet', dest='parquet_path', default="", help='benchmark path of parquet')
    parser.add_argument('--from-page-cache', dest='from_page_cache', action='store_true', help='if reading file from page cache')
    parser.add_argument('-v', dest='verbose', action='store_true', help='output the command')
    parser.add_argument('--repeat-time-disk', dest='repeat_time_disk', type=int, default=1, help='The repeat time of disk')
    parser.add_argument('--repeat-time-page-cache', dest='repeat_time_page_cache', type=int, default=1, help='The repeat time of page cache')
    args = parser.parse_args()
    pixels_benchmark = args.pixels_path
    parquet_benchmark = args.parquet_path
    from_page_cache = args.from_page_cache
    verbose = args.verbose
    repeat_time_disk = args.repeat_time_disk
    repeat_time_page_cache = args.repeat_time_page_cache
    benchmark_list = []
    if pixels_benchmark != "":
        benchmark_list.append(["pixels", pixels_benchmark])
    if parquet_benchmark != "":
        benchmark_list.append(["parquet", parquet_benchmark])

    for benchmark in benchmark_list:
        benchmark_name = benchmark[0]
        benchmark_path = benchmark[1]
        files = os.listdir(benchmark_path)
        files = sorted(files)
        for benchmark_file in files:
            query = re.search(r'q[0-9]+', benchmark_file).group(0)
            benchmark_abs_path = os.path.join(benchmark_path, benchmark_file)
            for _ in range(repeat_time_disk):
                clean_page_cache()
                run_benchmark(benchmark_abs_path, query, benchmark_name, True)
            if(from_page_cache):
                for _ in range(repeat_time_page_cache):
                    run_benchmark(benchmark_abs_path, query, benchmark_name, False)

    clean_page_cache()
    print(result_from_disk)
    print(result_from_page_cache)

    draw_disk()
    if from_page_cache:
        draw_page_cache()


if __name__ == "__main__":
    main()
