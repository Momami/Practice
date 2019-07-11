USE [ValuteDB]

CREATE TABLE Rate (
	ValuteID varchar(255) NOT NULL PRIMARY KEY,
	RateVal float NOT NULL,
	RateDate DATE NOT NULL
);
GO

DROP TABLE Rate

SELECT * from Rate

SELECT SUSER_SNAME(), HOST_NAME()

INSERT INTO Rate (ValuteID,RateVal, RateDate) 
VALUES ('USD', 64.98, '21-12-1998'),
		('RUB', 1.0, '12-03-2019');
go