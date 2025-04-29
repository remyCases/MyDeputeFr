CREATE TABLE IF NOT EXISTS `notification` (
  `id` int(11) NOT NULL,
  `user_id` varchar(20) NOT NULL,
  `depute_ref` varchar(20) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);