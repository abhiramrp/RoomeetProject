DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS profile;
DROP TABLE IF EXISTS housing;
DROP TABLE IF EXISTS housingAddress;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  email TEXT UNIQUE NOT NULL, 
  phone TEXT UNIQUE NOT NULL, 
  password TEXT NOT NULL,
  verified INTEGER DEFAULT 0
);

CREATE TABLE housingAddress ( 
  address_id INTEGER PRIMARY KEY AUTOINCREMENT,
  
  aptNum TEXT, 
  houseNumber INTEGER NOT NULL, 
  street TEXT NOT NULL, 
  location NUMBER NOT NULL, 
  city TEXT NOT NULL,
  state TEXT NOT NULL,
  zipcode INTEGER NOT NULL

);

CREATE TABLE profile (
  user_id INTEGER NOT NULL,

  first_name TEXT NOT NULL,
  middle_name TEXT, 
  last_name TEXT NOT NULL,

  occupation TEXT NOT NULL,
  description TEXT,

  gender TEXT NOT NULL,
  genderPref TEXT NOT NULL,

  ageMin INTEGER NOT NULL,
  ageMax INTEGER NOT NULL,

  priceMin INTEGER NOT NULL, 
  priceMax INTEGER NOT NULL,

  city TEXT NOT NULL,
  state TEXT NOT NULL,
  zipcode INTEGER NOT NULL,

  FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE housing (
  housing_id INTEGER PRIMARY KEY AUTOINCREMENT,
  housing_address INTEGER NOT NULL,
  poster_id INTEGER NOT NULL, 
  rent INTEGER NOT NULL,
  FOREIGN KEY (poster_id) REFERENCES user (id),
  FOREIGN KEY (housing_address) REFERENCES housingAddress (housing_address)
);


