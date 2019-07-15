USE [ValuteDB]

CREATE TABLE Rate (
	ValuteID varchar(255) NOT NULL PRIMARY KEY,
	RateVal float NOT NULL,
	RateDate DATE NOT NULL
);
GO

DROP TABLE Rate

SELECT * from Rate


INSERT INTO Rate (ValuteID,RateVal, RateDate) 
VALUES ('USD', 64.98, '21-12-1998');
go