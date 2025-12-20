create view v_rv_overview
as
select rv.id as rv_id, rv.spz, rv.manufacture_date, rv.price_for_day, brand.name as brand_name, rv_type.name as type_name, rv_type.description as type_description
from rv
join brand on rv.id_brand = brand.id
join rv_type on rv.id_type = rv_type.id;


create view v_rental_overview
as
select rental.id as rental_id, rental.date_from, rental.date_to, rental.creation_date, rental.price, rental.status, rental.is_paid, customer.name as customer_name, customer.surname as customer_surname, customer.email, rv.spz as rv_spz
from rental
join customer on rental.id_customer = customer.id
join rv on rental.id_rv = rv.id;

create view v_revenue_by_brand
as
select b.name as brand_name, COUNT(r.id) as total_rentals, SUM(r.price) as total_revenue, AVG(r.price) as avg_rental_price, MIN(r.price) as min_rental_price, MAX(r.price) as max_rental_price
from rental r
join rv on r.id_rv = rv.id
join brand b on rv.id_brand = b.id
where r.status != 'canceled'
group by b.name;

create view v_customer_statistics
as
select c.id as customer_id, c.name || ' ' || c.surname as customer_name, c.email, COUNT(r.id) as total_rentals, SUM(r.price) as total_spent, AVG(r.date_to - r.date_from) as avg_rental_days
from customer c
join rental r on c.id = r.id_customer
group by c.id, c.name, c.surname, c.email;

create view v_popular_accessories
as
select a.name as accessory_name, COUNT(ar.id) as times_rented, SUM(ar.amount) as total_quantity, SUM(ar.price_at_rent) as total_revenue
from accessory a
join accessory_rental ar on a.id = ar.id_accessory
join rental r on ar.id_rental = r.id
where r.status != 'canceled'
group by a.name;