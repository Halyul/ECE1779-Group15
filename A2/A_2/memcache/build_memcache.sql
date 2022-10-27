-- MySQL dump 10.13  Distrib 8.0.30, for Win64 (x86_64)
--
-- Host: localhost    Database: ece1779_memcache
-- ------------------------------------------------------
-- Server version	8.0.30

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `keys_table`
--

DROP TABLE IF EXISTS `keys_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `keys_table` (
  `key_id` int NOT NULL AUTO_INCREMENT,
  `key_string` varchar(45) NOT NULL,
  `path_string` varchar(45) NOT NULL,
  PRIMARY KEY (`key_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `keys_table`
--

LOCK TABLES `keys_table` WRITE;
/*!40000 ALTER TABLE `keys_table` DISABLE KEYS */;
/*!40000 ALTER TABLE `keys_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `memcache_config`
--

DROP TABLE IF EXISTS `memcache_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `memcache_config` (
  `id` int NOT NULL AUTO_INCREMENT,
  `capacity` int NOT NULL,
  `replacement_policy` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `memcache_config`
--

LOCK TABLES `memcache_config` WRITE;
/*!40000 ALTER TABLE `memcache_config` DISABLE KEYS */;
INSERT INTO `memcache_config` VALUES (1,1,'Random');
/*!40000 ALTER TABLE `memcache_config` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `statistics`
--

DROP TABLE IF EXISTS `statistics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `statistics` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cache_nums` int NOT NULL,
  `used_size` int NOT NULL,
  `total_request_served` int NOT NULL,
  `total_hit` int NOT NULL,
  `miss_rate` float DEFAULT NULL,
  `hit_rate` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `statistics`
--

LOCK TABLES `statistics` WRITE;
/*!40000 ALTER TABLE `statistics` DISABLE KEYS */;
INSERT INTO `statistics` VALUES (1,0,0,0,0,NULL,NULL);
/*!40000 ALTER TABLE `statistics` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `statistics_10min`
--

DROP TABLE IF EXISTS `statistics_10min`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `statistics_10min` (
  `time` varchar(40) NOT NULL,
  `num_item_added` int NOT NULL,
  `capacity_used` int NOT NULL,
  `num_request_served` int NOT NULL,
  `num_miss` int NOT NULL,
  `num_hit` int NOT NULL,
  PRIMARY KEY (`time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `statistics_10min`
--

LOCK TABLES `statistics_10min` WRITE;
/*!40000 ALTER TABLE `statistics_10min` DISABLE KEYS */;
/*!40000 ALTER TABLE `statistics_10min` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-10-05 19:46:39
