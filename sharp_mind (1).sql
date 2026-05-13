-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 13-05-2026 a las 03:35:32
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `sharp_mind`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add imagen', 6, 'add_imagen'),
(22, 'Can change imagen', 6, 'change_imagen'),
(23, 'Can delete imagen', 6, 'delete_imagen'),
(24, 'Can view imagen', 6, 'view_imagen'),
(25, 'Can add user', 7, 'add_customuser'),
(26, 'Can change user', 7, 'change_customuser'),
(27, 'Can delete user', 7, 'delete_customuser'),
(28, 'Can view user', 7, 'view_customuser'),
(29, 'Can add user session', 8, 'add_usersession'),
(30, 'Can change user session', 8, 'change_usersession'),
(31, 'Can delete user session', 8, 'delete_usersession'),
(32, 'Can view user session', 8, 'view_usersession'),
(33, 'Can add post', 9, 'add_post'),
(34, 'Can change post', 9, 'change_post'),
(35, 'Can delete post', 9, 'delete_post'),
(36, 'Can view post', 9, 'view_post'),
(37, 'Can add producto', 10, 'add_producto'),
(38, 'Can change producto', 10, 'change_producto'),
(39, 'Can delete producto', 10, 'delete_producto'),
(40, 'Can view producto', 10, 'view_producto'),
(41, 'Can add topic_section', 11, 'add_topic_section'),
(42, 'Can change topic_section', 11, 'change_topic_section'),
(43, 'Can delete topic_section', 11, 'delete_topic_section'),
(44, 'Can view topic_section', 11, 'view_topic_section'),
(45, 'Can add topics_group', 12, 'add_topics_group'),
(46, 'Can change topics_group', 12, 'change_topics_group'),
(47, 'Can delete topics_group', 12, 'delete_topics_group'),
(48, 'Can view topics_group', 12, 'view_topics_group');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `catalog_post`
--

CREATE TABLE `catalog_post` (
  `id` bigint(20) NOT NULL,
  `content` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  `group_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `catalog_producto`
--

CREATE TABLE `catalog_producto` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` longtext NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `stock` int(11) NOT NULL,
  `imagen` varchar(100) DEFAULT NULL,
  `imagen_url` varchar(200) DEFAULT NULL,
  `categoria` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `catalog_topics_group`
--

CREATE TABLE `catalog_topics_group` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `categoria` varchar(100) NOT NULL,
  `imagen` varchar(100) DEFAULT NULL,
  `imagen_url` varchar(200) DEFAULT NULL,
  `score` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `catalog_topics_group`
--

INSERT INTO `catalog_topics_group` (`id`, `nombre`, `categoria`, `imagen`, `imagen_url`, `score`) VALUES
(1, 'quimica organica', 'quimica', 'catalog/group/image/quimica_1.webp', '', 0),
(2, 'quimica inorganica', 'quimica', 'catalog/group/image/quimica_2.webp', '', 0),
(3, 'quimica', 'quimica', 'catalog/group/image/quimica_3.webp', '', 0),
(4, 'quimica molecular', 'quimica', 'catalog/group/image/quimica_5.webp', '', 0),
(5, 'quimica 2', 'quimica', 'catalog/group/image/quimica_6.webp', '', 0),
(6, 'quimica 3', 'quimica', 'catalog/group/image/quimica_7.webp', '', 0),
(7, 'quimica 4', 'quimica', 'catalog/group/image/quimica_8.webp', '', 0),
(8, 'quimica 5', 'quimica', 'catalog/group/image/quimica_9.webp', '', 0),
(12, 'quimica 10', 'quimica', 'catalog/group/image/quimica_10_sirQKya.webp', '', 0),
(14, 'matematicas 1', 'matematicas', 'catalog/group/image/1.webp', '', 0),
(15, 'matematicas 2', 'matematicas', 'catalog/group/image/22.webp', '', 0),
(16, 'matematicas 3', 'matematicas', 'catalog/group/image/3.webp', '', 0),
(17, 'matematicas 4', 'matematicas', 'catalog/group/image/4.webp', '', 0),
(18, 'matematicas 5', 'matematicas', 'catalog/group/image/5.webp', '', 0),
(19, 'matematicas 6', 'matematicas', 'catalog/group/image/6.webp', '', 0),
(20, 'matematicas 7', 'matematicas', 'catalog/group/image/7.webp', '', 0),
(21, 'matematicas 8', 'matematicas', 'catalog/group/image/8.webp', '', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `catalog_topics_group_posts`
--

CREATE TABLE `catalog_topics_group_posts` (
  `id` bigint(20) NOT NULL,
  `topics_group_id` bigint(20) NOT NULL,
  `post_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `catalog_topics_group_users_joined`
--

CREATE TABLE `catalog_topics_group_users_joined` (
  `id` bigint(20) NOT NULL,
  `topics_group_id` bigint(20) NOT NULL,
  `customuser_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `catalog_topic_section`
--

CREATE TABLE `catalog_topic_section` (
  `id` bigint(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `group_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `catalog_topic_section_posts`
--

CREATE TABLE `catalog_topic_section_posts` (
  `id` bigint(20) NOT NULL,
  `topic_section_id` bigint(20) NOT NULL,
  `post_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL
) ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(9, 'catalog', 'post'),
(10, 'catalog', 'producto'),
(12, 'catalog', 'topics_group'),
(11, 'catalog', 'topic_section'),
(4, 'contenttypes', 'contenttype'),
(5, 'sessions', 'session'),
(7, 'users', 'customuser'),
(6, 'users', 'imagen'),
(8, 'users', 'usersession');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2026-05-12 23:56:39.010641'),
(2, 'contenttypes', '0002_remove_content_type_name', '2026-05-12 23:56:39.221686'),
(3, 'auth', '0001_initial', '2026-05-12 23:56:39.729135'),
(4, 'auth', '0002_alter_permission_name_max_length', '2026-05-12 23:56:39.833841'),
(5, 'auth', '0003_alter_user_email_max_length', '2026-05-12 23:56:39.842142'),
(6, 'auth', '0004_alter_user_username_opts', '2026-05-12 23:56:39.854915'),
(7, 'auth', '0005_alter_user_last_login_null', '2026-05-12 23:56:39.867496'),
(8, 'auth', '0006_require_contenttypes_0002', '2026-05-12 23:56:39.873667'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2026-05-12 23:56:39.883436'),
(10, 'auth', '0008_alter_user_username_max_length', '2026-05-12 23:56:39.896724'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2026-05-12 23:56:39.906844'),
(12, 'auth', '0010_alter_group_name_max_length', '2026-05-12 23:56:39.938164'),
(13, 'auth', '0011_update_proxy_permissions', '2026-05-12 23:56:39.951710'),
(14, 'auth', '0012_alter_user_first_name_max_length', '2026-05-12 23:56:39.965359'),
(15, 'users', '0001_initial', '2026-05-12 23:56:40.727228'),
(16, 'admin', '0001_initial', '2026-05-12 23:56:40.960023'),
(17, 'admin', '0002_logentry_remove_auto_add', '2026-05-12 23:56:40.972577'),
(18, 'admin', '0003_logentry_add_action_flag_choices', '2026-05-12 23:56:40.987930'),
(19, 'catalog', '0001_initial', '2026-05-12 23:56:41.129816'),
(20, 'catalog', '0002_initial', '2026-05-12 23:56:42.275831'),
(21, 'catalog', '0003_alter_post_user', '2026-05-12 23:56:42.550599'),
(22, 'sessions', '0001_initial', '2026-05-12 23:56:42.623218'),
(23, 'users', '0002_alter_imagen_imagen', '2026-05-12 23:56:42.631984'),
(24, 'users', '0003_customuser_is_banned', '2026-05-12 23:56:42.802908'),
(25, 'users', '0004_usersession_logout_time_alter_usersession_login_time', '2026-05-12 23:56:42.900231'),
(26, 'users', '0005_alter_customuser_imagen', '2026-05-12 23:56:43.091415');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('c5slojet42cjwtgj3v3yltrxv1xffd4j', '.eJxVjLsOwjAMAP8lM4ryaEzCyM43RHbtkAJqpaadEP-OInWA9e50b5Vx32rem6x5YnVRVp1-GeH4lLkLfuB8X_S4zNs6ke6JPmzTt4XldT3av0HFVvvWBg8RvE-MBYGRizVFAhk_BCI0YIeQjAwcnQPnhARiAUPkSdIZ1ecL2kc38A:1wMx0w:wFgonq8AMTHvdGmRRa_Vpw-Vb8PbZYnxI0SQ-SuLkUA', '2026-05-26 23:59:50.823850');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users_customuser`
--

CREATE TABLE `users_customuser` (
  `id` bigint(20) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `email` varchar(254) NOT NULL,
  `imagen` varchar(100) NOT NULL,
  `score` int(11) NOT NULL,
  `is_banned` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `users_customuser`
--

INSERT INTO `users_customuser` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `is_staff`, `is_active`, `date_joined`, `email`, `imagen`, `score`, `is_banned`) VALUES
(1, 'pbkdf2_sha256$1000000$f2c1nlvGsVlrCX55ncr16C$SOcabis+aZSSpDJU5MW6ZsEtWU0ryHx2+iN+z9iLrSU=', '2026-05-12 23:59:50.803487', 0, 'david', '', '', 0, 1, '2026-05-12 23:59:45.783415', 'david@gmail.com', 'imagenes/platon.webp', 0, 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users_customuser_groups`
--

CREATE TABLE `users_customuser_groups` (
  `id` bigint(20) NOT NULL,
  `customuser_id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users_customuser_user_permissions`
--

CREATE TABLE `users_customuser_user_permissions` (
  `id` bigint(20) NOT NULL,
  `customuser_id` bigint(20) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users_imagen`
--

CREATE TABLE `users_imagen` (
  `id` bigint(20) NOT NULL,
  `imagen` varchar(100) NOT NULL,
  `imagen_url` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users_usersession`
--

CREATE TABLE `users_usersession` (
  `id` bigint(20) NOT NULL,
  `ip_address` char(39) NOT NULL,
  `user_agent` longtext NOT NULL,
  `device_id` varchar(128) NOT NULL,
  `login_time` datetime(6) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `logout_time` datetime(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `users_usersession`
--

INSERT INTO `users_usersession` (`id`, `ip_address`, `user_agent`, `device_id`, `login_time`, `is_active`, `user_id`, `logout_time`) VALUES
(1, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36 Edg/148.0.0.0', '76a70dd8-7f1b-4be5-888a-2af8ca7b7b3e', '2026-05-12 23:59:50.766442', 1, 1, NULL);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indices de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indices de la tabla `catalog_post`
--
ALTER TABLE `catalog_post`
  ADD PRIMARY KEY (`id`),
  ADD KEY `catalog_post_group_id_31c40b93_fk_catalog_topics_group_id` (`group_id`),
  ADD KEY `catalog_post_user_id_69662eaf_fk_users_customuser_id` (`user_id`);

--
-- Indices de la tabla `catalog_producto`
--
ALTER TABLE `catalog_producto`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `catalog_topics_group`
--
ALTER TABLE `catalog_topics_group`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `catalog_topics_group_posts`
--
ALTER TABLE `catalog_topics_group_posts`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `catalog_topics_group_posts_topics_group_id_post_id_ea64b589_uniq` (`topics_group_id`,`post_id`),
  ADD KEY `catalog_topics_group_posts_post_id_120c16a4_fk_catalog_post_id` (`post_id`);

--
-- Indices de la tabla `catalog_topics_group_users_joined`
--
ALTER TABLE `catalog_topics_group_users_joined`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `catalog_topics_group_use_topics_group_id_customus_8ca16dd3_uniq` (`topics_group_id`,`customuser_id`),
  ADD KEY `catalog_topics_group_customuser_id_a788d052_fk_users_cus` (`customuser_id`);

--
-- Indices de la tabla `catalog_topic_section`
--
ALTER TABLE `catalog_topic_section`
  ADD PRIMARY KEY (`id`),
  ADD KEY `catalog_topic_sectio_group_id_6876a3ee_fk_catalog_t` (`group_id`);

--
-- Indices de la tabla `catalog_topic_section_posts`
--
ALTER TABLE `catalog_topic_section_posts`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `catalog_topic_section_po_topic_section_id_post_id_a8dacc9f_uniq` (`topic_section_id`,`post_id`),
  ADD KEY `catalog_topic_section_posts_post_id_ab4f6419_fk_catalog_post_id` (`post_id`);

--
-- Indices de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_users_customuser_id` (`user_id`);

--
-- Indices de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indices de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indices de la tabla `users_customuser`
--
ALTER TABLE `users_customuser`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indices de la tabla `users_customuser_groups`
--
ALTER TABLE `users_customuser_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `users_customuser_groups_customuser_id_group_id_76b619e3_uniq` (`customuser_id`,`group_id`),
  ADD KEY `users_customuser_groups_group_id_01390b14_fk_auth_group_id` (`group_id`);

--
-- Indices de la tabla `users_customuser_user_permissions`
--
ALTER TABLE `users_customuser_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `users_customuser_user_pe_customuser_id_permission_7a7debf6_uniq` (`customuser_id`,`permission_id`),
  ADD KEY `users_customuser_use_permission_id_baaa2f74_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `users_imagen`
--
ALTER TABLE `users_imagen`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `users_usersession`
--
ALTER TABLE `users_usersession`
  ADD PRIMARY KEY (`id`),
  ADD KEY `users_usersession_user_id_2873d35e_fk_users_customuser_id` (`user_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=49;

--
-- AUTO_INCREMENT de la tabla `catalog_post`
--
ALTER TABLE `catalog_post`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `catalog_producto`
--
ALTER TABLE `catalog_producto`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `catalog_topics_group`
--
ALTER TABLE `catalog_topics_group`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT de la tabla `catalog_topics_group_posts`
--
ALTER TABLE `catalog_topics_group_posts`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `catalog_topics_group_users_joined`
--
ALTER TABLE `catalog_topics_group_users_joined`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `catalog_topic_section`
--
ALTER TABLE `catalog_topic_section`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `catalog_topic_section_posts`
--
ALTER TABLE `catalog_topic_section_posts`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT de la tabla `users_customuser`
--
ALTER TABLE `users_customuser`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `users_customuser_groups`
--
ALTER TABLE `users_customuser_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `users_customuser_user_permissions`
--
ALTER TABLE `users_customuser_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `users_imagen`
--
ALTER TABLE `users_imagen`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `users_usersession`
--
ALTER TABLE `users_usersession`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Filtros para la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Filtros para la tabla `catalog_post`
--
ALTER TABLE `catalog_post`
  ADD CONSTRAINT `catalog_post_group_id_31c40b93_fk_catalog_topics_group_id` FOREIGN KEY (`group_id`) REFERENCES `catalog_topics_group` (`id`),
  ADD CONSTRAINT `catalog_post_user_id_69662eaf_fk_users_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `users_customuser` (`id`);

--
-- Filtros para la tabla `catalog_topics_group_posts`
--
ALTER TABLE `catalog_topics_group_posts`
  ADD CONSTRAINT `catalog_topics_group_posts_post_id_120c16a4_fk_catalog_post_id` FOREIGN KEY (`post_id`) REFERENCES `catalog_post` (`id`),
  ADD CONSTRAINT `catalog_topics_group_topics_group_id_e2a411bd_fk_catalog_t` FOREIGN KEY (`topics_group_id`) REFERENCES `catalog_topics_group` (`id`);

--
-- Filtros para la tabla `catalog_topics_group_users_joined`
--
ALTER TABLE `catalog_topics_group_users_joined`
  ADD CONSTRAINT `catalog_topics_group_customuser_id_a788d052_fk_users_cus` FOREIGN KEY (`customuser_id`) REFERENCES `users_customuser` (`id`),
  ADD CONSTRAINT `catalog_topics_group_topics_group_id_f2277813_fk_catalog_t` FOREIGN KEY (`topics_group_id`) REFERENCES `catalog_topics_group` (`id`);

--
-- Filtros para la tabla `catalog_topic_section`
--
ALTER TABLE `catalog_topic_section`
  ADD CONSTRAINT `catalog_topic_sectio_group_id_6876a3ee_fk_catalog_t` FOREIGN KEY (`group_id`) REFERENCES `catalog_topics_group` (`id`);

--
-- Filtros para la tabla `catalog_topic_section_posts`
--
ALTER TABLE `catalog_topic_section_posts`
  ADD CONSTRAINT `catalog_topic_sectio_topic_section_id_ad670f45_fk_catalog_t` FOREIGN KEY (`topic_section_id`) REFERENCES `catalog_topic_section` (`id`),
  ADD CONSTRAINT `catalog_topic_section_posts_post_id_ab4f6419_fk_catalog_post_id` FOREIGN KEY (`post_id`) REFERENCES `catalog_post` (`id`);

--
-- Filtros para la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_users_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `users_customuser` (`id`);

--
-- Filtros para la tabla `users_customuser_groups`
--
ALTER TABLE `users_customuser_groups`
  ADD CONSTRAINT `users_customuser_gro_customuser_id_958147bf_fk_users_cus` FOREIGN KEY (`customuser_id`) REFERENCES `users_customuser` (`id`),
  ADD CONSTRAINT `users_customuser_groups_group_id_01390b14_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Filtros para la tabla `users_customuser_user_permissions`
--
ALTER TABLE `users_customuser_user_permissions`
  ADD CONSTRAINT `users_customuser_use_customuser_id_5771478b_fk_users_cus` FOREIGN KEY (`customuser_id`) REFERENCES `users_customuser` (`id`),
  ADD CONSTRAINT `users_customuser_use_permission_id_baaa2f74_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);

--
-- Filtros para la tabla `users_usersession`
--
ALTER TABLE `users_usersession`
  ADD CONSTRAINT `users_usersession_user_id_2873d35e_fk_users_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `users_customuser` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
