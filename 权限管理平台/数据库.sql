#erp权限管理表
create table user_right_manage(
	user_erp varchar(30) primary key,
	right_level int default 0,
	last_update_date bigint
);


#日志表
create table log(
	log_date date not null,
	log_type varchar(10) not null,
	admin_erp varchar(30) default "none",
	user_erp varchar(30) not null,
	user_equipment varchar(10) not null,
	content varchar(1000) not null,
	params varchar(1000)
);




