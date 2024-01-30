#!/bin/bash

declare -a arr=("/nvme1" "/nvme2" "/nvme3" "/nvme4" "/nvme5" "/nvme6" "/nvme7" "/nvme9" "/nvme10" "/nvme11" "/nvme14" "/nvme15" "/nvme16" "/nvme17" "/nvme18" "/nvme19" "/nvme20" "/nvme21" "/nvme22" "/nvme23" "/nvme24" "/nvme25" "/nvme26"，"/nvme26", "/nvme27")

dataset="fuck you"

for root in "${arr[@]}"
do
   echo $root
   echo $root/liyu/pixels-data/$dataset
   echo $root/liyu/parquet-data/$dataset
   cp -r /nvme0/liyu/pixels-data/clickbench-e2 $root/liyu/pixels-data/clickbench-e2
   #cp -r /nvme0/liyu/parquet-data/clickbench-e0 $root/liyu/parquet-data/clickbench-e0
done
