DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS profile;
DROP TABLE IF EXISTS housing; 
DROP TABLE IF EXISTS matchpairing;
DROP TABLE IF EXISTS housepairing;


CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  email TEXT UNIQUE NOT NULL, 
  phone TEXT UNIQUE NOT NULL, 
  password TEXT NOT NULL,
  verified INTEGER DEFAULT 0
);

CREATE TABLE profile (
  user_id INTEGER NOT NULL,

  first_name TEXT NOT NULL,
  middle_name TEXT, 
  last_name TEXT NOT NULL,

  photo BLOB NOT NULL, 

  dob TEXT NOT NULL,

  occupation TEXT NOT NULL,
  description TEXT,

  gender TEXT NOT NULL,
  genderPref TEXT NOT NULL,

  ageMin INTEGER NOT NULL,
  ageMax INTEGER NOT NULL,

  priceMin INTEGER NOT NULL, 
  priceMax INTEGER NOT NULL,

  pets TEXT NOT NULL,

  city TEXT NOT NULL,
  state TEXT NOT NULL,
  zipcode INTEGER NOT NULL,

  looking TEXT NOT NULL, 

  FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE housing (
  housing_id INTEGER PRIMARY KEY AUTOINCREMENT, 
  poster_id INTEGER NOT NULL, 

  photo BLOB NOT NULL, 
  description TEXT,

  housing_number INTEGER NOT NULL, 
  apt_number TEXT NOT NULL, 
  street TEXT NOT NULL, 
  city TEXT NOT NULL,
  state TEXT NOT NULL,
  zipcode INTEGER NOT NULL,

  rent INTEGER NOT NULL,

  pets TEXT NOT NULL,
  genderPref TEXT NOT NULL,

  ageMin INTEGER NOT NULL,
  ageMax INTEGER NOT NULL,


  FOREIGN KEY (poster_id) REFERENCES user (id)


);


CREATE TABLE matchpairing (
  user_id INTEGER NOT NULL, 
  match_id INTEGER NOT NULL, 

  FOREIGN KEY (user_id) REFERENCES user (id),
  FOREIGN KEY (match_id) REFERENCES user (id)
);



CREATE TABLE housepairing (
  user_id INTEGER NOT NULL, 
  house_id INTEGER NOT NULL, 

  FOREIGN KEY (user_id) REFERENCES user (id),
  FOREIGN KEY (house_id) REFERENCES user (id)
);
