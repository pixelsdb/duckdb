import os

# 定义基础路径和数据表
base_path = "/data"
ssd_prefix = "9a3-"
ssd_start = 1
ssd_end = 24
pixel_dirs = ["orders", "customer", "nation", "part", "partsupp", "lineitem", "supplier", "region"]

# 输出路径模板
output_template = "{}/{}-{:02d}/tpch-300/pixels_ssd/{}/v-0-ordered/*.pxl"

# 生成 CREATE VIEW 语句
for pixel_dir in pixel_dirs:
    view_name = pixel_dir.lower()
    paths = [output_template.format(base_path, ssd_prefix, i, pixel_dir) for i in range(ssd_start, ssd_end + 1)]
    paths_str = ', '.join(f'"{path}"' for path in paths)

    create_view_sql = f"""
CREATE VIEW {view_name} AS SELECT * FROM pixels_scan([
{paths_str}
]);
"""

print(create_view_sql)
