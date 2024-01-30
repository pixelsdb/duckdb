#!/bin/bash

nvme=$1
dataset=$2

for file in /nvme${nvme}/liyu/pixels-data/${dataset}/customer/v-0-ordered/*
do
 for version in {0..1}
 do
    cp $file ${file}.${version}
 done
done

for file in /nvme${nvme}/liyu/pixels-data/${dataset}/lineitem/v-0-ordered/*
do
 for version in {0..1}
 do
    cp $file ${file}.${version}
 done
done

for file in /nvme${nvme}/liyu/pixels-data/${dataset}/orders/v-0-ordered/*
do
 for version in {0..1}
 do
    cp $file ${file}.${version}
 done
done

for file in /nvme${nvme}/liyu/pixels-data/${dataset}/part/v-0-ordered/*
do
 for version in {0..1}
 do
    cp $file ${file}.${version}
 done
done

for file in /nvme${nvme}/liyu/pixels-data/${dataset}/partsupp/v-0-ordered/*
do
 for version in {0..1}
 do
    cp $file ${file}.${version}
 done
done

for file in /nvme${nvme}/liyu/pixels-data/${dataset}/supplier/v-0-ordered/*
do
 for version in {0..1}
 do
    cp $file ${file}.${version}
 done
done