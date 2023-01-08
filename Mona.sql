-- ----------------Queries-------------------
select distinct category from product;
select * from product where discount > 14;
select * from comment;   -- esme moshtari ham gofte beshe
select avg(total_price)from cart where is_paid=1;

-- ---------------Update Tables----------------------
ALTER TABLE `mydb`.`comment` 
ADD COLUMN `rate` INT UNSIGNED NOT NULL AFTER `date`;
INSERT INTO `mydb`.`comment` (`Customer_user_id`, `Product_name`, `text`, `date`) VALUES ('25', 'ice-cream', 'Delicious', '2022-11-09 14:55:34');
UPDATE `mydb`.`comment` SET `rate` = '9' WHERE (`Customer_user_id` = '21') and (`Product_name` = 'milk');
UPDATE `mydb`.`comment` SET `rate` = '2' WHERE (`Customer_user_id` = '22') and (`Product_name` = 'flour');
UPDATE `mydb`.`comment` SET `rate` = '4' WHERE (`Customer_user_id` = '22') and (`Product_name` = 'rice');
UPDATE `mydb`.`comment` SET `rate` = '7' WHERE (`Customer_user_id` = '23') and (`Product_name` = 'milk');
INSERT INTO `mydb`.`comment` (`Customer_user_id`, `Product_name`, `text`, `date`, `rate`) VALUES ('25', 'ice-cream', 'SOOOO delicious!!!', '2022-10-18 14:35:34', '10');


-- ---------------enter users ----------------------
http://127.0.0.1:5000/login?username=u3&password=12345