use test
set names utf8;

-- 1. Выбрать все товары (все поля)
select * 
from product;

-- 2. Выбрать названия всех автоматизированных складов
select * 
from store 
where is_automated=1;

-- 3. Посчитать общую сумму в деньгах всех продаж
select sum(total)
from sale;

-- 4. Получить уникальные store_id всех складов, с которых была хоть одна продажа
select distinct store_id 
from sale;

-- 5. Получить уникальные store_id всех складов, с которых не было ни одной продажи
select store.store_id
from store natural 
left join sale 
where total is null;

-- 6. Получить для каждого товара название и среднюю стоимость единицы товара avg(total/quantity), если товар не продавался, он не попадает в отчет.
select product.name, avg(sale.total/sale.quantity) 
from product 
natural join sale 
group by product_id;

-- 7. Получить названия всех продуктов, которые продавались только с единственного склада
select product.name 
from product 
natural join sale 
group by product_id
having count(distinct `store_id`) = 1;

-- 8. Получить названия всех складов, с которых продавался только один продукт
select st.name
from store as st
natural join sale as sl
group by store_id
having count(distinct `product_id`) = 1;

-- 9. Выберите все ряды (все поля) из продаж, в которых сумма продажи (total) максимальна (равна максимальной из всех встречающихся)
select * 
from sale
where total = (
    select max(total) from sale);

-- 10. Выведите дату самых максимальных продаж, если таких дат несколько, то самую раннюю из них
select date
from sale
where total = (
    select max(total) from sale)
order by date ASC 
limit 1;
