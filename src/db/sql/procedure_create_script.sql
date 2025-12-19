create or replace procedure delete_rental_proc(
p_id_rental in int
)
as
v_id_rv int;
begin
select id_rv into v_id_rv from rental where id = p_id_rental;

delete from accessory_rental where id_rental = p_id_rental;
delete from rental where id = p_id_rental;

update rv set status = 'available' where id = v_id_rv;

commit;
exception
when others then

rollback;
raise;
end;
/

create or replace procedure create_rental_simple(
p_date_from in date,
p_date_to in date,
p_creation_date in date,
p_price in decimal,
p_id_customer in int,
p_id_rv in int
)
as
begin
insert into rental (date_from, date_to, creation_date, price, status, is_paid, id_customer, id_rv)
values (p_date_from, p_date_to, p_creation_date, p_price, 'reserved', 0, p_id_customer, p_id_rv);

update rv set status = 'rented' where id = p_id_rv;
commit;
exception
when others then
rollback;
raise;
end;
/


create or replace procedure create_rental_with_acc(
p_date_from in date,
p_date_to in date,
p_creation_date in date,
p_price in decimal,
p_id_customer in int,
p_id_rv in int,
p_rental_id out int
)
as
begin
insert into rental (date_from, date_to, creation_date, price, status, is_paid, id_customer, id_rv)
values (p_date_from, p_date_to, p_creation_date, p_price, 'reserved', 0, p_id_customer, p_id_rv)
returning id into p_rental_id;

update rv set status = 'rented' where id = p_id_rv;
commit;
exception
when others then
rollback;
raise;
end;
/
