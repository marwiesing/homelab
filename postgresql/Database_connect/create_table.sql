CREATE TABLE person (
    id SERIAL PRIMARY KEY, 
    txforename VARCHAR(64), 
    txlastname VARCHAR(64), 
    dtbirthdate TIMESTAMP, 
    idgender int,
    dtcreatedate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    idcreatedby INT,
    dtchangedate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    idchangedby INT,
    idstate INT, 
    istate INT
);

INSERT INTO person (txforename, txlastname, dtbirthdate, idgender, dtcreatedate, idcreatedby, dtchangedate, idchangedby, idstate, istate)
VALUES ('Martin', 'Wiesinger', '1984-12-11', CURRENT_TIMESTAMP, 1, 1, CURRENT_TIMESTAMP, 1, 1, 1);

INSERT INTO person (txforename, txlastname, dtbirthdate, idgender, dtcreatedate, idcreatedby, dtchangedate, idchangedby, idstate, istate)
VALUES ('Karin', 'Wiesinger', '1989-07-14', CURRENT_TIMESTAMP, 2, 1, CURRENT_TIMESTAMP, 1, 1, 1);


