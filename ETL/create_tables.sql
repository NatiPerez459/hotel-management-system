CREATE TABLE IF NOT EXISTS Chains (
    chid serial PRIMARY KEY,
    cname varchar(50),
    springmkup float,
    summermkup float,
    fallmkup float,
    wintermkup float
);

CREATE TABLE IF NOT EXISTS Hotel (
    hid serial PRIMARY KEY,
    chid integer references Chains(chid) ON DELETE CASCADE,
    hname varchar(50),
    hcity varchar(25)
);

CREATE TABLE IF NOT EXISTS Employee (
    eid serial PRIMARY KEY,
    hid integer references Hotel(hid) ON DELETE CASCADE,
    fname varchar(50),
    lname varchar(50),
    age integer,
    position varchar(25),
    salary float
);

CREATE TABLE IF NOT EXISTS Login (
    lid serial PRIMARY KEY,
    eid integer references Employee(eid) ON DELETE CASCADE,
    username varchar(50),
    password varchar(25)
);

CREATE TABLE IF NOT EXISTS RoomDescription (
    rdid serial PRIMARY KEY,
    rname varchar(25),
    rtype varchar(25),
    capacity integer,
    ishandicap boolean
);

CREATE TABLE IF NOT EXISTS Room (
    rid serial PRIMARY KEY,
    hid integer references Hotel(hid) ON DELETE CASCADE,
    rdid integer references RoomDescription(rdid) ON DELETE CASCADE,
    rprice float
);

CREATE TABLE IF NOT EXISTS RoomUnavailable (
    ruid serial PRIMARY KEY,
    rid integer references Room(rid) ON DELETE CASCADE,
    startdate date,
    enddate date
);

CREATE TABLE IF NOT EXISTS Client (
    clid serial PRIMARY KEY,
    fname varchar(50),
    lname varchar(50),
    age integer,
    memberyear integer
);

CREATE TABLE IF NOT EXISTS Reserve (
    reid serial PRIMARY KEY,
    ruid integer references RoomUnavailable(ruid) ON DELETE CASCADE,
    clid integer references Client(clid) ON DELETE CASCADE,
    total_cost float,
    payment varchar(25),
    guests integer
);