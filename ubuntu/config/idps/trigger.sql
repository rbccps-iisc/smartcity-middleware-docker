CREATE TRIGGER add_hash_trigger
BEFORE INSERT
ON logs
FOR EACH ROW
WHEN (pg_trigger_depth() = 0)
EXECUTE PROCEDURE add_hash();