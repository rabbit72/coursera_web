use test
set names utf8;

-- 1. Выбрать все товары (все поля)
select * from product;

-- 2. Выбрать названия всех автоматизированных складов
select name from store;

-- 3. Посчитать общую сумму в деньгах всех продаж
select SUM(total) from sale;

-- 4. Получить уникальные store_id всех складов, с которых была хоть одна продажа
select store_id from sale group by store_id;


-- 5. Получить уникальные store_id всех складов, с которых не было ни одной продажи
select store.store_id from store left join sale using (store_id) where sale.store_id is NULL group by store.store_id;

-- 6. Получить для каждого товара название и среднюю стоимость единицы товара avg(total/quantity), если товар не продавался, он не попадает в отчет.
select name, avg(total/quantity) from product join sale using (product_id) group by name order by avg(total/quantity) DESC;

-- 7. Получить названия всех продуктов, которые продавались только с единственного склада
select ANY_VALUE(name) as name from product natural join sale group by product_id having count(DISTINCT store_id) = 1;

-- 8. Получить названия всех складов, с которых продавался только один продукт
select ANY_VALUE(name) as name from store natural join sale group by product_id having count(DISTINCT store_id) = 1;

-- 9. Выберите все ряды (все поля) из продаж, в которых сумма продажи (total) максимальна (равна максимальной из всех встречающихся)
SELECT * from sale WHERE total = (SELECT max(total) as m from sale group by sale_id ORDER BY m DESC LIMIT 1);

-- 10. Выведите дату самых максимальных продаж, если таких дат несколько, то самую раннюю из них
select sale.date, SUM(total) FROM sale GROUP BY sale.date order by SUM(total) DESC, sale.date LIMIT 1;
