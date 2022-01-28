s = "508253/male/white/21/cs/2022/2022-1-26 11:00:00/CS 495/Marc Rubin"
data = s.split('/')
values = ""
for i in range(len(data)-1):
    values += data[i] + ', '
values += data[-1]
sql = "INSERT INTO attendance (stuID, sex, race, age, major, class, access, event, planner)" \
      " VALUES (" + values + ");"

print(sql)

#create table attendance (
# id int primary key autoincrement,
# stuID varchar(6) not null,
# sex varchar(5) not null,
# race varchar(10) not null,
# age varchar(3) not null,
# major varchar (4) not null,
# gradYear varchar(4) not null,
# access datetime not null,
# event varchar(45) not null,
# planner varchar(35) not null
# );
