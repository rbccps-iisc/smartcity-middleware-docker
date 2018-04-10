CREATE OR REPLACE FUNCTION add_hash()
  RETURNS trigger AS $$
DECLARE
    tab record;
    hash text;
    line text;
    prev cursor for select * from logs where id = (select max(id) from logs);
BEGIN
    tab=row(null);
    open prev;
    fetch prev into tab;
    if tab.hash is null then
    line=encode(hmac('smartcity','rbccps@123456','sha512'),'hex')||' '||new.logline;
    else
    line=tab.hash||' '||NEW.logline;
    end if;
    hash=encode(hmac(line,'rbccps@123456','sha512'),'hex');
    insert into logs(logline,hash) values(NEW.logline,hash);
    close prev;
    RETURN null;
END;
$$
LANGUAGE plpgsql

