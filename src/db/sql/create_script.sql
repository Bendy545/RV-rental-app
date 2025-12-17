create table brand(
id int generated always as identity primary key,
name varchar(20) not null
);

create table rv_type(
id int generated always as identity primary key,
name varchar(40) not null,
description varchar(40) not null
);

create table rv(
id int generated always as identity primary key,
spz varchar(20) not null unique,
manufacture_date date not null,
price_for_day decimal(10, 2) not null,
status varchar(20) not null check(status in ('available', 'rented', 'service')),
id_brand int not null check(id_brand > 0),
id_type int not null check(id_type > 0),

foreign key(id_brand) references brand(id),
foreign key(id_type) references rv_type(id)
);

create table customer(
id int generated always as identity primary key,
name varchar(30) not null,
surname varchar(30) not null,
email varchar(50) not null,
tel varchar(12) not null
);

create table accessory(
id int generated always as identity primary key,
name varchar(40) not null,
description varchar(50) not null,
price_for_day decimal(10, 2) not null
);

create table rental(
id int generated always as identity primary key,
date_from date not null,
date_to date not null,
creation_date date not null,
price decimal(10, 2) not null,
status varchar(20) not null check(status in ('reserved', 'active', 'finished', 'canceled')),
is_paid number(1,0) not null check(is_paid in (1, 0)),
id_customer int not null check(id_customer > 0),
id_rv int not null check(id_rv > 0),

check(date_from < date_to),

foreign key(id_customer) references customer(id),
foreign key(id_rv) references rv(id)
);

create table accessory_rental(
id int generated always as identity primary key,
id_accessory int not null check(id_accessory > 0),
id_rental int not null check(id_rental > 0),
amount int not null check(amount > 0),
price_at_rent decimal(10, 2) not null,

foreign key(id_accessory) references accessory(id),
foreign key(id_rental) references rental(id)
);