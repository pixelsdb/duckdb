#!/bin/bash
for i in {0..30}
do
   echo $i
   for file in /nvme${i}/liyu/pixels-data/tpch-300-partition/lineitem/v-0-ordered/*
   do
     for version in {0..1}
     do
        cp $file ${file}.${version}
     done
   done

   for file in /nvme${i}/liyu/parquet-data/tpch-300-partition/lineitem/*
   do
     for version in {0..1}
     do
        cp $file ${file}_${version}
     done
   done
done
