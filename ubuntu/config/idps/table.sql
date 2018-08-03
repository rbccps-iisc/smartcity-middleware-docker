CREATE TABLE logs
(
  id serial NOT NULL,
  logline text,
  hash text,
  CONSTRAINT logs_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE logs
  OWNER TO idps;
