import mysql.connector as ddd
 
conn = ddd.connect(
    host="localhost",
    user="root",
    password="123456"
)

cursor = conn.cursor()

sf1 = """ DROP DATABASE IF EXISTS `bosh_mater` """
sf2 = """ CREATE DATABASE `bosh_mater`  """
sf3 = """ USE `bosh_mater`  """
sf4 = """ 
    CREATE TABLE `products` (
        `product_id` int(11) NOT NULL AUTO_INCREMENT,
        `date_a` varchar(50) NOT NULL,
        `name` varchar(50) NOT NULL,
        `enter_a` int(11) NOT NULL,
        `exit_a` int(11) NOT NULL,
        `nats_a` varchar(50) NOT NULL,

        PRIMARY KEY (`product_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci
"""



formulas = [sf1, sf2, sf3, sf4]

[cursor.execute(s) for s in formulas]

conn.commit()



