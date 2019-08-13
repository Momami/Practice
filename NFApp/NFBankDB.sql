USE [NFBankDB]
GO

CREATE TABLE account_status(
	id integer NOT NULL PRIMARY KEY IDENTITY(1,1),
	name varchar(7) NOT NULL
);
GO

CREATE TABLE object_type(
	id integer NOT NULL PRIMARY KEY IDENTITY(1,1),
	otype varchar(7) NOT NULL
);
GO

CREATE TABLE audit_action(
	id integer NOT NULL PRIMARY KEY IDENTITY(1,1),
	a_action varchar(6) NOT NULL
);
GO

CREATE TABLE client(
	id bigint NOT NULL PRIMARY KEY,
	username varchar(20) NOT NULL UNIQUE,
	[password] varchar(30) NOT NULL,
	birth_date date NOT NULL,
	name varchar(30) NOT NULL,
	surname varchar(30) NOT NULL
);
GO

CREATE TABLE account(
	id bigint NOT NULL PRIMARY KEY,
	balance float  NOT NULL,
	open_date date  NOT NULL,
	close_date date,
	id_client bigint NOT NULL FOREIGN KEY REFERENCES client(id),
	[status] integer NOT NULL FOREIGN KEY REFERENCES account_status(id)
);
GO

CREATE TABLE [audit](
	id bigint NOT NULL PRIMARY KEY IDENTITY(1,1), 
	[object_id] bigint NOT NULL,
	object_type integer NOT NULL FOREIGN KEY REFERENCES object_type(id),
	action_date date  NOT NULL,
	action_id integer NOT NULL FOREIGN KEY REFERENCES audit_action(id),
	new_value XML
);
GO


INSERT INTO account_status(name) 
VALUES ('open'), ('closed'), ('suspend');
go

INSERT INTO object_type(otype) 
VALUES ('client'), ('account');
go

INSERT INTO audit_action(a_action) 
VALUES ('create'), ('update'), ('delete');
go

DROP TABLE [account]
DROP TABLE [audit]
DROP TABLE client
drop table audit_action
drop table account_status
drop table object_type
GO

