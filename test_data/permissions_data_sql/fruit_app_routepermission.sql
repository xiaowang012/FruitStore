/*
 Navicat Premium Data Transfer

 Source Server         : mysql_localhost
 Source Server Type    : MySQL
 Source Server Version : 80021
 Source Host           : localhost:3306
 Source Schema         : fruit_database

 Target Server Type    : MySQL
 Target Server Version : 80021
 File Encoding         : 65001

 Date: 05/05/2022 22:56:25
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for fruit_app_routepermission
-- ----------------------------
DROP TABLE IF EXISTS `fruit_app_routepermission`;
CREATE TABLE `fruit_app_routepermission`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `group_name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `url` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `description` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `add_route_permission_time` datetime(6) NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 59 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of fruit_app_routepermission
-- ----------------------------
INSERT INTO `fruit_app_routepermission` VALUES (59, 'admin', '/admin/', '测试权限URL', '2022-05-05 22:23:57.712303');
INSERT INTO `fruit_app_routepermission` VALUES (60, 'admin', '/login/', '测试权限URL', '2022-05-05 22:23:57.766898');
INSERT INTO `fruit_app_routepermission` VALUES (61, 'admin', '/register/', '测试权限URL', '2022-05-05 22:23:57.784891');
INSERT INTO `fruit_app_routepermission` VALUES (62, 'admin', '/logout/', '测试权限URL', '2022-05-05 22:23:57.794879');
INSERT INTO `fruit_app_routepermission` VALUES (63, 'admin', '/index/', '测试权限URL', '2022-05-05 22:23:57.801846');
INSERT INTO `fruit_app_routepermission` VALUES (64, 'admin', '/index_send_message/', '测试权限URL', '2022-05-05 22:23:57.811818');
INSERT INTO `fruit_app_routepermission` VALUES (65, 'admin', '/delete/message', '测试权限URL', '2022-05-05 22:23:57.820798');
INSERT INTO `fruit_app_routepermission` VALUES (66, 'admin', '/morefruits/get', '测试权限URL', '2022-05-05 22:23:57.827776');
INSERT INTO `fruit_app_routepermission` VALUES (67, 'admin', '/userInfo/', '测试权限URL', '2022-05-05 22:23:57.834758');
INSERT INTO `fruit_app_routepermission` VALUES (68, 'admin', '/update_user_info/', '测试权限URL', '2022-05-05 22:23:57.844744');
INSERT INTO `fruit_app_routepermission` VALUES (69, 'admin', '/update_password/', '测试权限URL', '2022-05-05 22:23:57.853867');
INSERT INTO `fruit_app_routepermission` VALUES (70, 'admin', '/getfruitList/type', '测试权限URL', '2022-05-05 22:23:57.863851');
INSERT INTO `fruit_app_routepermission` VALUES (71, 'admin', '/getfruitList/type/page', '测试权限URL', '2022-05-05 22:23:57.871659');
INSERT INTO `fruit_app_routepermission` VALUES (72, 'admin', '/getfruitList/', '测试权限URL', '2022-05-05 22:23:57.879641');
INSERT INTO `fruit_app_routepermission` VALUES (73, 'admin', '/getfruitList/page', '测试权限URL', '2022-05-05 22:23:57.889618');
INSERT INTO `fruit_app_routepermission` VALUES (74, 'admin', '/fruitDetails/search', '测试权限URL', '2022-05-05 22:23:57.909562');
INSERT INTO `fruit_app_routepermission` VALUES (75, 'admin', '/fruitDetails/add/', '测试权限URL', '2022-05-05 22:23:57.919568');
INSERT INTO `fruit_app_routepermission` VALUES (76, 'admin', '/my_shopping_cart/', '测试权限URL', '2022-05-05 22:23:57.929505');
INSERT INTO `fruit_app_routepermission` VALUES (77, 'admin', '/my_shopping_cart/page', '测试权限URL', '2022-05-05 22:23:57.939481');
INSERT INTO `fruit_app_routepermission` VALUES (78, 'admin', '/shopping_cart/fruit/update/', '测试权限URL', '2022-05-05 22:23:57.946462');
INSERT INTO `fruit_app_routepermission` VALUES (79, 'admin', '/shopping_cart/fruit/delete', '测试权限URL', '2022-05-05 22:23:57.953440');
INSERT INTO `fruit_app_routepermission` VALUES (80, 'admin', '/settle_accounts/', '测试权限URL', '2022-05-05 22:23:57.962420');
INSERT INTO `fruit_app_routepermission` VALUES (81, 'admin', '/confirm/order/', '测试权限URL', '2022-05-05 22:23:57.969398');
INSERT INTO `fruit_app_routepermission` VALUES (82, 'admin', '/pay/', '测试权限URL', '2022-05-05 22:23:57.976382');
INSERT INTO `fruit_app_routepermission` VALUES (83, 'admin', '/management/', '测试权限URL', '2022-05-05 22:23:57.983362');
INSERT INTO `fruit_app_routepermission` VALUES (84, 'admin', '/management/user', '测试权限URL', '2022-05-05 22:23:57.993334');
INSERT INTO `fruit_app_routepermission` VALUES (85, 'admin', '/searchUser/', '测试权限URL', '2022-05-05 22:23:58.002313');
INSERT INTO `fruit_app_routepermission` VALUES (86, 'admin', '/management/user/page', '测试权限URL', '2022-05-05 22:23:58.009291');
INSERT INTO `fruit_app_routepermission` VALUES (87, 'admin', '/managementUser/disable', '测试权限URL', '2022-05-05 22:23:58.016272');
INSERT INTO `fruit_app_routepermission` VALUES (88, 'admin', '/managementUser/enable', '测试权限URL', '2022-05-05 22:23:58.025250');
INSERT INTO `fruit_app_routepermission` VALUES (89, 'admin', '/managementUser/delete', '测试权限URL', '2022-05-05 22:23:58.042206');
INSERT INTO `fruit_app_routepermission` VALUES (90, 'admin', '/managementUser/update/', '测试权限URL', '2022-05-05 22:23:58.054174');
INSERT INTO `fruit_app_routepermission` VALUES (91, 'admin', '/managementUser/add/', '测试权限URL', '2022-05-05 22:23:58.064147');
INSERT INTO `fruit_app_routepermission` VALUES (92, 'admin', '/managementUser/import/', '测试权限URL', '2022-05-05 22:23:58.075120');
INSERT INTO `fruit_app_routepermission` VALUES (93, 'admin', '/managementUser/download/', '测试权限URL', '2022-05-05 22:23:58.087135');
INSERT INTO `fruit_app_routepermission` VALUES (94, 'admin', '/management/permission/', '测试权限URL', '2022-05-05 22:23:58.100052');
INSERT INTO `fruit_app_routepermission` VALUES (95, 'admin', '/management/permission/page', '测试权限URL', '2022-05-05 22:23:58.113064');
INSERT INTO `fruit_app_routepermission` VALUES (96, 'admin', '/management/permission/searchPermission/', '测试权限URL', '2022-05-05 22:23:58.124035');
INSERT INTO `fruit_app_routepermission` VALUES (97, 'admin', '/management/permission/searchPermission/page', '测试权限URL', '2022-05-05 22:23:58.134961');
INSERT INTO `fruit_app_routepermission` VALUES (98, 'admin', '/management/permission/searchPermission/type', '测试权限URL', '2022-05-05 22:23:58.146924');
INSERT INTO `fruit_app_routepermission` VALUES (99, 'admin', '/management/permission/searchPermission/type/page', '测试权限URL', '2022-05-05 22:23:58.154902');
INSERT INTO `fruit_app_routepermission` VALUES (100, 'admin', '/management/permission/add/', '测试权限URL', '2022-05-05 22:23:58.165882');
INSERT INTO `fruit_app_routepermission` VALUES (101, 'admin', '/management/permission/import/', '测试权限URL', '2022-05-05 22:23:58.176015');
INSERT INTO `fruit_app_routepermission` VALUES (102, 'admin', '/management/permission/download/', '测试权限URL', '2022-05-05 22:23:58.194945');
INSERT INTO `fruit_app_routepermission` VALUES (103, 'admin', '/management/permission/update/', '测试权限URL', '2022-05-05 22:23:58.209754');
INSERT INTO `fruit_app_routepermission` VALUES (104, 'admin', '/management/permission/delete', '测试权限URL', '2022-05-05 22:23:58.226735');
INSERT INTO `fruit_app_routepermission` VALUES (105, 'admin', '/management/permission/refresh/', '测试权限URL', '2022-05-05 22:23:58.253640');
INSERT INTO `fruit_app_routepermission` VALUES (106, 'admin', '/management/order/', '测试权限URL', '2022-05-05 22:23:58.270596');
INSERT INTO `fruit_app_routepermission` VALUES (107, 'admin', '/management/order/page', '测试权限URL', '2022-05-05 22:23:58.279610');
INSERT INTO `fruit_app_routepermission` VALUES (108, 'admin', '/management/order/search/', '测试权限URL', '2022-05-05 22:23:58.289542');
INSERT INTO `fruit_app_routepermission` VALUES (109, 'admin', '/management/order/search/page', '测试权限URL', '2022-05-05 22:23:58.299556');
INSERT INTO `fruit_app_routepermission` VALUES (110, 'admin', '/management/order/add/', '测试权限URL', '2022-05-05 22:23:58.310525');
INSERT INTO `fruit_app_routepermission` VALUES (111, 'admin', '/management/order/update/', '测试权限URL', '2022-05-05 22:23:58.319463');
INSERT INTO `fruit_app_routepermission` VALUES (112, 'admin', '/management/order/delete', '测试权限URL', '2022-05-05 22:23:58.326482');
INSERT INTO `fruit_app_routepermission` VALUES (113, 'admin', '/management/order/logical_deletion', '测试权限URL', '2022-05-05 22:23:58.337413');
INSERT INTO `fruit_app_routepermission` VALUES (114, 'admin', '/management/order/import/', '测试权限URL', '2022-05-05 22:23:58.347425');
INSERT INTO `fruit_app_routepermission` VALUES (115, 'admin', '/management/order/download/', '测试权限URL', '2022-05-05 22:23:58.357397');
INSERT INTO `fruit_app_routepermission` VALUES (116, 'admin', '/management/order/send_order_goods', '测试权限URL', '2022-05-05 22:23:58.364380');
INSERT INTO `fruit_app_routepermission` VALUES (117, 'admin', '/management/goods/', '测试权限URL', '2022-05-05 22:23:58.371322');
INSERT INTO `fruit_app_routepermission` VALUES (118, 'admin', '/management/goods/page', '测试权限URL', '2022-05-05 22:23:58.381295');
INSERT INTO `fruit_app_routepermission` VALUES (119, 'admin', '/management/goods/add/', '测试权限URL', '2022-05-05 22:23:58.388314');
INSERT INTO `fruit_app_routepermission` VALUES (120, 'admin', '/management/goods/update/', '测试权限URL', '2022-05-05 22:23:58.397255');
INSERT INTO `fruit_app_routepermission` VALUES (121, 'admin', '/management/goods/delete', '测试权限URL', '2022-05-05 22:23:58.405231');
INSERT INTO `fruit_app_routepermission` VALUES (122, 'admin', '/management/goods/search/', '测试权限URL', '2022-05-05 22:23:58.414247');
INSERT INTO `fruit_app_routepermission` VALUES (123, 'admin', '/management/goods/search/page', '测试权限URL', '2022-05-05 22:23:58.422186');
INSERT INTO `fruit_app_routepermission` VALUES (124, 'admin', '/management/goods/search/type', '测试权限URL', '2022-05-05 22:23:58.429169');
INSERT INTO `fruit_app_routepermission` VALUES (125, 'admin', '/management/goods/search/type/page', '测试权限URL', '2022-05-05 22:23:58.437201');
INSERT INTO `fruit_app_routepermission` VALUES (126, 'admin', '/management/role/', '测试权限URL', '2022-05-05 22:23:58.445145');
INSERT INTO `fruit_app_routepermission` VALUES (127, 'admin', '/management/role/page', '测试权限URL', '2022-05-05 22:23:58.454106');
INSERT INTO `fruit_app_routepermission` VALUES (128, 'admin', '/management/role/search/', '测试权限URL', '2022-05-05 22:23:58.461086');
INSERT INTO `fruit_app_routepermission` VALUES (129, 'admin', '/management/role/search/page', '测试权限URL', '2022-05-05 22:23:58.471057');
INSERT INTO `fruit_app_routepermission` VALUES (130, 'admin', '/management/role/add/', '测试权限URL', '2022-05-05 22:23:58.479052');
INSERT INTO `fruit_app_routepermission` VALUES (131, 'admin', '/management/role/update/', '测试权限URL', '2022-05-05 22:23:58.486016');
INSERT INTO `fruit_app_routepermission` VALUES (132, 'admin', '/management/role/delete', '测试权限URL', '2022-05-05 22:23:58.495992');
INSERT INTO `fruit_app_routepermission` VALUES (133, 'admin', '/management/logistics/', '测试权限URL', '2022-05-05 22:23:58.506022');
INSERT INTO `fruit_app_routepermission` VALUES (134, 'admin', '/management/logistics/page', '测试权限URL', '2022-05-05 22:23:58.515936');
INSERT INTO `fruit_app_routepermission` VALUES (135, 'admin', '/management/logistics/add/', '测试权限URL', '2022-05-05 22:23:58.523918');
INSERT INTO `fruit_app_routepermission` VALUES (136, 'admin', '/management/logistics/update/', '测试权限URL', '2022-05-05 22:23:58.534886');
INSERT INTO `fruit_app_routepermission` VALUES (137, 'admin', '/management/logistics/delete', '测试权限URL', '2022-05-05 22:23:58.545861');
INSERT INTO `fruit_app_routepermission` VALUES (138, 'admin', '/management/logistics/import/', '测试权限URL', '2022-05-05 22:23:58.555850');
INSERT INTO `fruit_app_routepermission` VALUES (139, 'admin', '/management/logistics/download/', '测试权限URL', '2022-05-05 22:23:58.566800');
INSERT INTO `fruit_app_routepermission` VALUES (140, 'admin', '/management/logistics/search/', '测试权限URL', '2022-05-05 22:23:58.577805');
INSERT INTO `fruit_app_routepermission` VALUES (141, 'admin', '/management/logistics/search/page', '测试权限URL', '2022-05-05 22:23:58.587763');
INSERT INTO `fruit_app_routepermission` VALUES (142, 'admin', '/management/logistics/create/logistics_sheet', '测试权限URL', '2022-05-05 22:23:58.597759');
INSERT INTO `fruit_app_routepermission` VALUES (143, 'customer', '/admin/', '测试权限URL', '2022-05-05 22:36:49.098207');
INSERT INTO `fruit_app_routepermission` VALUES (144, 'customer', '/login/', '测试权限URL', '2022-05-05 22:36:49.104194');
INSERT INTO `fruit_app_routepermission` VALUES (145, 'customer', '/register/', '测试权限URL', '2022-05-05 22:36:49.109178');
INSERT INTO `fruit_app_routepermission` VALUES (146, 'customer', '/logout/', '测试权限URL', '2022-05-05 22:36:50.584406');
INSERT INTO `fruit_app_routepermission` VALUES (147, 'customer', '/index/', '测试权限URL', '2022-05-05 22:36:50.593387');
INSERT INTO `fruit_app_routepermission` VALUES (148, 'customer', '/index_send_message/', '测试权限URL', '2022-05-05 22:36:50.597370');
INSERT INTO `fruit_app_routepermission` VALUES (149, 'customer', '/delete/message', '测试权限URL', '2022-05-05 22:36:50.603356');
INSERT INTO `fruit_app_routepermission` VALUES (150, 'customer', '/morefruits/get', '测试权限URL', '2022-05-05 22:36:50.606341');
INSERT INTO `fruit_app_routepermission` VALUES (151, 'customer', '/userInfo/', '测试权限URL', '2022-05-05 22:36:50.608336');
INSERT INTO `fruit_app_routepermission` VALUES (152, 'customer', '/update_user_info/', '测试权限URL', '2022-05-05 22:36:50.611328');
INSERT INTO `fruit_app_routepermission` VALUES (153, 'customer', '/update_password/', '测试权限URL', '2022-05-05 22:36:50.614323');
INSERT INTO `fruit_app_routepermission` VALUES (154, 'customer', '/getfruitList/type', '测试权限URL', '2022-05-05 22:36:50.618309');
INSERT INTO `fruit_app_routepermission` VALUES (155, 'customer', '/getfruitList/type/page', '测试权限URL', '2022-05-05 22:36:50.621304');
INSERT INTO `fruit_app_routepermission` VALUES (156, 'customer', '/getfruitList/', '测试权限URL', '2022-05-05 22:36:50.623296');
INSERT INTO `fruit_app_routepermission` VALUES (157, 'customer', '/getfruitList/page', '测试权限URL', '2022-05-05 22:36:50.626288');
INSERT INTO `fruit_app_routepermission` VALUES (158, 'customer', '/fruitDetails/search', '测试权限URL', '2022-05-05 22:36:50.629283');
INSERT INTO `fruit_app_routepermission` VALUES (159, 'customer', '/fruitDetails/add/', '测试权限URL', '2022-05-05 22:36:50.631274');
INSERT INTO `fruit_app_routepermission` VALUES (160, 'customer', '/my_shopping_cart/', '测试权限URL', '2022-05-05 22:36:50.635279');
INSERT INTO `fruit_app_routepermission` VALUES (161, 'customer', '/my_shopping_cart/page', '测试权限URL', '2022-05-05 22:36:50.638259');
INSERT INTO `fruit_app_routepermission` VALUES (162, 'customer', '/shopping_cart/fruit/update/', '测试权限URL', '2022-05-05 22:36:50.641251');
INSERT INTO `fruit_app_routepermission` VALUES (163, 'customer', '/shopping_cart/fruit/delete', '测试权限URL', '2022-05-05 22:36:50.644240');
INSERT INTO `fruit_app_routepermission` VALUES (164, 'customer', '/settle_accounts/', '测试权限URL', '2022-05-05 22:36:50.648233');
INSERT INTO `fruit_app_routepermission` VALUES (165, 'customer', '/confirm/order/', '测试权限URL', '2022-05-05 22:36:50.651221');
INSERT INTO `fruit_app_routepermission` VALUES (166, 'customer', '/pay/', '测试权限URL', '2022-05-05 22:36:50.653219');

SET FOREIGN_KEY_CHECKS = 1;
