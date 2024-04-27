Drop table if exists iot.cay;
Drop table if exists iot.users_roles;
Drop table if exists iot.users;
Drop table if exists iot.roles;

Drop table if exists iot.tasks;
CREATE TABLE iot.cay (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ten_cay VARCHAR(255) NOT NULL,
    min_ideal_temp FLOAT,
    max_ideal_temp FLOAT,
    min_ideal_humidity INT,
    max_ideal_humidity INT,
    min_ideal_sunlight INT,
    max_ideal_sunlight INT,
    min_ideal_soil_moisture INT,
    max_ideal_soil_moisture INT
);
INSERT INTO iot.cay 
VALUES(1,"CaChua","24","26","50","55","60","65","70","74");

create table iot.users (
	id INT AUTO_INCREMENT PRIMARY KEY,
    username varchar(255) NOT NULL,
    `password` varchar(255) NOT NULL,
    email varchar(255) NOT NULL,
    `name` varchar(255) NOT NULL
);
create table iot.roles(
	id int auto_increment primary key,
    `name` varchar(255) NOT NULL
);

create table iot.users_roles(
	id int auto_increment primary key,
    id_user int NOT NULL,
    id_role int NOT NULL,
    foreign key (id_user) REFERENCES users(id),
    foreign key (id_role) references roles(id)
);

create table iot.tasks(
	id int auto_increment primary key,
    id_user int NOt null,
    time_receive datetime,
    title varchar(255),
    description longtext,
    deadline datetime not null,
    status varchar(255),
    reasonCancel varchar(255)
);
insert into iot.users
VALUES(1,"huyabc","123456","nguyenhuuhuyptit@gmail.com", "Nguyễn Hữu Huy"),
(2, "nguyenvana","123456","nguyenvana@gmail.com","Nguyễn Văn A"),
(3, "nguyenvanb","123456","nguyenvanb@gmail.com","Nguyễn Văn B");

insert into iot.roles
VALUES(1,"admin"),(2,"user");
-- -- insert into iot.tasks(id_user,time_receive,title,description,deadline) values(1,"2024-03-26 12:30:00","test 1","test1","2024-03-27 12:30:00");
insert into iot.users_roles 
values(1,1,1),
(2,2,2),
(3,3,2);