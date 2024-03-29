-- Ali Khadangi - 9912762472
-- MohammadReza Esmailian - 9912762574 
-- Mona Saghafi - 9912762290 
-- Atiye Bonakdar - 9922762413


-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`Store`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Store` (
  `branch_no` INT NOT NULL,
  `address` VARCHAR(100) NULL,
  `manager_id` INT NULL,
  PRIMARY KEY (`branch_no`));


-- -----------------------------------------------------
-- Table `mydb`.`Employee`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Employee` (
  `user_id` INT NOT NULL,
  `degree` VARCHAR(45) NULL,
  `role` VARCHAR(45) NULL,
  `salary` INT NULL,
  PRIMARY KEY (`user_id`));


-- -----------------------------------------------------
-- Table `mydb`.`User`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`User` (
  `id` INT NOT NULL auto_increment,
  `password` VARCHAR(15) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `address` VARCHAR(100) NULL,
  `phone` INT NULL,
  `email` VARCHAR(45) NULL,
  `birthdate` DATE NULL,
  `role` VARCHAR(10) NULL,
  PRIMARY KEY (`id`));


-- -----------------------------------------------------
-- Table `mydb`.`Customer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Customer` (
  `user_id` INT NOT NULL,
  `score` INT NULL,
  PRIMARY KEY (`user_id`));


-- -----------------------------------------------------
-- Table `mydb`.`Cart`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Cart` (
  `id` INT NOT NULL auto_increment,
  `date` DATETIME NULL,
  `total_price` INT NULL,
  `is_paid` TINYINT NOT NULL,
  `discount` INT NULL,
  `Customer_user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_Cart_Customer1_idx` (`Customer_user_id` ASC) VISIBLE,
  CONSTRAINT `fk_Cart_Customer1`
    FOREIGN KEY (`Customer_user_id`)
    REFERENCES `mydb`.`Customer` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `mydb`.`DeliveryEmployee`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`DeliveryEmployee` (
  `id` INT NOT NULL,
  PRIMARY KEY (`id`));


-- -----------------------------------------------------
-- Table `mydb`.`Delivery`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Delivery` (
  `date` DATETIME NOT NULL,
  `address` VARCHAR(100) NOT NULL,
  `phone` INT NULL,
  `price` INT NOT NULL,
  `Cart_id` INT NOT NULL,
  `DeliveryEmployee_id` INT NOT NULL,
  PRIMARY KEY (`date`, `Cart_id`, `DeliveryEmployee_id`),
  INDEX `fk_Delivery_Cart1_idx` (`Cart_id` ASC) VISIBLE,
  INDEX `fk_Delivery_DeliveryEmployee1_idx` (`DeliveryEmployee_id` ASC) VISIBLE,
  CONSTRAINT `fk_Delivery_Cart1`
    FOREIGN KEY (`Cart_id`)
    REFERENCES `mydb`.`Cart` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Delivery_DeliveryEmployee1`
    FOREIGN KEY (`DeliveryEmployee_id`)
    REFERENCES `mydb`.`DeliveryEmployee` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `mydb`.`Product`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Product` (
  `name` VARCHAR(45) NOT NULL,
  `barcode` INT NULL,
  `price` INT NOT NULL,
  `discount` INT NULL,
  `category` VARCHAR(45) NOT NULL,
  `brand` VARCHAR(45) NULL,
  PRIMARY KEY (`name`));


-- -----------------------------------------------------
-- Table `mydb`.`Supplier`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Supplier` (
  `id` INT NOT NULL auto_increment,
  `name` VARCHAR(45) NOT NULL,
  `address` VARCHAR(100) NULL,
  `manager_name` VARCHAR(45) NULL,
  `phone` INT NULL,
  PRIMARY KEY (`id`));


-- -----------------------------------------------------
-- Table `mydb`.`OrderItem`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`OrderItem` (
  `total` INT NULL,
  `quantity` INT NOT NULL,
  `Cart_id` INT NOT NULL,
  `Product_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`Cart_id`, `Product_name`),
  INDEX `fk_OrderItem_Cart1_idx` (`Cart_id` ASC) VISIBLE,
  INDEX `fk_OrderItem_Product1_idx` (`Product_name` ASC) VISIBLE,
  CONSTRAINT `fk_OrderItem_Cart1`
    FOREIGN KEY (`Cart_id`)
    REFERENCES `mydb`.`Cart` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_OrderItem_Product1`
    FOREIGN KEY (`Product_name`)
    REFERENCES `mydb`.`Product` (`name`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `mydb`.`Warehouse`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Warehouse` (
  `id` INT NOT NULL auto_increment,
  `address` VARCHAR(100) NOT NULL,
  `manager_id` INT NOT NULL,
  PRIMARY KEY (`id`));


-- -----------------------------------------------------
-- Table `mydb`.`StoreWarehouse`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`StoreWarehouse` (
  `Store_branch_no` INT NOT NULL,
  `Warehouse_id` INT NOT NULL,
  PRIMARY KEY (`Store_branch_no`, `Warehouse_id`),
  INDEX `fk_Store_has_Warehouse_Warehouse1_idx` (`Warehouse_id` ASC) VISIBLE,
  INDEX `fk_Store_has_Warehouse_Store_idx` (`Store_branch_no` ASC) VISIBLE,
  CONSTRAINT `fk_Store_has_Warehouse_Store`
    FOREIGN KEY (`Store_branch_no`)
    REFERENCES `mydb`.`Store` (`branch_no`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Store_has_Warehouse_Warehouse1`
    FOREIGN KEY (`Warehouse_id`)
    REFERENCES `mydb`.`Warehouse` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `mydb`.`WarehouseProduct`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`WarehouseProduct` (
  `Warehouse_id` INT NOT NULL,
  `Product_name` VARCHAR(45) NOT NULL,
  `quantity` INT NULL,
  PRIMARY KEY (`Warehouse_id`, `Product_name`),
  INDEX `fk_Warehouse_has_Product_Product1_idx` (`Product_name` ASC) VISIBLE,
  INDEX `fk_Warehouse_has_Product_Warehouse1_idx` (`Warehouse_id` ASC) VISIBLE,
  CONSTRAINT `fk_Warehouse_has_Product_Warehouse1`
    FOREIGN KEY (`Warehouse_id`)
    REFERENCES `mydb`.`Warehouse` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Warehouse_has_Product_Product1`
    FOREIGN KEY (`Product_name`)
    REFERENCES `mydb`.`Product` (`name`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `mydb`.`SupplierProduct`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`SupplierProduct` (
  `Supplier_id` INT NOT NULL,
  `Product_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`Supplier_id`, `Product_name`),
  INDEX `fk_Supplier_has_Product_Product1_idx` (`Product_name` ASC) VISIBLE,
  INDEX `fk_Supplier_has_Product_Supplier1_idx` (`Supplier_id` ASC) VISIBLE,
  CONSTRAINT `fk_Supplier_has_Product_Supplier1`
    FOREIGN KEY (`Supplier_id`)
    REFERENCES `mydb`.`Supplier` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Supplier_has_Product_Product1`
    FOREIGN KEY (`Product_name`)
    REFERENCES `mydb`.`Product` (`name`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `mydb`.`HistoryPrice`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`HistoryPrice` (
  `date` DATETIME NOT NULL,
  `price` INT NOT NULL,
  `Product_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`date`, `price`, `Product_name`),
  INDEX `fk_HistoryPrice_Product1_idx` (`Product_name` ASC) VISIBLE,
  CONSTRAINT `fk_HistoryPrice_Product1`
    FOREIGN KEY (`Product_name`)
    REFERENCES `mydb`.`Product` (`name`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `mydb`.`SupplierStore`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`SupplierStore` (
  `Store_branch_no` INT NOT NULL,
  `Supplier_id` INT NOT NULL,
  `start_date` DATETIME NULL,
  `broker_name` VARCHAR(45) NULL,
  `end_date` DATETIME NULL,
  PRIMARY KEY (`Store_branch_no`, `Supplier_id`),
  INDEX `fk_Store_has_Supplier_Supplier1_idx` (`Supplier_id` ASC) VISIBLE,
  INDEX `fk_Store_has_Supplier_Store1_idx` (`Store_branch_no` ASC) VISIBLE,
  CONSTRAINT `fk_Store_has_Supplier_Store1`
    FOREIGN KEY (`Store_branch_no`)
    REFERENCES `mydb`.`Store` (`branch_no`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Store_has_Supplier_Supplier1`
    FOREIGN KEY (`Supplier_id`)
    REFERENCES `mydb`.`Supplier` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `mydb`.`StoreEmployee`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`StoreEmployee` (
  `user_id` INT NOT NULL,
  `Store_branch_no` INT NOT NULL,
  PRIMARY KEY (`user_id`, `Store_branch_no`),
  INDEX `fk_StoreEmployee_Store1_idx` (`Store_branch_no` ASC) VISIBLE,
  CONSTRAINT `fk_StoreEmployee_Store1`
    FOREIGN KEY (`Store_branch_no`)
    REFERENCES `mydb`.`Store` (`branch_no`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `mydb`.`WarehouseEmployee`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`WarehouseEmployee` (
  `id` INT NOT NULL,
  `Warehouse_id` INT NOT NULL,
  PRIMARY KEY (`id`, `Warehouse_id`),
  INDEX `fk_WarehouseEmployee_Warehouse1_idx` (`Warehouse_id` ASC) VISIBLE,
  CONSTRAINT `fk_WarehouseEmployee_Warehouse1`
    FOREIGN KEY (`Warehouse_id`)
    REFERENCES `mydb`.`Warehouse` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `mydb`.`Comment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Comment` (
  `Customer_user_id` INT NOT NULL,
  `Product_name` VARCHAR(45) NOT NULL,
  `text` VARCHAR(200) NULL,
  `date` DATETIME NULL,
  `rate` INT NULL,
  PRIMARY KEY (`Customer_user_id`, `Product_name`),
  INDEX `fk_Comment_Product1_idx` (`Product_name` ASC) VISIBLE,
  INDEX `fk_Comment_Customer1_idx` (`Customer_user_id` ASC) VISIBLE,
  CONSTRAINT `fk_Comment_Customer1`
    FOREIGN KEY (`Customer_user_id`)
    REFERENCES `mydb`.`Customer` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Comment_Product1`
    FOREIGN KEY (`Product_name`)
    REFERENCES `mydb`.`Product` (`name`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `mydb`.`Favorite`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Favorite` (
  `Customer_user_id` INT NOT NULL,
  `Product_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`Customer_user_id`, `Product_name`),
  INDEX `fk_Favorite_Product1_idx` (`Product_name` ASC) VISIBLE,
  INDEX `fk_Favorite_Customer1_idx` (`Customer_user_id` ASC) VISIBLE,
  CONSTRAINT `fk_Favorite_Customer1`
    FOREIGN KEY (`Customer_user_id`)
    REFERENCES `mydb`.`Customer` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Favorite_Product1`
    FOREIGN KEY (`Product_name`)
    REFERENCES `mydb`.`Product` (`name`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

-- User---------------------------------------------------------------------------------------------*
-- (I id, S password, S name, S address, I phone, S email, D birthdate)-----------------------------

insert into user (password, name, address, phone, email, birthdate, role) values 
('12345', 'u1',  'addr1',  989195761, 'u1@gmail.com',  '2002-01-01', 'superuser'),
('12345', 'u2',  'addr2',  989154762, 'u2@gmail.com',  '1998-01-23', 'superuser'),
('12345', 'u3',  'addr3',  989195771, 'u3@gmail.com',  '2002-02-03', 'user'),
('12345', 'u4',  'addr4',  989495961, 'u4@gmail.com',  '1998-12-24', 'user'),
('12345', 'u5',  'addr5',  989195545, 'u5@gmail.com',  '1995-01-05', 'user'),
('12345', 'u6',  'addr6',  954495747, 'u6@gmail.com',  '1995-11-15', 'user'),
('12345', 'u7',  'addr7',  989454454, 'u7@gmail.com',  '2002-01-19', 'user'),
('12345', 'u8',  'addr8',  989495899, 'u8@gmail.com',  '2002-08-02', 'user'),
('12345', 'u9',  'addr9',  989195000, 'u9@gmail.com',  '2002-04-09', 'user'),
('12345', 'u10', 'addr10', 989155544, 'u10@gmail.com', '2000-01-23', 'user'),
('12345', 'u11', 'addr11', 984495723, 'u11@gmail.com', '1998-04-12', 'user'),
('12345', 'u12', 'addr12', 989455455, 'u12@gmail.com', '2000-11-21', 'user'),
('12345', 'u13', 'addr13', 989413154, 'u13@gmail.com', '1998-01-12', 'user'),
('12345', 'u14', 'addr14', 989754131, 'u14@gmail.com', '2000-12-30', 'user'),
('12345', 'u15', 'addr15', 989318648, 'u15@gmail.com', '1995-01-12', 'user'),
('12345', 'u16', 'addr16', 989988455, 'u16@gmail.com', '2000-05-18', 'user'),
('12345', 'u17', 'addr17', 989021111, 'u17@gmail.com', '2002-03-16', 'user'),
('12345', 'u18', 'addr18', 989248632, 'u18@gmail.com', '1995-01-17', 'user'),
('12345', 'u19', 'addr19', 989871566, 'u19@gmail.com', '2002-06-04', 'user'),
('12345', 'u20', 'addr20', 989465321, 'u20@gmail.com', '1999-07-06', 'user'),
('12345', 'u21', 'addr21', 989849943, 'u21@gmail.com', '1999-06-04', 'user'),
('12345', 'u22', 'addr22', 989333789, 'u22@gmail.com', '1999-12-08', 'user'),
('12345', 'u23', 'addr23', 989000013, 'u23@gmail.com', '1999-03-10', 'user'),
('12345', 'u24', 'addr24', 989453666, 'u24@gmail.com', '1998-02-16', 'user'),
('12345', 'u25', 'addr25', 989441654, 'u25@gmail.com', '1999-03-29', 'user');
---------------------------------------------------------------------------------------------------

-- Store--------------------------------------------------------------------------------------------*
-- (I branch_no, S address, I manager_id)-----------------------------------------------------------

insert into store values
(1001, 'Storeaddr1', 1),
(1002, 'Storeaddr2', 2),
(1003, 'Storeaddr3', 3);
---------------------------------------------------------------------------------------------------

-- Warehouse----------------------------------------------------------------------------------------*
-- (I id, S address, I manager_id)------------------------------------------------------------------

insert into warehouse (address, manager_id) values
('Warehouseaddr1', 4),
('Warehouseaddr2', 5);
---------------------------------------------------------------------------------------------------

-- Suplier------------------------------------------------------------------------------------------*
-- (I id, S name, S address, S manager_name, I phone)-----------------------------------------------

insert into supplier(name, address, manager_name, phone) values
('tak', 'Suplier1', 'Ali Ghasemi', 51384912),
('tabiat', 'Suplier2', 'Reza Irani', 21478484),
('mihan', 'Suplier3', 'Mohammad Karimi', 51456875);
---------------------------------------------------------------------------------------------------

-- Customer-----------------------------------------------------------------------------------------*
-- (I user_id, I score)-----------------------------------------------------------------------------

insert into customer values
(21, 20),
(22, 50),
(23, 10),
(24, 25),
(25, 35);
---------------------------------------------------------------------------------------------------

-- Employee-----------------------------------------------------------------------------------------*
-- (I user_id, S degree, S role, I salary)----------------------------------------------------------

insert into employee values
(1, 'masters', 'store manager', 10000),
(2, 'PH.D.', 'store manager', 11000),
(3, 'masters', 'store manager', 10000),
(4, 'bachelor', 'warehouse manager', 9000),
(5, 'bachelor', 'warehouse manager', 9000),
(6, 'masters', 'cashier', 6000),
(7, 'bachelor', 'cashier', 5500),
(8, 'masters', 'cashier', 6000),
(9, 'bachelor', 'cashier', 5500),
(10, 'bachelor', 'cashier', 5500),
(11, 'masters', 'cashier', 6000),
(12, 'masters', 'janitor', 3500),
(13, 'bachelor', 'janitor', 3000),
(14, 'masters', 'janitor', 3500),
(15, 'bachelor', 'guard', 7000),
(16, 'masters', 'guard', 7500),
(17, 'bachelor', 'guard', 7000),
(18, 'bachelor', 'guard', 7000),
(19, 'masters', 'driver', 4000),
(20, 'bachelor', 'driver', 4000);
---------------------------------------------------------------------------------------------------

-- Product------------------------------------------------------------------------------------------*
-- (S name, I barcode, I price, I discount, S category, S brand)------------------------------------

insert into product values 
('milk', 62612345, 4, 0, 'dairy', 'mihan'),
('ice-cream', 62612354, 3, 10, 'dairy', 'mihan'),
('cheese', 62612346, 6, 33, 'dairy', 'mihan'),
('rice', 62616789, 10, 0, 'cereal', 'tabiat'),
('flour', 62616000, 9, 25, 'cereal', 'tak'),
('pasta', 62612398, 8, 0, 'cereal', 'tak');
---------------------------------------------------------------------------------------------------

-- Storeemployee------------------------------------------------------------------------------------*
-- (I user_id, I store_branch_no)-------------------------------------------------------------------

insert into storeemployee values
(1,  1001),
(2,  1002),
(3,  1003),
(6,  1001),
(7,  1001),
(8,  1002),
(9,  1002),
(10, 1003),
(11, 1003),
(12, 1001),
(13, 1002),
(14, 1003);
---------------------------------------------------------------------------------------------------

-- Deliveryemployee---------------------------------------------------------------------------------*
-- (I id)-------------------------------------------------------------------------------------------

insert into deliveryemployee values
(19),
(20);
---------------------------------------------------------------------------------------------------

-- Warehouseemployee--------------------------------------------------------------------------------*
-- (I user_id, I warehouse)-------------------------------------------------------------------------

insert into warehouseemployee values
(4,  1),
(5,  2),
(15, 1),
(16, 1),
(17, 2),
(18, 2);
---------------------------------------------------------------------------------------------------


-- Cart---------------------------------------------------------------------------------------------*
-- (I id, DT date, I total_price, I is_paid, I discount, I customer_user_id)------------------------

insert into cart (date, total_price, is_paid, discount, customer_user_id) values
('2022-05-01 18:25:30', 70, 0, 10, 21),
('2022-06-01 19:25:30', 31, 1, 15, 22),
('2022-07-01 17:12:30', 42, 0, 30, 22),
('2022-03-02 20:43:30', 30, 1, 5, 22),
('2022-07-07 06:33:30', 45, 1, 15, 23),
('2022-10-01 14:17:30', 87, 0, 15, 23),
('2022-12-15 12:20:30', 95, 1, 25, 24),
('2023-01-05 01:02:30', 44, 1, 30, 24),
('2022-11-12 13:37:30', 120, 1, 35, 25);
---------------------------------------------------------------------------------------------------


-- Comment-----------------------------------------------------------------------------------------*
-- (I customer_user_id, S product_name, S text, DT time)--------------------------------------------

insert into comment values
(21, 'milk',  'Pretty good!', '2022-07-03 18:35:30', 9),
(22, 'flour', 'Why?!?', '2022-03-01 11:25:30', 2),
(22, 'rice',  'Use other brands too...', '2022-09-12 19:25:30', 4),
(23, 'milk',  'Liked it', '2022-07-25 13:39:30', 7),
(24, 'flour', 'Weak QUALITTTTTTY.', '2022-08-08 12:25:30', 3),
(24, 'ice-cream', 'Delicious', '2022-11-09 14:55:34', 8),
(25, 'ice-cream', 'SOOOO delicious!!!', '2022-10-18 14:35:34', 10);
---------------------------------------------------------------------------------------------------


-- Delivery-----------------------------------------------------------------------------------------*
-- (DT date, S address, I phone, I price, I cart_id, I DeliveryE_id)------------------------------------------------

insert into delivery values
('2022-04-12', 'daddr1', 913849712, 5, 3, 19),
('2022-04-12', 'daddr2', 915559712, 3, 5, 19),
('2022-04-12', 'daddr2', 935844735, 3, 6, 20),
('2022-04-12', 'daddr3', 918447749, 2, 7, 20),
('2022-04-12', 'daddr1', 937125742, 5, 2, 20);
---------------------------------------------------------------------------------------------------


-- Favorite-----------------------------------------------------------------------------------------*
-- (I customer_id, S product_name)------------------------------------------------------------------

insert into favorite values
(21, 'milk'),
(22, 'milk'),
(22, 'rice'),
(23, 'rice'),
(23, 'ice-cream'),
(23, 'pasta'),
(24, 'milk'),
(24, 'ice-cream'),
(25, 'milk'),
(25, 'pasta'),
(25, 'flour');
---------------------------------------------------------------------------------------------------


-- Historyprice-------------------------------------------------------------------------------------*
-- (DT date, I price, S product_name)---------------------------------------------------------------

insert into historyprice values
('2019-05-01 18:25:30', 2, 'milk'),
('2021-05-01 18:25:30', 3, 'milk'),
('2022-05-01 18:25:30', 4, 'milk'),
('2018-05-01 18:25:30', 2, 'ice-cream'),
('2022-05-01 18:25:30', 3, 'ice-cream'),
('2018-02-01 18:25:30', 3, 'cheese'),
('2019-05-01 18:25:30', 4, 'cheese'),
('2020-05-01 18:25:30', 5, 'cheese'),
('2022-05-01 18:25:30', 6, 'cheese'),
('2017-05-01 18:25:30', 6, 'rice'),
('2020-05-01 18:25:30', 8, 'rice'),
('2022-05-01 18:25:30', 10, 'rice');
---------------------------------------------------------------------------------------------------


-- Orderitem----------------------------------------------------------------------------------------*
-- (I total, I quantity, I cart_id, S product_name)-------------------------------------------------

insert into orderitem values
(8, 2, 5, 'milk'),
(10, 1, 5, 'rice'),
(27, 3, 5, 'flour'),
(15, 5, 2, 'ice-cream'),
(16, 4, 2, 'milk'),
(10, 1, 3, 'rice'),
(8, 2, 3, 'milk'),
(24, 3, 3, 'pasta'),
(6, 2, 8, 'ice-cream'),
(10, 1, 8, 'rice'),
(4, 1, 8, 'milk'),
(24, 3, 8, 'pasta'),
(4, 1, 7, 'milk');
---------------------------------------------------------------------------------------------------


-- Storewarehouse-----------------------------------------------------------------------------------*
-- (I store_branch_no, I warehouse_id)--------------------------------------------------------------

insert into storewarehouse values
(1001, 1),
(1002, 1),
(1002, 2),
(1003, 2);
---------------------------------------------------------------------------------------------------


-- Suplierproduct-----------------------------------------------------------------------------------*
-- (I suplier_id, S product_name)-------------------------------------------------------------------
insert into supplierproduct values
(1, 'flour'),
(1, 'pasta'),
(2, 'rice'),
(3, 'milk'),
(3, 'ice-cream'),
(3, 'cheese');
---------------------------------------------------------------------------------------------------


-- Suplierstore-------------------------------------------------------------------------------------*
-- (I store_branch_no, I supplier_id, DT start_date, S broker_name, DT end_date)--------------------

insert into supplierstore values
(1001, 1, '2021-05-14 00:00:00', 'Baback Asadi', '2022-06-13 00:00:00'),
(1001, 3, '2022-03-01 00:00:00', 'Ali Javdinia', '2022-04-01 00:00:00'),
(1002, 1, '2022-09-23 00:00:00', 'Baback Asadi', '2023-03-16 00:00:00'),
(1002, 2, '2021-03-01 00:00:00', 'Hosain fakhr', '2022-09-23 00:00:00'),
(1002, 3, '2021-11-28 00:00:00', 'Ali Javdinia', '2024-01-10 00:00:00'),
(1003, 2, '2020-02-01 00:00:00', 'Hosain fakhr', '2022-11-01 00:00:00'),
(1003, 3, '2021-01-23 00:00:00', 'Ali Javdinia', '2023-12-15 00:00:00');
---------------------------------------------------------------------------------------------------


-- Warehouseproduct---------------------------------------------------------------------------------*
-- (I warehouse_id, S product_name, I quantity)-----------------------------------------------------

insert into warehouseproduct values
(1, 'milk', 150),
(1, 'ice-cream', 531),
(1, 'cheese', 1451),
(1, 'rice', 8066),
(1, 'pasta', 2314),
(2, 'milk', 129),
(2, 'ice-cream', 846),
(2, 'cheese', 2011),
(2, 'rice', 9483),
(2, 'flour', 7465),
(2, 'pasta', 1730);
-- -------------------------------------------------------------------------------------------------

-- Reports
select month(date), year(date), sum(quantity) 
from cart, orderitem 
where cart.id = orderitem.cart_id
group by year(date),month(date);

select name, discount from product where discount > 0;

select customer_user_id, sum(total_price) from cart where is_paid = 1 group by customer_user_id;
-- -------------------------------------------------------------------------------------------------

-- Queries
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