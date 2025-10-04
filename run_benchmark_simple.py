import os
import subprocess
import csv
import matplotlib.pyplot as plt
import argparse

def clean_page_cache():
    """
    Clean the system page cache using the sync command and writing to /proc/sys/vm/drop_caches
    Requires root privileges (sudo) to execute successfully
    """

    cmd = "sudo bash -c \"sync; echo 3 > /proc/sys/vm/drop_caches\""
    if verbose:
        print(cmd)
    os.system(cmd)

def run_benchmark(benchmark_path, draw=0):
    """
    Run benchmark tests on all .benchmark files in the specified directory

    Args:
        benchmark_path (str): Path to directory containing benchmark files
        draw (int): Flag to enable result plotting (1 = enable, 0 = disable)
    """
    # Verify the provided path is a valid directory

    if not os.path.isdir(benchmark_path):
        print(f"Error: {benchmark_path} is not a valid path")
        return


    # Get last two parts of the path to use as output filename

    path_parts = os.path.normpath(benchmark_path).split(os.sep)
    output_name = f"{path_parts[-2]}_{path_parts[-1]}"
    output_csv = "output/"+f"{output_name}.csv"

    results = []


    # Traverse through all files in the directory
    for root, dirs, files in os.walk(benchmark_path):
        # Sort files ending with .benchmark by numeric part in filename

        files = sorted([file for file in files if file.endswith('.benchmark')],
                       key=lambda x: int(x[1:3]))
        print(files)
        for file in files:
            if file.endswith('.benchmark'):

                # Construct full file path
                benchmark_file = os.path.join(root, file)

                # Execute benchmark command and capture output
                try:
                    # Build command with --disable-timeout parameter
                    cmd = f"{os.path.join(pixels_home, 'cpp/build/release/benchmark/benchmark_runner')} \"{benchmark_file}\" --disable-timeout --Nruns={nRuns}"
                    if verbose:
                        print(cmd)
                    output = subprocess.getoutput(cmd)


                    # Collect all run results

                    run_times = []
                    print(output)
                    for line in output.splitlines():
                        if line.startswith('Result:'):
                            time = float(line.split()[1])
                            run_times.append(time)
                            if verbose:

                                print(f"File {file} runtime: {time}")

                    # Save all run times if results exist
                    if run_times:
                        # Store filename and all run times
                        results.append((file, run_times))
                        if verbose:
                            print(f"File {file} results: {run_times}")
                    else:
                        if verbose:
                            print(f"No results found for file {file}")

                except Exception as e:
                    print(f"An error {e}  ocurred whne running {benchmark_file}")


    # Save results to CSV file
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write header: benchmark name + columns for each run
        max_runs = max(len(times) for _, times in results) if results else 0
        header = ['Benchmark'] + [f'Run {i+1} Time(s)' for i in range(max_runs)]
        writer.writerow(header)

        # Write all run results for each benchmark
        for file, times in results:
            # Ensure consistent column count per row

            row = [file] + times + [''] * (max_runs - len(times))
            writer.writerow(row)

    print(f"oupput has saved in {output_csv}")


    # Generate plot if requested

    if draw:
        plot_results(output_name, results)

def plot_results(title, results):

    """
    Generate a bar chart from benchmark results showing average run times

    Args:
        title (str): Title for the plot (used in chart title and filename)
        results (list): List of tuples containing (filename, run_times)
    """
    # Extract benchmark names and calculate average times
    benchmarks = [r[0].split('.')[0] for r in results]
    # Calculate average time for each benchmark
    avg_times = [sum(r[1])/len(r[1]) for r in results]

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.bar(benchmarks, avg_times, color='skyblue')
    plt.xlabel('Benchmarks')
    plt.ylabel('Average Time (s)')
    plt.title(f'{title} Results')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("output/"+f"{title}.png")
    plt.show()

    print(f"Chart saved as {title}.png")


if __name__ == "__main__":
    # Global variables for configuration
    global pixels_home
    global verbose
    global nRuns


    # Get PIXELS_SRC environment variable
    pixels_home = os.environ.get('PIXELS_SRC')
    current_dir = os.getcwd()
    # Create output directory if it doesn't exist
    os.makedirs(os.path.join(current_dir, "output"), exist_ok=True)

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Run benchmark tests and save results.")
    parser.add_argument('--dir', type=str, required=True, help='Directory containing benchmark files')
    parser.add_argument('--draw', type=int, default=0, choices=[0, 1],
                        help='Draw chart: 1 = yes, 0 = no (default: 0)')
    parser.add_argument('--from-page-cache', help='Whether to read files from page cache',
                        type=int, default=0, choices=[0,1])
    parser.add_argument('--v', dest='verbose', help='Output commands',
                        type=int, default=1, choices=[0,1])
    parser.add_argument('--nRuns', type=int, default=1, help='Number of times to run each benchmark')
    args = parser.parse_args()

    # Initialize configuration from arguments
    from_page_cache = args.from_page_cache
    verbose = args.verbose
    nRuns = args.nRuns


    # Clean page cache if not reading from cache

    if not from_page_cache:
        clean_page_cache()

    # Run benchmarks with provided arguments
    run_benchmark(args.dir, args.draw)


