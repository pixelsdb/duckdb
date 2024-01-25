#!/bin/bash

declare -a arr=("/nvme0" "/nvme2" "/nvme3" "/nvme4" "/nvme5" "/nvme6" "/nvme7" "/nvme9" "/nvme10" "/nvme11" "/nvme13" "/nvme14" "/nvme15" "/nvme16" "/nvme17" "/nvme18" "/nvme19" "/nvme20" "/nvme21" "/nvme22" "/nvme23" "/nvme24" "/nvme25" "/nvme26")


for root in "${arr[@]}"
do
   echo $root
   echo $root/liyu/pixels-data/clickbench
   echo $root/liyu/parquet-data/clickbench
   cp -r /nvme1/liyu/pixels-data/clickbench $root/liyu/pixels-data/clickbench
   cp -r /nvme1/liyu/parquet-data/clickbench $root/liyu/parquet-data/clickbench
done
