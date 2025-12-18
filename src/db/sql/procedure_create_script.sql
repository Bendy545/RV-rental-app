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
