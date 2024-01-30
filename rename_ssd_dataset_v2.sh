#!/bin/bash

declare -a arr=("/nvme1" "/nvme2" "/nvme3" "/nvme4" "/nvme5" "/nvme6" "/nvme7" "/nvme9" "/nvme10" "/nvme11" "/nvme27" "/nvme14" "/nvme15" "/nvme16" "/nvme17" "/nvme18" "/nvme19" "/nvme20" "/nvme21" "/nvme22" "/nvme23" "/nvme24" "/nvme25" "/nvme26")

dataset=$1
renamed_dataset=$2
for root in "${arr[@]}"
do
   echo $root/liyu/pixels-data/$dataset
   mv $root/liyu/pixels-data/$dataset $root/liyu/pixels-data/${renamed_dataset}
   mv $root/liyu/parquet-data/$dataset $root/liyu/parquet-data/${renamed_dataset}
done
