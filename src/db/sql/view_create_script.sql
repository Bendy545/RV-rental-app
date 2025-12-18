create view v_rv_overview
as
select rv.id as rv_id, rv.spz, rv.manufacture_date, rv.price_for_day, rv.status, brand.name as brand_name, rv_type.name as type_name, rv_type.description as type_description
from rv
join brand on rv.id_brand = brand.id
join rv_type on rv.id_type = rv_type.id;


create view v_rental_overview
as
select rental.id as rental_id, rental.date_from, rental.date_to, rental.creation_date, rental.price, rental.status, rental.is_paid, customer.name as customer_name, customer.surname as customer_surname, customer.email, rv.spz as rv_spz
from rental
join customer on rental.id_customer = customer.id
join rv on rental.id_rv = rv.id;