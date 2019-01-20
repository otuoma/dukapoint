/*Remove key index to avoid 'Duplicate entry' errors on BranchProduct model for MySQL databases*/
ALTER TABLE products_branchproduct DROP INDEX product_id