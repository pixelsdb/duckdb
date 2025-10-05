import os
import shutil

def add_pragma_to_sql_files(source_dir, dest_dir):
    """
    在所有SQL文件开头添加PRAGMA disable_optimizer;
    并保持目录结构复制到新目录

    参数:
        source_dir: 源SQL文件目录
        dest_dir: 目标目录
    """
    # 确保源目录存在
    if not os.path.exists(source_dir):
        print(f"错误: 源目录 '{source_dir}' 不存在")
        return

    # 创建目标目录（如果不存在）
    os.makedirs(dest_dir, exist_ok=True)

    # 遍历源目录中的所有文件和子目录
    for root, dirs, files in os.walk(source_dir):
        # 为每个子目录在目标目录中创建对应的目录
        for dir_name in dirs:
            source_subdir = os.path.join(root, dir_name)
            relative_path = os.path.relpath(source_subdir, source_dir)
            dest_subdir = os.path.join(dest_dir, relative_path)
            os.makedirs(dest_subdir, exist_ok=True)

        # 处理每个SQL文件
        for file in files:
            if file.endswith('.sql'):
                # 构建源文件和目标文件的路径
                source_file = os.path.join(root, file)
                relative_path = os.path.relpath(root, source_dir)
                dest_file = os.path.join(dest_dir, relative_path, file)

                # 读取源文件内容
                with open(source_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 在内容开头添加PRAGMA语句
                new_content = f"PRAGMA disable_optimizer;\n{content}"

                # 写入目标文件
                with open(dest_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)

                print(f"已处理: {dest_file}")

    print(f"所有SQL文件处理完成，已保存至: {os.path.abspath(dest_dir)}")

if __name__ == "__main__":
    # 源目录和目标目录设置
    source_directory = "queries"
    destination_directory = "queries-withoutoptimizer"

    # 执行处理
    add_pragma_to_sql_files(source_directory, destination_directory)
