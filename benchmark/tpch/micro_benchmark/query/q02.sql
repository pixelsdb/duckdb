SELECT
    l_partkey,
    l_linenumber,
    l_extendedprice,
    l_tax,
    l_linestatus,
    l_commitdate,
    l_shipinstruct
FROM
    lineitem
WHERE
    l_partkey = 1;
