-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 09, 2025 at 11:16 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `coffee_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `firstname` varchar(255) NOT NULL,
  `lastname` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` varchar(10) NOT NULL,
  `created_at` timestamp(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `firstname`, `lastname`, `email`, `password`, `role`, `created_at`) VALUES
(1, 'joiling', 'ford', 'joilingford@gmail.com', 'scrypt:32768:8:1$v9iWsOFKugWOUKil$cc2d0a98ec3b72a60c4c8c71a7cd60c77480756e1d632884861f1e0957ebed91bfb3ca0e384704a20e39191599716f412296fbd35c04272746e808323a2375d8', 'Admin', '2025-02-08 09:39:57.709840');

-- --------------------------------------------------------

--
-- Table structure for table `category`
--

CREATE TABLE `category` (
  `id` int(11) NOT NULL,
  `categoryname` varchar(255) NOT NULL,
  `created_at` timestamp(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `category`
--

INSERT INTO `category` (`id`, `categoryname`, `created_at`) VALUES
(3, 'coffee', '2025-02-08 10:40:11.812265'),
(4, 'softdrink', '2025-02-08 12:57:13.824598'),
(5, 'desert', '2025-02-08 10:42:23.805760'),
(6, 'breakfast food', '2025-02-08 11:51:27.591720'),
(7, 'dinner food', '2025-02-09 09:44:07.136170'),
(8, 'milktea', '2025-02-09 09:50:55.651608');

-- --------------------------------------------------------

--
-- Table structure for table `customers`
--

CREATE TABLE `customers` (
  `id` int(11) NOT NULL,
  `firstname` varchar(255) NOT NULL,
  `lastname` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `address` varchar(250) NOT NULL,
  `mobilenumber` varchar(50) NOT NULL,
  `created_at` timestamp(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `customers`
--

INSERT INTO `customers` (`id`, `firstname`, `lastname`, `email`, `password`, `address`, `mobilenumber`, `created_at`) VALUES
(1, 'joiling', 'ford', 'joilingford@gmail.com', 'scrypt:32768:8:1$nFYiVCX67tbdtqIk$61f1248b9193ae85501bd1df62557b06721606518860feaa9c3dbf6efd324200950e33233e89bd43f96d088c186e6acdcf895a8a92b08e24597d6ca4ab706859', 'Bantayan Island,Cebu', '09123456799', '2025-02-08 09:36:16.875575');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `total_price` decimal(10,2) NOT NULL,
  `status` enum('Pending','Completed','Cancelled') DEFAULT 'Pending',
  `payments` enum('Cash','ATM','Notpaid') DEFAULT 'Notpaid',
  `delivery` enum('Takeout','Dinein','Delivery') DEFAULT 'Dinein',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `id` int(11) NOT NULL,
  `category` varchar(255) NOT NULL,
  `prod_name` varchar(200) NOT NULL,
  `prod_img` varchar(200) NOT NULL,
  `prod_desc` varchar(500) NOT NULL,
  `prod_price` varchar(200) NOT NULL,
  `stock` varchar(50) NOT NULL,
  `created_at` timestamp(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `category`, `prod_name`, `prod_img`, `prod_desc`, `prod_price`, `stock`, `created_at`) VALUES
(7, '5', 'Philly', 'cheesestk.jpg', 'Cheesesteak', '200.0', '3', '2025-02-09 10:05:55.654742'),
(8, '5', 'Spaghetti ', 'spaghetti_bolognese.jpg', 'Bolognese', '200.0', '2', '2025-02-09 09:29:13.217340'),
(9, '6', 'Sandwich', 'reubensandwich.jpg', 'Reuben', '50.0', '20', '2025-02-09 09:43:20.832754'),
(10, '6', 'Sandwich', 'submarine_sndwh.jpg', 'Submarine ', '60.0', '20', '2025-02-09 09:31:30.272473'),
(11, '5', 'Burger', 'cheeseburgers.jpg', 'Cheese', '30.0', '10', '2025-02-09 09:42:22.747502'),
(12, '7', 'Jambalaya', 'Jambalaya.jpg', 'Special', '60.0', '10', '2025-02-09 09:47:35.687720'),
(13, '7', 'Buffalo Wings', 'buffalo_wings.jpg', 'Special', '320.0', '10', '2025-02-09 09:48:17.129157'),
(14, '6', 'Enchiladas', 'enchiladas.jpg', 'Special', '100.0', '2', '2025-02-09 09:49:02.711067'),
(15, '5', 'Cincinnati Chili', 'cincinnatichili.jpg', 'Special', '50.0', '6', '2025-02-09 09:49:56.431643'),
(16, '8', 'Caramel Macchiato', 'default.jpg', 'Special', '50.0', '10', '2025-02-09 09:51:43.352327'),
(17, '5', 'Cheese Curd', 'cheesecurd.jpg', 'Special', '60.0', '10', '2025-02-09 09:52:51.575026'),
(18, '5', 'Margherita Pizza', 'margherita-pizza0.jpg', 'Spicy', '150.0', '12', '2025-02-09 10:02:02.935109'),
(19, '3', 'Irish Coffee', 'irishcoffee.jpg', 'Special', '99.0', '3', '2025-02-09 10:03:27.794110'),
(20, '6', 'Chicken Nugget', 'chicnuggets.jpeg', 'Special', '300.0', '6', '2025-02-09 10:04:17.635245'),
(21, '5', 'Burger', 'pulledprk.jpeg', 'Pulled Pork', '60.0', '5', '2025-02-09 10:05:24.497501'),
(22, '5', 'Pizza', 'rhuharbpie.jpg', 'StrawberryPie', '150.0', '2', '2025-02-09 10:08:19.739423'),
(23, '3', 'Turkish Coffee', 'turkshcoffee.jpg', 'Special', '12.0', '10', '2025-02-09 10:08:54.830292'),
(24, '8', 'Whipped Milk Shake', 'milkshake.jpeg', 'Special', '90.0', '2', '2025-02-09 10:09:50.639608'),
(25, '5', 'Hot Dog', 'hotdog0.jpg', 'Special', '70.0', '5', '2025-02-09 10:10:16.847555'),
(26, '5', 'Corn Dogs', 'corndog.jpg', 'Special', '20.0', '2', '2025-02-09 10:10:48.238467'),
(27, '8', 'Frappuccino', 'frappuccino.jpg', 'Special', '60.0', '10', '2025-02-09 10:11:15.094169'),
(28, '5', 'Pepperoni Pizza', 'peperopizza.jpg', 'Special', '50.0', '2', '2025-02-09 10:11:58.030332'),
(29, '5', 'Carbonara', 'carbonaraimgre.jpg', 'Special', '50.0', '2', '2025-02-09 10:12:45.310784'),
(30, '5', 'Crab Cake', 'crabcakes.jpg', 'Special', '80.0', '5', '2025-02-09 10:13:14.654279'),
(31, '7', 'Country Fried Steak', 'country_fried_stk.jpg', 'Special', '120.0', '5', '2025-02-09 10:13:56.482520'),
(32, '3', 'Americano', 'default.jpg', 'Special', '50.0', '1', '2025-02-09 10:14:45.256288');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `category`
--
ALTER TABLE `category`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `category`
--
ALTER TABLE `category`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `customers`
--
ALTER TABLE `customers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
