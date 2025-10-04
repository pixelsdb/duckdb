import os
import subprocess
import csv
import matplotlib.pyplot as plt
import argparse

def clean_page_cache():
    cmd = "sudo bash -c \"sync; echo 3 > /proc/sys/vm/drop_caches\""
    if verbose:
        print(cmd)
    os.system(cmd)

def run_benchmark(benchmark_path, draw=0):
    # 确保路径是一个目录
    if not os.path.isdir(benchmark_path):
        print(f"错误: {benchmark_path} 不是一个有效的目录")
        return

    # 获取目录名的最后两部分作为输出文件名
    path_parts = os.path.normpath(benchmark_path).split(os.sep)
    output_name = f"{path_parts[-2]}_{path_parts[-1]}"
    output_csv = "output/"+f"{output_name}.csv"

    results = []

    # 遍历目录中的所有文件
    for root, dirs, files in os.walk(benchmark_path):
        # 按文件名排序
        files = sorted([file for file in files if file.endswith('.benchmark')],
                       key=lambda x: int(x[1:3]))
        print(files)
        for file in files:
            if file.endswith('.benchmark'):
                # 构建完整文件路径
                benchmark_file = os.path.join(root, file)

                # 运行命令并捕获输出
                try:
                    # 构建命令时添加--disable-timeout参数
                    cmd = f"{os.path.join(pixels_home, 'cpp/build/release/benchmark/benchmark_runner')} \"{benchmark_file}\" --disable-timeout --Nruns={nRuns}"
                    if verbose:
                        print(cmd)
                    output = subprocess.getoutput(cmd)

                    # 收集所有结果
                    run_times = []
                    print(output)
                    for line in output.splitlines():
                        if line.startswith('Result:'):
                            time = float(line.split()[1])
                            run_times.append(time)
                            if verbose:
                                print(f"文件 {file} 运行时间: {time}")

                    # 如果有结果，保存所有运行时间
                    if run_times:
                        # 存储文件名和所有运行时间
                        results.append((file, run_times))
                        if verbose:
                            print(f"文件 {file} 结果: {run_times}")
                    else:
                        if verbose:
                            print(f"文件 {file} 未找到结果")
                except Exception as e:
                    print(f"运行 {benchmark_file} 时出错: {e}")

    # 保存结果到CSV
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # 写入表头：基准测试名称 + 多次运行的结果列
        max_runs = max(len(times) for _, times in results) if results else 0
        header = ['基准测试'] + [f'运行{i+1}时间(s)' for i in range(max_runs)]
        writer.writerow(header)

        # 写入每个基准测试的所有运行结果
        for file, times in results:
            # 确保每行的列数相同
            row = [file] + times + [''] * (max_runs - len(times))
            writer.writerow(row)

    print(f"结果已保存到 {output_csv}")

    # 如果请求则绘制结果
    if draw:
        plot_results(output_name, results)

def plot_results(title, results):
    # 提取文件名和平均时间（使用平均值进行绘图）
    benchmarks = [r[0].split('.')[0] for r in results]
    # 计算每个基准测试的平均时间
    avg_times = [sum(r[1])/len(r[1]) for r in results]

    # 绘制结果
    plt.figure(figsize=(10, 6))
    plt.bar(benchmarks, avg_times, color='skyblue')
    plt.xlabel('基准测试')
    plt.ylabel('平均时间 (s)')
    plt.title(f'{title} 的结果')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("output/"+f"{title}.png")
    plt.show()
    print(f"图表已保存为 {title}.png")

if __name__ == "__main__":
    global pixels_home
    global verbose
    global nRuns

    pixels_home = os.environ.get('PIXELS_SRC')
    current_dir = os.getcwd()
    os.makedirs(os.path.join(current_dir, "output"), exist_ok=True)

    # 使用argparse处理命令行参数
    parser = argparse.ArgumentParser(description="运行基准测试并保存结果。")
    parser.add_argument('--dir', type=str, required=True, help='包含基准测试文件的目录')
    parser.add_argument('--draw', type=int, default=0, choices=[0, 1], help='绘制图表：1表示是，0表示否（默认：0）')
    parser.add_argument('--from-page-cache', help='是否从页面缓存读取文件', type=int, default=0, choices=[0,1])
    parser.add_argument('--v', dest='verbose', help='输出命令', type=int, default=1, choices=[0,1])
    parser.add_argument('--nRuns', type=int, default=1, help='runTimes')
    args = parser.parse_args()

    from_page_cache = args.from_page_cache
    verbose = args.verbose
    nRuns=args.nRuns


    if not from_page_cache:
        clean_page_cache()

    run_benchmark(args.dir, args.draw)


