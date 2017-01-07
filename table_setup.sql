create table words (
	word varbinary(25) not null primary key,
	meaning char(40),
	etyma char(20),
        association char(30),
	yes tinyint unsigned default 0,
	no tinyint unsigned default 0,
	ts timestamp default CURRENT_TIMESTAMP
) character set utf8 collate utf8_general_ci;

create table etymas (
	represent char(10) not null primary key,
	meaning char(30),
	synonymous char(50)
) character set utf8 collate utf8_general_ci;

create table associations (
	association char(20) not null primary key
) character set utf8 collate utf8_general_ci;
