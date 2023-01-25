select * from user;

INSERT INTO user (password, name, address, phone, email, birthdate, role) VALUES (%s, %s, %s, %s, %s, %s, %s);

SELECT * FROM user WHERE name = %s and password = %s;

UPDATE user SET password = "' + password + '", name = "' + name + '", address = "' + address + '", phone = "' + phone + '", email = "' + email + '", birthdate = "' + birthdate + '" WHERE id = "' + str(session['userid']) + '";

SELECT user.name, comment.text, comment.date, comment.rate FROM comment, user where comment.Customer_user_id = user.id and comment.Product_name = %s order by comment.rate limit 3;

SELECT * FROM supplier where address like %s;

SELECT sum(quantity), product_name FROM cart, orderitem WHERE cart.id = orderitem.cart_id and is_paid = 1 and date between date_sub(now(), INTERVAL 1 MONTH) and now() group by product_name order by sum(quantity) desc;

SELECT sum(quantity), product_name FROM cart, orderitem WHERE cart.id = orderitem.cart_id and is_paid = 1 and date between date_sub(now(), INTERVAL 1 WEEK) and now() group by product_name order by sum(quantity) desc;

select * from cart,orderitem Where cart.id=orderitem.cart_id and cart.customer_user_id = %s;

select supplier.name, supplier.phone, supplier.address from supplier,supplierproduct where supplier.id = supplierproduct.Supplier_id and supplierproduct.Product_name = %s;

select * from cart,orderitem Where cart.id=orderitem.cart_id and cart.customer_user_id = %s order by date DESC limit 10;

SELECT * FROM comment where product_name = %s;

SELECT Product_name, sum(total), sum(quantity) from orderitem,cart where Product_name = %s and is_paid = 1 and Cart_id = cart.id and date between date_sub(now(), INTERVAL 1 month) and now();

select name, price, discount, category, brand from product;

SELECT distinct user.id, user.name, user.address, user.phone, count(user.id) as number_of_purchases FROM cart, user WHERE cart.Customer_user_id = user.id and date < "' + str(datetime.date.today()) + '" and date > "' + last_month() + '" GROUP BY user.id ORDER BY number_of_purchases DESC LIMIT 10;

SELECT distinct user.id, user.name, user.address, user.phone, count(user.id) as number_of_purchases FROM cart, user WHERE cart.Customer_user_id = user.id and date < "' + str(datetime.date.today()) + '" and date > "' + last_week() + '" GROUP BY user.id ORDER BY number_of_purchases DESC LIMIT 10;

SELECT product.name, product.price, product.brand, supplier.id, supplier.name, supplier.phone, Min(product.price) FROM supplier, supplierproduct, product WHERE Supplier_id = supplier.id AND Product_name = product.name AND product.name LIKE "' + pname + '%";

SELECT name, Product_name, text, date, rate FROM comment, user WHERE Product_name = "' + pname + '" AND user.id = Customer_user_id ORDER BY rate DESC LIMIT 3;

SELECT id, name, address, phone, email, birthdate FROM user WHERE address LIKE "%' + city + '%" ;

DELETE FROM user WHERE id = "' + id + '" AND password = "' + password + '" AND name = "' + name + '" AND address = "' + address + '" AND phone = "' + phone + '" AND email = "' + email + '" AND birthdate = "' + birthdate + '" AND role = "user";

UPDATE user SET , password = "' + password + '", name = "' + name + '", address = "' + address + '", phone = "' + phone + '", email = "' + email + '", birthdate = "' + birthdate + '" WHERE id = "' + id + '" And role = "user";

INSERT INTO user ( password, name, address, phone, email, birthdate, role ) VALUES ( "' + password + '", "' + name + '", "' + address + '", "' + phone + '", "' + email + '", "' + birthdate + '", "' + role + '" );

UPDATE product SET name = "' + name + '", barcode = "' + barcode + '", price = "' + price + '", discount = "' + discount + '", category = "' + category + '", brand = "' + brand + '" WHERE id = "' + id + '";

INSERT INTO product (name, barcode, price, discount, category, brand) values ("' + name + '", "' + barcode + '", "' + price + '", "' + discount + '", "' + category + '", "' + brand + '");

DELETE FROM Product 'WHERE name = "' + name + '" AND barcode = "' + barcode + '" AND price = "' + price + '" AND discount = "' + discount + '" AND category = "' + category + '" AND brand = "' + brand + '" WHERE id = "' + id + '"';

select distinct category from product;

select * from product where discount > 15;

select avg(total_price) from cart where is_paid = 1 and date between date_sub(now(), INTERVAL 1 MONTH) and now();