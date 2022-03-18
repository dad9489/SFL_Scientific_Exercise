DROP TABLE IF EXISTS SFL_DATA;
CREATE TABLE IF NOT EXISTS SFL_DATA (
    id NUMERIC NOT NULL,
    first_name VARCHAR(40),
    last_name VARCHAR(40),
    email VARCHAR(40),
    gender VARCHAR(40),
    ip_address inet
);