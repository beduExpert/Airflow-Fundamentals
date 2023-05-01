select
    f.title    
from film f
inner join film_category fc
on (f.film_id = fc.film_id)
inner join category c
on (fc.category_id = c.category_id)
where
    c.name = 'Drama'
order by random()
limit 1;

select distinct name from category;