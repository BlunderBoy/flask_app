--studenti
CREATE TABLE studenti
(
	id             numeric,
	nume           varchar(45) NOT NULL,
	prenume        varchar(45) NOT NULL,
	id_clasa       numeric NOT NULL,
	email          varchar(45) NOT NULL,
	nr_telefon     varchar(45) NOT NULL,
	anul_inrolarii date NOT NULL,
	data_nasterii  date NOT NULL,
	primary key(id)
);







