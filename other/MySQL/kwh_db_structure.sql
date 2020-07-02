# If database doesn't already exist create it
CREATE DATABASE IF NOT EXISTS kwh;

# Create MySQL user "pi"
CREATE USER IF NOT EXISTS 'pi'@'localhost' IDENTIFIED BY '';
# Grant all privileges on kwh database to pi user
GRANT ALL PRIVILEGES ON `kwh`.* TO 'pi'@'localhost' IDENTIFIED BY '';

# Switch to new kwh database
USE kwh

# If config table doesn't already exist create it and insert mandatory config values
CREATE TABLE IF NOT EXISTS `config`(`key` VARCHAR(30) NOT NULL, 
                `value` VARCHAR(30) NOT NULL, 
                `time_created` DATETIME NOT NULL, 
                `time_changed` DATETIME DEFAULT NULL, 
                `active` TINYINT NOT NULL,
CONSTRAINT CONFIG_PK PRIMARY KEY (`active`, 
               `key`)
)ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4;
COMMIT;

# If data tables doesn't already exist create it
CREATE TABLE IF NOT EXISTS `data`(`timestamp` INT NOT NULL, 
                `key` VARCHAR(30) NOT NULL, 
                `value` DECIMAL(15,6) NOT NULL,
CONSTRAINT DATA_PK PRIMARY KEY(`timestamp`, 
               `key`)
)ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4;
COMMIT;

# If tstring tables doesn't already exist create it
CREATE TABLE IF NOT EXISTS `tx_string`(`timestamp` INT NOT NULL, 
                `tx_string` LONGBLOB NOT NULL, 
CONSTRAINT CONFIG_PK PRIMARY KEY (`timestamp`)
)ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4 ;
COMMIT;
