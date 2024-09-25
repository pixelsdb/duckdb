import pandas as pd
import matplotlib.pyplot as plt
import os

# 目录路径（你可以根据你的情况修改）
directory = './'

# 获取目录下所有CSV文件
csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]

# 定义颜色列表，每个文件的柱状图用不同的颜色
colors = ['skyblue', 'orange', 'green', 'red', 'purple', 'yellow', 'cyan', 'pink', 'gray', 'brown']


x_labels = [f'q{i}' for i in range(1, 23)]

# 创建一个位置索引对应每个 q 的位置
x = range(1,len(x_labels)+1)
# 创建一个图表
plt.figure(figsize=(14, 8))

# 遍历所有CSV文件并绘制柱状图
for i, file in enumerate(csv_files):
    file_path = os.path.join(directory, file)
    data = pd.read_csv(file_path)
    data['Benchmark'] = pd.to_numeric(data['Benchmark'].str.extract(r'(\d+)', expand=False), errors='coerce')
    # 绘制柱状图，每个文件的柱状图都有不同的偏移，避免重叠
    plt.bar(data['Benchmark'] + i * 0.2, data['Result'], width=0.2, color=colors[i % len(colors)], label=file)

# 添加图例
plt.legend(title='CSV Files', bbox_to_anchor=(1.05, 1), loc='upper left')




plt.xticks(x, x_labels)
# 添加标题和标签
plt.title('Benchmark Results Comparison Across CSV Files')
plt.xlabel('Benchmark')
plt.ylabel('Result')

# 保存图像
plt.tight_layout()
plt.savefig('benchmark_comparison.png')

# 显示图形
plt.show()

