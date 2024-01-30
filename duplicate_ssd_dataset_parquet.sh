#!/bin/bash

nvme=$1
dataset=$2

for file in /nvme${nvme}/liyu/parquet-data/${dataset}/customer/*
do
 for version in {0..1}
 do
    cp $file ${file}.${version}
 done
done

for file in /nvme${nvme}/liyu/parquet-data/${dataset}/lineitem/*
do
 for version in {0..1}
 do
    cp $file ${file}.${version}
 done
done

for file in /nvme${nvme}/liyu/parquet-data/${dataset}/orders/*
do
 for version in {0..1}
 do
    cp $file ${file}.${version}
 done
done

for file in /nvme${nvme}/liyu/parquet-data/${dataset}/part/*
do
 for version in {0..1}
 do
    cp $file ${file}.${version}
 done
done

for file in /nvme${nvme}/liyu/parquet-data/${dataset}/partsupp/*
do
 for version in {0..1}
 do
    cp $file ${file}.${version}
 done
done

for file in /nvme${nvme}/liyu/parquet-data/${dataset}/supplier/*
do
 for version in {0..1}
 do
    cp $file ${file}.${version}
 done
done