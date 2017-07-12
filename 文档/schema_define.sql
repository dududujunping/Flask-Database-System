create table ClassInfo(
    classno  varchar(5)  not null,
    major    varchar(20) default null,
    primary key (classno)
);

create table StudentInfo(
    sno      varchar(5)  not null,
    passwd   varchar(20) not null,
    sname    varchar(10) default null,
    sex      varchar(2)  default null,
    age      varchar(3)  default null,
    classno  varchar(5),
    primary key (sno),
    foreign key (classno) references ClassInfo
);

create table TeacherInfo(
    tno      varchar(5)  not null,
    passwd   varchar(20) not null,
    tname    varchar(10) default null,
    sex      varchar(2)  default null,
    age      varchar(3)  default null,
    primary key (tno)
);

create table AdminInfo(
    ano      varchar(5)  not null,
    passwd   varchar(20) not null,
    primary key (ano)
);

create table CourseInfo(
    cno      varchar(5)  not null,
    cname    varchar(30) default null,
    tno      varchar(5),
    primary key (cno),
    foreign key (tno) references TeacherInfo
);

create table StudentCourse(
    cno      varchar(5)  not null,
    sno      varchar(5)  not null,
    grade    varchar(3),
    primary key (cno, sno),
    foreign key (cno) references CourseInfo on delete cascade,
    foreign key (sno) references StudentInfo on delete cascade
);



