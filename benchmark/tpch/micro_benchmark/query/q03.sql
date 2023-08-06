SELECT
    o_orderkey,
    o_orderstatus,
    o_orderdate,
    o_clerk,
    o_comment
FROM
    orders
WHERE o_orderkey = 1;
