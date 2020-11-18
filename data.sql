INSERT INTO Users (
user_id,
user_name,
diet_default,
car_travel_default,
train_travel_default,
bus_travel_default,
food_disposal_default,
plastic_disposal_default,
paper_disposal_default,
glass_disposal_default,
tin_disposal_default,
mobile_screentime_default,
computer_screetime_default,
tv_screentime_default
)
VALUES (
"abc",
"Steve",
"meat",
2.0,
3.0,
0.0,
TRUE,
TRUE,
TRUE,
TRUE,
FALSE,
4.0,
6.0,
2.0
);

INSERT INTO Organisations (
user_id,
organisation_name
)
VALUES (
"abc",
"AstraZeneca"
);

INSERT INTO Organisations (
user_id,
organisation_name
)
VALUES (
"abc",
"Microsoft"
);

INSERT INTO Reports (
date,
user_id,
use_defaults,
diet,
car_travel,
train_travel,
bus_travel,
food_disposal,
plastic_disposal,
paper_disposal,
glass_disposal,
tin_disposal,
mobile_screentime,
computer_screentime,
tv_screentime
)
VALUES (
"2020-11-18",
"abc",
TRUE,
"meat",
2.0,
3.0,
0.0,
TRUE,
TRUE,
TRUE,
TRUE,
FALSE,
4.0,
6.0,
2.0
);

INSERT INTO Reports (
date,
user_id,
use_defaults,
diet,
car_travel,
train_travel,
bus_travel,
food_disposal,
plastic_disposal,
paper_disposal,
glass_disposal,
tins_disposal,
mobile_screentime,
computer_screentime,
tv_screentime
)
VALUES (
"2020-11-17",
"abc",
FALSE,
"vegan",
0.0,
6.0,
0.0,
FALSE,
TRUE,
TRUE,
TRUE,
FALSE,
6.0,
6.0,
0.0
);