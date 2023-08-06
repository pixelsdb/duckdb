SELECT
    ps_partkey,
    ps_availqty,
    ps_comment
FROM
    partsupp
WHERE ps_partkey = 1;
