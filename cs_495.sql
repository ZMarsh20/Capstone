-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 21, 2022 at 07:35 AM
-- Server version: 10.4.17-MariaDB
-- PHP Version: 8.0.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cs_495`
--

-- --------------------------------------------------------

--
-- Table structure for table `attendance`
--

DROP TABLE IF EXISTS `attendance`;
CREATE TABLE `attendance` (
  `id` int(11) NOT NULL,
  `stuID` varchar(6) NOT NULL,
  `sex` int(11) NOT NULL,
  `race` int(11) NOT NULL,
  `age` int(11) NOT NULL,
  `major` int(11) NOT NULL,
  `minor` int(11) NOT NULL,
  `major2` int(11) NOT NULL,
  `minor2` int(11) NOT NULL,
  `gradYear` int(11) NOT NULL,
  `program` tinyint(1) NOT NULL,
  `housing` tinyint(1) NOT NULL,
  `transfer` tinyint(1) NOT NULL,
  `latinx` tinyint(1) NOT NULL,
  `lgbtq` tinyint(1) NOT NULL,
  `access` datetime NOT NULL DEFAULT current_timestamp(),
  `event` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `events`
--

DROP TABLE IF EXISTS `events`;
CREATE TABLE `events` (
  `id` int(11) NOT NULL,
  `event` varchar(45) NOT NULL,
  `startTime` datetime NOT NULL,
  `endTime` datetime NOT NULL,
  `code` int(11) NOT NULL,
  `user` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `majors`
--

DROP TABLE IF EXISTS `majors`;
CREATE TABLE `majors` (
  `id` int(11) NOT NULL,
  `major` varchar(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `majors`
--

INSERT INTO `majors` (`id`, `major`) VALUES
(1, 'ACC'),
(2, 'ANTH'),
(3, 'ART'),
(4, 'BIOL'),
(5, 'BUAD'),
(6, 'CHEM'),
(7, 'COM'),
(8, 'CS'),
(9, 'ECON'),
(10, 'EDUC'),
(11, 'ENGR'),
(12, 'ENG'),
(13, 'ENVS'),
(14, 'ESS'),
(15, 'GEOG'),
(16, 'GEOL'),
(17, 'HIST'),
(18, 'MATH'),
(19, 'MUS'),
(20, 'NTR'),
(21, 'PHIL'),
(22, 'PHYS'),
(23, 'POLS'),
(24, 'PSY'),
(25, 'ROE'),
(26, 'SOC'),
(27, 'SPAN'),
(28, 'None');

-- --------------------------------------------------------

--
-- Table structure for table `race`
--

DROP TABLE IF EXISTS `race`;
CREATE TABLE `race` (
  `id` int(11) NOT NULL,
  `race` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `race`
--

INSERT INTO `race` (`id`, `race`) VALUES
(2, 'african america'),
(4, 'asian'),
(7, 'asian pacific islander'),
(3, 'hispanic'),
(5, 'indian'),
(6, 'native american'),
(8, 'other'),
(1, 'white'),
(9, 'white / african american'),
(10, 'white / hispanic'),
(11, 'white / asian'),
(12, 'white / asian pacific islander'),
(13, 'white / indian'),
(14, 'white / native american'),
(15, 'white / other'),
(16, 'african american / hispanic'),
(17, 'african american / asian'),
(18, 'african american / asian pacific islande'),
(19, 'african american / indian'),
(20, 'african american / native american'),
(21, 'african american / other'),
(22, 'hispanic / asian'),
(23, 'hispanic / asian pacific islander'),
(24, 'hispanic / indian'),
(25, 'hispanic / native american'),
(26, 'hispanic / other'),
(27, 'asian / asian pacific islander'),
(28, 'asian / indian'),
(29, 'asian / native american'),
(30, 'asian / other'),
(31, 'asian pacific islander / indian'),
(32, 'asian pacific islander / native american'),
(33, 'asian pacific islander / other'),
(34, 'indian / native american'),
(35, 'indian / other'),
(36, 'native american / other');

-- --------------------------------------------------------

--
-- Table structure for table `sex`
--

DROP TABLE IF EXISTS `sex`;
CREATE TABLE `sex` (
  `id` int(11) NOT NULL,
  `sex` varchar(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `sex`
--

INSERT INTO `sex` (`id`, `sex`) VALUES
(2, 'female'),
(1, 'male'),
(3, 'other');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(40) DEFAULT NULL,
  `password` varchar(80) DEFAULT NULL,
  `name` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `attendance`
--
ALTER TABLE `attendance`
  ADD PRIMARY KEY (`id`),
  ADD KEY `event` (`event`);

--
-- Indexes for table `events`
--
ALTER TABLE `events`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user` (`user`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `attendance`
--
ALTER TABLE `attendance`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `events`
--
ALTER TABLE `events`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
