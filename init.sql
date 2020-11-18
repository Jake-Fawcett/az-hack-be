USE azhack;

DROP TABLE IF EXISTS Organisations;
DROP TABLE IF EXISTS Reports;
DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
    user_id VARCHAR(250) PRIMARY KEY NOT NULL,
    user_name VARCHAR(250) NOT NULL,
    diet_default VARCHAR(250) NOT NULL,
    car_travel_default DOUBLE,
    train_travel_default DOUBLE,
    bus_travel_default DOUBLE,
    food_disposal_default BOOLEAN,
    plastic_disposal_default BOOLEAN,
    paper_disposal_default BOOLEAN,
    glass_disposal_default BOOLEAN,
    tin_disposal_default BOOLEAN,
    mobile_screentime_default DOUBLE,
    computer_screetime_default DOUBLE,
    tv_screentime_default DOUBLE
);

CREATE TABLE Organisations (
    user_id VARCHAR(250) NOT NULL,
    organisation_name VARCHAR(250) NOT NULL,
    PRIMARY KEY (user_id, organisation_name)
);

CREATE TABLE Reports (
    date DATE NOT NULL,
    user_id VARCHAR(250),
    use_defaults BOOLEAN NOT NULL,
    diet VARCHAR(250),
    car_travel DOUBLE,
    train_travel DOUBLE,
    bus_travel DOUBLE,
    food_disposal BOOLEAN,
    plastic_disposal BOOLEAN,
    paper_disposal BOOLEAN,
    glass_disposal BOOLEAN,
    tin_disposal BOOLEAN,
    mobile_screentime DOUBLE,
    computer_screentime DOUBLE,
    tv_screentime DOUBLE,
    PRIMARY KEY(user_id, date)
);

