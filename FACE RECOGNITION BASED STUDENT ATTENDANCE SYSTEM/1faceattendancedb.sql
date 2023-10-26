-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Apr 07, 2023 at 08:21 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `1faceattendancedb`
--

-- --------------------------------------------------------

--
-- Table structure for table `attentb`
--

CREATE TABLE `attentb` (
  `id` bigint(250) NOT NULL auto_increment,
  `Date` varchar(250) NOT NULL,
  `Time` varchar(250) NOT NULL,
  `Degree` varchar(250) NOT NULL,
  `Department` varchar(250) NOT NULL,
  `Year` varchar(250) NOT NULL,
  `Regno` varchar(250) NOT NULL,
  `Status` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=45 ;

--
-- Dumping data for table `attentb`
--

INSERT INTO `attentb` (`id`, `Date`, `Time`, `Degree`, `Department`, `Year`, `Regno`, `Status`) VALUES
(30, '2023-01-25', '14:14:15', 'UG', 'BSC', '2017', '345678', '1'),
(31, '2023-02-11', '15:30:08', 'UG', 'BSC', '2017', '4019', '1'),
(32, '2023-02-11', '15:41:12', 'UG', 'BE', '2019', '5535', '1'),
(33, '2023-02-21', '13:19:55', 'PG', 'MSC', '2020', 'p21270921', '1'),
(34, '2023-03-14', '19:28:47', 'UG', 'BSC', '2020', '1920', '1'),
(35, '2023-03-24', '15:18:33', 'UG', 'BE', '2019', '5535', '1'),
(36, '2023-03-24', '15:21:45', 'UG', 'BSC', '2020', '621419104010', '1'),
(37, '2023-03-24', '15:40:15', 'UG', 'BSC', '2020', '1920', '0'),
(38, '2023-04-04', '12:33:57', 'PG', 'MSC', '2020', '13226', '1'),
(39, '2023-04-04', '14:05:03', 'PG', 'MSC', '2020', '5656', '1'),
(40, '2023-04-04', '14:05:32', 'UG', 'BSC', '2020', '1920', '0'),
(41, '2023-04-07', '13:44:05', 'UG', 'BSC', '2020', '814419104009', '1'),
(42, '2023-04-07', '13:45:13', 'UG', 'BSC', '2020', '1920', '0'),
(43, '2023-04-07', '13:45:14', 'PG', 'MSC', '2020', '5656', '0'),
(44, '2023-04-07', '13:47:49', 'UG', 'BSC', '2020', '814419104006', '1');

-- --------------------------------------------------------

--
-- Table structure for table `regtb`
--

CREATE TABLE `regtb` (
  `Regno` varchar(250) NOT NULL,
  `Name` varchar(250) NOT NULL,
  `Gender` varchar(250) NOT NULL,
  `Age` varchar(250) NOT NULL,
  `Email` varchar(250) NOT NULL,
  `Phone` varchar(250) NOT NULL,
  `Address` varchar(250) NOT NULL,
  `Degree` varchar(250) NOT NULL,
  `Department` varchar(250) NOT NULL,
  `Year` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `regtb`
--

INSERT INTO `regtb` (`Regno`, `Name`, `Gender`, `Age`, `Email`, `Phone`, `Address`, `Degree`, `Department`, `Year`) VALUES
('1920', 'srinivasan', 'male', '20', 'sangeeth5535@gmail.com', '9486365535', 'No 16, Samnath Plaza, Madurai Main Road, Melapudhur', 'UG', 'BSC', '2020'),
('5656', 'Sangeeth Kumar', 'male', '20', 'sangeeth5535@gmail.com', '9080951184', 'No 16 samnath plaza, melapudur  trichy', 'PG', 'MSC', '2020'),
('814419104009', 'kalai', 'female', '20', 'kalai@gmail.com', '7010157910', 'dgh', 'UG', 'BSC', '2020'),
('814419104006', 'harini', 'female', '20', 'harini@gmail.com', '6382898279', 'No 16, Samnath Plaza, Madurai Main Road, Melapudhur', 'UG', 'BSC', '2020');
