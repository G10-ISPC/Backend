CREATE DATABASE  IF NOT EXISTS `bd_ricco24` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `bd_ricco24`;
-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: localhost    Database: bd_ricco24
-- ------------------------------------------------------
-- Server version	8.0.33

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add Token',6,'add_token'),(22,'Can change Token',6,'change_token'),(23,'Can delete Token',6,'delete_token'),(24,'Can view Token',6,'view_token'),(25,'Can add Token',7,'add_tokenproxy'),(26,'Can change Token',7,'change_tokenproxy'),(27,'Can delete Token',7,'delete_tokenproxy'),(28,'Can view Token',7,'view_tokenproxy'),(29,'Can add Direccion',8,'add_direccion'),(30,'Can change Direccion',8,'change_direccion'),(31,'Can delete Direccion',8,'delete_direccion'),(32,'Can view Direccion',8,'view_direccion'),(33,'Can add Producto',9,'add_producto'),(34,'Can change Producto',9,'change_producto'),(35,'Can delete Producto',9,'delete_producto'),(36,'Can view Producto',9,'view_producto'),(37,'Can add Usuario',10,'add_customuser'),(38,'Can change Usuario',10,'change_customuser'),(39,'Can delete Usuario',10,'delete_customuser'),(40,'Can view Usuario',10,'view_customuser');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `authtoken_token`
--

DROP TABLE IF EXISTS `authtoken_token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `authtoken_token` (
  `key` varchar(40) NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`key`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `authtoken_token_user_id_35299eff_fk_usuario_id` FOREIGN KEY (`user_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authtoken_token`
--

LOCK TABLES `authtoken_token` WRITE;
/*!40000 ALTER TABLE `authtoken_token` DISABLE KEYS */;
INSERT INTO `authtoken_token` VALUES ('ad81b67d43ba1a9de7cfce0f27196db79ba7a052','2024-09-17 14:11:35.407933',2),('cd4c87d85ab31e805b4f334f9ec3b9380944a2ca','2024-09-17 13:56:32.533133',1),('f7e06e6049b51d4778919a994c847ab615cfd940','2024-09-17 14:18:27.812110',3);
/*!40000 ALTER TABLE `authtoken_token` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `direccion`
--

DROP TABLE IF EXISTS `direccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `direccion` (
  `id_direccion` int NOT NULL AUTO_INCREMENT,
  `calle` varchar(100) NOT NULL,
  `numero` int NOT NULL,
  PRIMARY KEY (`id_direccion`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `direccion`
--

LOCK TABLES `direccion` WRITE;
/*!40000 ALTER TABLE `direccion` DISABLE KEYS */;
INSERT INTO `direccion` VALUES (1,'Corro',123),(2,'Belgrano',457);
/*!40000 ALTER TABLE `direccion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_usuario_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_usuario_id` FOREIGN KEY (`user_id`) REFERENCES `usuario` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2024-09-17 14:11:35.408937','2','admin@gmail.com',1,'[{\"added\": {}}]',10,1),(2,'2024-09-17 14:13:09.383154','2','admin@gmail.com',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Telefono\"]}}]',10,1),(3,'2024-09-17 14:18:27.814116','3','cliente@gmail.com',1,'[{\"added\": {}}]',10,1),(4,'2024-09-17 14:19:09.283381','3','cliente@gmail.com',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Telefono\"]}}]',10,1),(5,'2024-09-17 14:19:32.183719','2','admin@gmail.com',2,'[{\"changed\": {\"fields\": [\"Staff status\"]}}]',10,1),(6,'2024-09-17 14:20:21.856104','1','Corro, 123',1,'[{\"added\": {}}]',8,1),(7,'2024-09-17 14:21:06.589868','2','Belgrano, 457',1,'[{\"added\": {}}]',8,1),(8,'2024-09-17 14:21:27.941409','2','admin@gmail.com',2,'[{\"changed\": {\"fields\": [\"Direccion\"]}}]',10,1),(9,'2024-09-17 14:21:41.467557','3','cliente@gmail.com',2,'[{\"changed\": {\"fields\": [\"Direccion\"]}}]',10,1),(10,'2024-09-17 14:24:59.773468','1','Tasty Ricca',1,'[{\"added\": {}}]',9,1),(11,'2024-09-17 14:50:59.270427','2','American',1,'[{\"added\": {}}]',9,1),(12,'2024-09-17 14:52:15.971606','3','Louis\' Honor',1,'[{\"added\": {}}]',9,1),(13,'2024-09-17 14:53:24.301737','4','Lambhaus',1,'[{\"added\": {}}]',9,1),(14,'2024-09-17 15:18:56.900227','5','Ricca',1,'[{\"added\": {}}]',9,1),(15,'2024-09-17 15:20:14.640376','6','Double Cheese & Bacon',1,'[{\"added\": {}}]',9,1),(16,'2024-09-17 15:20:58.308496','7','Lassen Wurst',1,'[{\"added\": {}}]',9,1),(17,'2024-09-17 15:21:40.420402','8','King Kong Burguer',1,'[{\"added\": {}}]',9,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(6,'authtoken','token'),(7,'authtoken','tokenproxy'),(4,'contenttypes','contenttype'),(10,'ricco_app','customuser'),(8,'ricco_app','direccion'),(9,'ricco_app','producto'),(5,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2024-09-17 13:49:10.707442'),(2,'contenttypes','0002_remove_content_type_name','2024-09-17 13:49:10.816352'),(3,'auth','0001_initial','2024-09-17 13:49:11.210382'),(4,'auth','0002_alter_permission_name_max_length','2024-09-17 13:49:11.297211'),(5,'auth','0003_alter_user_email_max_length','2024-09-17 13:49:11.313823'),(6,'auth','0004_alter_user_username_opts','2024-09-17 13:49:11.340064'),(7,'auth','0005_alter_user_last_login_null','2024-09-17 13:49:11.364561'),(8,'auth','0006_require_contenttypes_0002','2024-09-17 13:49:11.374094'),(9,'auth','0007_alter_validators_add_error_messages','2024-09-17 13:49:11.379922'),(10,'auth','0008_alter_user_username_max_length','2024-09-17 13:49:11.413577'),(11,'auth','0009_alter_user_last_name_max_length','2024-09-17 13:49:11.430084'),(12,'auth','0010_alter_group_name_max_length','2024-09-17 13:49:11.463907'),(13,'auth','0011_update_proxy_permissions','2024-09-17 13:49:11.479665'),(14,'auth','0012_alter_user_first_name_max_length','2024-09-17 13:49:11.506003'),(15,'ricco_app','0001_initial','2024-09-17 13:49:12.011344'),(16,'admin','0001_initial','2024-09-17 13:49:12.185466'),(17,'admin','0002_logentry_remove_auto_add','2024-09-17 13:49:12.212455'),(18,'admin','0003_logentry_add_action_flag_choices','2024-09-17 13:49:12.238252'),(19,'authtoken','0001_initial','2024-09-17 13:49:12.396780'),(20,'authtoken','0002_auto_20160226_1747','2024-09-17 13:49:12.479727'),(21,'authtoken','0003_tokenproxy','2024-09-17 13:49:12.503180'),(22,'authtoken','0004_alter_tokenproxy_options','2024-09-17 13:49:12.518185'),(23,'ricco_app','0003_alter_customuser_username_alter_direccion_barrio','2024-09-17 13:52:57.181949'),(24,'sessions','0001_initial','2024-09-17 13:55:04.418061');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('x2iyj5rmvolu2prc6g41ivqpbd70gd2g','.eJxVjMsOwiAQAP-FsyHL8ioevfsNBNhVqoYmpT0Z_92Q9KDXmcm8RUz7VuPeeY0zibNQ4vTLcipPbkPQI7X7IsvStnXOciTysF1eF-LX5Wj_BjX1OrbJq8QBC4BD8IVLnkgZJJdRZw2GgdzNApMKgTR6hVMIYK1GSyUb8fkC1HI3KA:1sqYi4:dnWpn0b3fUKuoe8ALpjkPb6z-9b4x3QO4O0Lpe6OU7c','2024-10-01 13:57:40.909436');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `producto`
--

DROP TABLE IF EXISTS `producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `producto` (
  `id_producto` int NOT NULL AUTO_INCREMENT,
  `nombre_producto` varchar(100) NOT NULL,
  `descripcion` longtext NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id_producto`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producto`
--

LOCK TABLES `producto` WRITE;
/*!40000 ALTER TABLE `producto` DISABLE KEYS */;
INSERT INTO `producto` VALUES (1,'Tasty Ricca','Pan casero. Burger de carne 220gr. Queso cheddar fundido, lechuga, tomate huevo planchado, panceta crocante y cebolla asada',2450.00),(2,'American','Pan casero. Burger de carne 200gr. Queso cheddar fundido con panceta crocante y huevo a la plancha',3900.00),(3,'Louis\' Honor','Pan casero. Doble burguer de carne 200gr. Queso azul fundido. Cebolla caramelizada. Panceta crocante. Champignones asados. Rúcula',4100.00),(4,'Lambhaus','Pan casero. Burger de cordero 190gr. Queso brie fundido con frutos secos. Cebolla al malbec',2780.00),(5,'Ricca','Pan casero. Burger de carne 200gr. Queso muzzarella fundido. Aros de cebolla fritos. Panceta crocante. Guacamole',3250.00),(6,'Double Cheese & Bacon','Pan casero. Doble burger de carne 200gr. Doble queso cheddar. Panceta. Cebolla',4450.00),(7,'Lassen Wurst','Pan ciabatta de aceitunas. Sandwich de chorizo alemán 140gr. Queso dambo fundido. Cebolla caramelizada. Panceta crocante',3450.00),(8,'King Kong Burguer','Para compartir!!! 6/8 porciones. Impresionante Burger XXL de 1kg, de carne, con queso cheddar fundido, lechuga, tomate y panceta crocante',4500.00);
/*!40000 ALTER TABLE `producto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `username` varchar(150) DEFAULT NULL,
  `email` varchar(150) NOT NULL,
  `telefono` varchar(50) DEFAULT NULL,
  `direccion_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`),
  KEY `usuario_direccion_id_4d2cc5e4_fk_direccion_id_direccion` (`direccion_id`),
  CONSTRAINT `usuario_direccion_id_4d2cc5e4_fk_direccion_id_direccion` FOREIGN KEY (`direccion_id`) REFERENCES `direccion` (`id_direccion`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (1,'pbkdf2_sha256$600000$fwI4wftgoRgF7OQMBlfaAB$xQYR1vVVmEvFfhVt2jseHqai6Jg/cefJrSyRz3ki1Gk=','2024-09-17 13:57:40.903305',1,'','',1,1,'2024-09-17 13:56:31.866080',NULL,'cosmarian@gmail.com',NULL,NULL),(2,'pbkdf2_sha256$600000$YrpTSdaU3qUVzO8wrDNYn9$6yAT4CShh5/uO7ProiZX+KyTXU3zXG7Utd7TKPOKQas=',NULL,0,'Juan','Perez',1,1,'2024-09-17 14:11:34.000000',NULL,'admin@gmail.com','351987654',1),(3,'pbkdf2_sha256$600000$PJoRjHo5XeR8wFORPsL9HJ$6ACHZFEYo2Y/4z7NbrxYUnlTcIif597PKXM6dGkqzYw=',NULL,0,'Rosa','Lopez',0,1,'2024-09-17 14:18:27.000000',NULL,'cliente@gmail.com','351456778',2);
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario_groups`
--

DROP TABLE IF EXISTS `usuario_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuario_groups_customuser_id_group_id_18e8ca87_uniq` (`customuser_id`,`group_id`),
  KEY `usuario_groups_group_id_c67c8651_fk_auth_group_id` (`group_id`),
  CONSTRAINT `usuario_groups_customuser_id_dae56c50_fk_usuario_id` FOREIGN KEY (`customuser_id`) REFERENCES `usuario` (`id`),
  CONSTRAINT `usuario_groups_group_id_c67c8651_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario_groups`
--

LOCK TABLES `usuario_groups` WRITE;
/*!40000 ALTER TABLE `usuario_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `usuario_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario_user_permissions`
--

DROP TABLE IF EXISTS `usuario_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuario_user_permissions_customuser_id_permission_956f0d16_uniq` (`customuser_id`,`permission_id`),
  KEY `usuario_user_permiss_permission_id_a8893ce7_fk_auth_perm` (`permission_id`),
  CONSTRAINT `usuario_user_permiss_permission_id_a8893ce7_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `usuario_user_permissions_customuser_id_f3811ba0_fk_usuario_id` FOREIGN KEY (`customuser_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario_user_permissions`
--

LOCK TABLES `usuario_user_permissions` WRITE;
/*!40000 ALTER TABLE `usuario_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `usuario_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-09-17 13:14:27
