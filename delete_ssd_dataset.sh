#!/bin/bash
for i in {0..30}
do
   rm -r /nvme${i}/liyu/pixels-data/tpch-300-partition
   rm -r /nvme${i}/liyu/parquet-data/tpch-300-partition
done