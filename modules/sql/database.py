import sqlite3
import hashlib
import random

# Step 1: Connect to the database or create it if it doesn't exist
conn = sqlite3.connect('example.db')

# Step 2: Create a cursor object
cursor = conn.cursor()

# Function to generate a unique usr
def generate_unique_usr(databasePath):
    conn = sqlite3.connect(databasePath)
    cursor = conn.cursor()
    while True:
        # Generate a random number or use a unique identifier
        new_usr = random.randint(1, 9000)  # Adjust the range as needed

        # Check if the usr exists in the users table
        cursor.execute('SELECT * FROM users WHERE usr = ?', (new_usr,))
        result = cursor.fetchone()

        # If the usr does not exist, return it
        if not result:
            return new_usr

# Step 3: Create tables
cursor.execute('DROP TABLE IF EXISTS includes')
cursor.execute('DROP TABLE IF EXISTS lists')
cursor.execute('DROP TABLE IF EXISTS retweets')
cursor.execute('DROP TABLE IF EXISTS mentions')
cursor.execute('DROP TABLE IF EXISTS hashtags')
cursor.execute('DROP TABLE IF EXISTS tweets')
cursor.execute('DROP TABLE IF EXISTS follows')
cursor.execute('DROP TABLE IF EXISTS users')

cursor.execute('''
CREATE TABLE users (
  usr         INTEGER,
  pwd	      TEXT,
  name        TEXT,
  email       TEXT,
  city        TEXT,
  timezone    REAL,
  PRIMARY KEY (usr)
)''')

cursor.execute('''
CREATE TABLE follows (
  flwer       INTEGER,
  flwee       INTEGER,
  start_date  DATE,
  PRIMARY KEY (flwer,flwee),
  FOREIGN KEY (flwer) REFERENCES users(usr),
  FOREIGN KEY (flwee) REFERENCES users(usr)
)''')

cursor.execute('''
CREATE TABLE tweets (
  tid	      INTEGER,
  writer      INTEGER,
  tdate       DATE,
  text        TEXT,
  replyto     INTEGER,
  PRIMARY KEY (tid),
  FOREIGN KEY (writer) REFERENCES users(usr),
  FOREIGN KEY (replyto) REFERENCES tweets(tid)
)''')

cursor.execute('''
CREATE TABLE hashtags (
  term        TEXT,
  PRIMARY KEY (term)
)''')

cursor.execute('''
CREATE TABLE mentions (
  tid         INTEGER,
  term        TEXT,
  PRIMARY KEY (tid,term),
  FOREIGN KEY (tid) REFERENCES tweets(tid),
  FOREIGN KEY (term) REFERENCES hashtags(term)
)''')

cursor.execute('''
CREATE TABLE retweets (
  usr         INTEGER,
  tid         INTEGER,
  rdate       DATE,
  PRIMARY KEY (usr,tid),
  FOREIGN KEY (usr) REFERENCES users(usr),
  FOREIGN KEY (tid) REFERENCES tweets(tid)
)''')

cursor.execute('''
CREATE TABLE lists (
  lname        TEXT,
  owner        INTEGER,
  PRIMARY KEY (lname),
  FOREIGN KEY (owner) REFERENCES users(usr)
)''')

cursor.execute('''
CREATE TABLE includes (
  lname       TEXT,
  member      INTEGER,
  PRIMARY KEY (lname,member),
  FOREIGN KEY (lname) REFERENCES lists(lname),
  FOREIGN KEY (member) REFERENCES users(usr)
)''')

# Step 4: Insert data into tables

# Insert data into the 'users' table
users_data = [
    (generate_unique_usr('example.db'), 'pwd1', 'John Doe', 'john@example.com', 'New York', -5.0),
    (generate_unique_usr('example.db'), 'pwd2', 'Jane Smith', 'jane@example.com', 'Los Angeles', -8.0),
    (generate_unique_usr('example.db'), 'pwd3', 'Michael Johnson', 'michael@example.com', 'Chicago', -6.0),
    (generate_unique_usr('example.db'), 'pwd4', 'Emily Williams', 'emily@example.com', 'San Francisco', -8.0),
    (generate_unique_usr('example.db'), 'pwd5', 'Daniel Brown', 'daniel@example.com', 'Seattle', -8.0),
    (generate_unique_usr('example.db'), 'pwd6', 'Olivia Davis', 'olivia@example.com', 'Miami', -5.0),
    (generate_unique_usr('example.db'), 'pwd7', 'William Wilson', 'william@example.com', 'Boston', -5.0),
    (generate_unique_usr('example.db'), 'pwd8', 'Sophia Moore', 'sophia@example.com', 'Dallas', -6.0),
    (generate_unique_usr('example.db'), 'pwd9', 'Alexander Taylor', 'alexander@example.com', 'Houston', -6.0),
    (generate_unique_usr('example.db'), 'pwd10', 'Isabella Anderson', 'isabella@example.com', 'Atlanta', -5.0),
    (generate_unique_usr('example.db'), 'pwd11', 'Emma Lee', 'emma@example.com', 'San Diego', -8.0),
    (generate_unique_usr('example.db'), 'pwd12', 'James Wilson', 'james@example.com', 'Denver', -7.0),
    (generate_unique_usr('example.db'), 'pwd13', 'Grace Martin', 'grace@example.com', 'Phoenix', -7.0),
    (generate_unique_usr('example.db'), 'pwd14', 'Benjamin Garcia', 'benjamin@example.com', 'Philadelphia', -5.0),
    (generate_unique_usr('example.db'), 'pwd15', 'Avery Martinez', 'avery@example.com', 'San Antonio', -6.0),
    (generate_unique_usr('example.db'), 'pwd16', 'Victoria Robinson', 'victoria@example.com', 'San Jose', -8.0),
    (generate_unique_usr('example.db'), 'pwd17', 'Oliver Clark', 'oliver@example.com', 'Austin', -6.0),
    (generate_unique_usr('example.db'), 'pwd18', 'Evelyn Rodriguez', 'evelyn@example.com', 'Jacksonville', -5.0),
    (generate_unique_usr('example.db'), 'pwd19', 'Mia Lewis', 'mia@example.com', 'Fort Worth', -6.0),
    (generate_unique_usr('example.db'), 'pwd20', 'Matthew Hall', 'matthew@example.com', 'Columbus', -5.0),
    (generate_unique_usr('example.db'), 'pwd21', 'Luna Perez', 'luna@example.com', 'Charlotte', -5.0),
    (generate_unique_usr('example.db'), 'pwd22', 'Sofia Young', 'sofia@example.com', 'San Francisco', -8.0),
    (generate_unique_usr('example.db'), 'pwd23', 'Lucas Hernandez', 'lucas@example.com', 'Indianapolis', -5.0),
    (generate_unique_usr('example.db'), 'pwd24', 'Liam King', 'liam@example.com', 'Seattle', -8.0),
    (generate_unique_usr('example.db'), 'pwd25', 'Aria Nelson', 'aria@example.com', 'Denver', -7.0),
    (generate_unique_usr('example.db'), 'pwd26', 'Harper Carter', 'harper@example.com', 'Washington', -5.0),
    (generate_unique_usr('example.db'), 'pwd27', 'Ethan Ward', 'ethan@example.com', 'Boston', -5.0),
    (generate_unique_usr('example.db'), 'pwd28', 'Aiden Foster', 'aiden@example.com', 'Nashville', -6.0),
    (generate_unique_usr('example.db'), 'pwd29', 'Amelia Simmons', 'amelia@example.com', 'Baltimore', -5.0),
    (generate_unique_usr('example.db'), 'pwd30', 'Madison Rogers', 'madison@example.com', 'Louisville', -5.0),
    (generate_unique_usr('example.db'), 'pwd31', 'Daniel Stewart', 'daniel@example.com', 'Portland', -8.0),
    (generate_unique_usr('example.db'), 'pwd32', 'Aubrey Cooper', 'aubrey@example.com', 'Oklahoma City', -6.0),
    (generate_unique_usr('example.db'), 'pwd33', 'Logan Reed', 'logan@example.com', 'Las Vegas', -8.0),
    (generate_unique_usr('example.db'), 'pwd34', 'Sebastian Hayes', 'sebastian@example.com', 'Milwaukee', -6.0),
    (generate_unique_usr('example.db'), 'pwd35', 'Jack Wright', 'jack@example.com', 'Albuquerque', -7.0),
    (generate_unique_usr('example.db'), 'pwd36', 'Penelope Perry', 'penelope@example.com', 'Tucson', -7.0),
    (generate_unique_usr('example.db'), 'pwd37', 'Gabriel Long', 'gabriel@example.com', 'Fresno', -8.0),
    (generate_unique_usr('example.db'), 'pwd38', 'Bella Hughes', 'bella@example.com', 'Sacramento', -8.0),
    (generate_unique_usr('example.db'), 'pwd39', 'Madelyn Flores', 'madelyn@example.com', 'Long Beach', -6.0),
    (generate_unique_usr('example.db'), 'pwd40', 'Grayson Washington', 'grayson@example.com', 'Kansas City', -5.0),
    (generate_unique_usr('example.db'), 'pwd41', 'Liam Foster', 'liam@example.com', 'Philadelphia', -5.0),
    (generate_unique_usr('example.db'), 'pwd42', 'Evelyn Reed', 'evelyn@example.com', 'Phoenix', -7.0),
    (generate_unique_usr('example.db'), 'pwd43', 'Mia Hayes', 'mia@example.com', 'San Antonio', -6.0),
    (generate_unique_usr('example.db'), 'pwd44', 'Noah Simmons', 'noah@example.com', 'San Jose', -8.0),
    (generate_unique_usr('example.db'), 'pwd45', 'Emma Perry', 'emma@example.com', 'Austin', -6.0),
    (generate_unique_usr('example.db'), 'pwd46', 'Oliver Hughes', 'oliver@example.com', 'Jacksonville', -5.0),
    (generate_unique_usr('example.db'), 'pwd47', 'Sophia Martin', 'sophia@example.com', 'Fort Worth', -6.0),
    (generate_unique_usr('example.db'), 'pwd48', 'William Young', 'william@example.com', 'Columbus', -5.0),
    (generate_unique_usr('example.db'), 'pwd49', 'Elijah Hernandez', 'elijah@example.com', 'Charlotte', -5.0),
    (generate_unique_usr('example.db'), 'pwd50', 'Lucas King', 'lucas@example.com', 'San Francisco', -8.0),
    (generate_unique_usr('example.db'), 'pwd51', 'Aiden Nelson', 'aiden@example.com', 'Indianapolis', -5.0),
    (generate_unique_usr('example.db'), 'pwd52', 'Amelia Carter', 'amelia@example.com', 'Seattle', -8.0),
    (generate_unique_usr('example.db'), 'pwd53', 'Madison Ward', 'madison@example.com', 'Denver', -7.0),
    (generate_unique_usr('example.db'), 'pwd54', 'Daniel Foster', 'daniel@example.com', 'Washington', -5.0),
    (generate_unique_usr('example.db'), 'pwd55', 'Logan Simmons', 'logan@example.com', 'Boston', -5.0),
    (generate_unique_usr('example.db'), 'pwd56', 'Sebastian Cooper', 'sebastian@example.com', 'Nashville', -6.0),
    (generate_unique_usr('example.db'), 'pwd57', 'Jack Reed', 'jack@example.com', 'Baltimore', -5.0),
    (generate_unique_usr('example.db'), 'pwd58', 'Penelope Rogers', 'penelope@example.com', 'Louisville', -5.0),
    (generate_unique_usr('example.db'), 'pwd59', 'Gabriel Stewart', 'gabriel@example.com', 'Portland', -8.0),
    (generate_unique_usr('example.db'), 'pwd60', 'Bella Cooper', 'bella@example.com', 'Oklahoma City', -6.0),
    (generate_unique_usr('example.db'), 'pwd61', 'Aria Reed', 'aria@example.com', 'Las Vegas', -8.0),
    (generate_unique_usr('example.db'), 'pwd62', 'Daniel Hayes', 'daniel@example.com', 'Milwaukee', -6.0),
    (generate_unique_usr('example.db'), 'pwd63', 'Olivia Wright', 'olivia@example.com', 'Albuquerque', -7.0),
    (generate_unique_usr('example.db'), 'pwd64', 'Logan Perry', 'logan@example.com', 'Tucson', -7.0),
    (generate_unique_usr('example.db'), 'pwd65', 'Sebastian Washington', 'sebastian@example.com', 'Fresno', -8.0),
    (generate_unique_usr('example.db'), 'pwd66', 'Jack Hughes', 'jack@example.com', 'Sacramento', -8.0),
    (generate_unique_usr('example.db'), 'pwd67', 'Penelope Flores', 'penelope@example.com', 'Long Beach', -6.0),
    (generate_unique_usr('example.db'), 'pwd68', 'Gabriel Washington', 'gabriel@example.com', 'Kansas City', -5.0),
    (generate_unique_usr('example.db'), 'pwd69', 'Bella Foster', 'bella@example.com', 'New York', -5.0),
    (generate_unique_usr('example.db'), 'pwd70', 'Madelyn Reed', 'madelyn@example.com', 'Los Angeles', -8.0),
    (generate_unique_usr('example.db'), 'pwd71', 'Grayson Hayes', 'grayson@example.com', 'Chicago', -6.0),
    (generate_unique_usr('example.db'), 'pwd72', 'Liam Wright', 'liam@example.com', 'San Francisco', -8.0),
    (generate_unique_usr('example.db'), 'pwd73', 'Evelyn Perry', 'evelyn@example.com', 'Seattle', -8.0),
    (generate_unique_usr('example.db'), 'pwd74', 'Mia Washington', 'mia@example.com', 'Miami', -5.0),
    (generate_unique_usr('example.db'), 'pwd75', 'Noah Foster', 'noah@example.com', 'Boston', -5.0),
    (generate_unique_usr('example.db'), 'pwd76', 'Aria Simmons', 'aria@example.com', 'Dallas', -6.0),
    (generate_unique_usr('example.db'), 'pwd77', 'Daniel Hughes', 'daniel@example.com', 'Houston', -6.0),
    (generate_unique_usr('example.db'), 'pwd78', 'Olivia Foster', 'olivia@example.com', 'Atlanta', -5.0),
    (generate_unique_usr('example.db'), 'pwd79', 'Logan Perry', 'logan@example.com', 'San Diego', -8.0),
    (generate_unique_usr('example.db'), 'pwd80', 'Sebastian Washington', 'sebastian@example.com', 'Denver', -7.0),
    (generate_unique_usr('example.db'), 'pwd81', 'Jack Hayes', 'jack@example.com', 'Phoenix', -7.0),
    (generate_unique_usr('example.db'), 'pwd82', 'Penelope Wright', 'penelope@example.com', 'Philadelphia', -5.0),
    (generate_unique_usr('example.db'), 'pwd83', 'Gabriel Perry', 'gabriel@example.com', 'San Antonio', -6.0),
    (generate_unique_usr('example.db'), 'pwd84', 'Bella Washington', 'bella@example.com', 'San Jose', -8.0),
    (generate_unique_usr('example.db'), 'pwd85', 'Madelyn Foster', 'madelyn@example.com', 'Austin', -6.0),
    (generate_unique_usr('example.db'), 'pwd86', 'Grayson Simmons', 'grayson@example.com', 'Jacksonville', -5.0),
    (generate_unique_usr('example.db'), 'pwd87', 'Liam Perry', 'liam@example.com', 'Fort Worth', -6.0),
    (generate_unique_usr('example.db'), 'pwd88', 'Evelyn Washington', 'evelyn@example.com', 'Columbus', -5.0)
]

cursor.executemany('INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)', users_data)

# A flwer follows a flwee
# Insert data into the 'follows' table
follows_data = [
    (91, 134, '2023-01-01'),
    (134, 380, '2023-02-15'),
    (380, 469, '2023-03-10'),
    (469, 546, '2023-04-22'),
    (546, 563, '2023-05-05'),
    (563, 669, '2023-06-18'),
    (669, 712, '2023-07-02'),
    (712, 746, '2023-08-14'),
    (746, 776, '2023-09-27'),
    (776, 91, '2023-10-09'),
    (91, 9, '2023-10-15'),
    (9, 26, '2023-10-17'),
    (26, 28, '2023-10-18'),
    (28, 29, '2023-10-20'),
    (29, 48, '2023-10-22'),
    (48, 106, '2023-10-24'),
    (106, 120, '2023-10-26'),
    (120, 125, '2023-10-28'),
    (125, 135, '2023-10-30'),
    (135, 143, '2023-11-01'),
    (143, 152, '2023-11-03'),
    (152, 167, '2023-11-05'),
    (167, 173, '2023-11-07'),
    (173, 207, '2023-11-09'),
    (207, 222, '2023-11-11'),
    (222, 237, '2023-11-13'),
    (237, 240, '2023-11-15'),
    (240, 250, '2023-11-17'),
    (250, 273, '2023-11-19'),
    (273, 354, '2023-11-21'),
    (354, 381, '2023-11-23'),
    (381, 397, '2023-11-25'),
    (397, 417, '2023-11-27'),
    (417, 426, '2023-11-29'),
    (426, 440, '2023-12-01'),
    (440, 476, '2023-12-03'),
    (476, 479, '2023-12-05'),
    (479, 487, '2023-12-07'),
    (487, 513, '2023-12-09'),
    (513, 516, '2023-12-11'),
    (516, 561, '2023-12-13'),
    (561, 576, '2023-12-15'),
    (576, 587, '2023-12-17'),
    (587, 589, '2023-12-19'),
    (589, 605, '2023-12-21'),
    (605, 627, '2023-12-23'),
    (627, 628, '2023-12-25'),
    (628, 629, '2023-12-27'),
    (629, 636, '2023-12-29'),
    (636, 673, '2023-12-31'),
    (673, 687, '2024-01-01'),
    (687, 720, '2024-01-03'),
    (720, 736, '2024-01-05'),
    (736, 738, '2024-01-07'),
    (738, 792, '2024-01-09'),
    (792, 803, '2024-01-11'),
    (803, 839, '2024-01-13'),
    (839, 841, '2024-01-15'),
    (841, 857, '2024-01-17'),
    (857, 858, '2024-01-19'),
    (858, 859, '2024-01-21'),
    (859, 863, '2024-01-23'),
    (863, 877, '2024-01-25'),
    (877, 901, '2024-01-27'),
    (901, 917, '2024-01-29'),
    (917, 956, '2024-01-31'),
    (956, 975, '2024-02-02'),
    (975, 980, '2024-02-04'),
    (980, 984, '2024-02-06'),
    (984, 998, '2024-02-08'),
    (998, 999, '2024-02-10'),
    (999, 1134, '2024-02-12'),
    (1134, 1653, '2024-02-14'),
    (1653, 2041, '2024-02-16'),
    (2041, 2479, '2024-02-18'),
    (2479, 2591, '2024-02-20'),
    (2591, 3733, '2024-02-22'),
    (3733, 3870, '2024-02-24'),
    (3870, 3942, '2024-02-26'),
    (3942, 4021, '2024-02-28'),
    (4021, 4045, '2024-03-01'),
    (4045, 4251, '2024-03-03'),
    (4251, 4321, '2024-03-05'),
    (4321, 4390, '2024-03-07'),
    (4390, 4394, '2024-03-09'),
    (4394, 5431, '2024-03-11'),
    (5431, 5644, '2024-03-13'),
    (5644, 6033, '2024-03-15'),
    (6033, 6555, '2024-03-17'),
    (6555, 6921, '2024-03-19'),
    (6921, 7133, '2024-03-21'),
    (7133, 7963, '2024-03-23'),
    (7963, 8099, '2024-03-25'),
    (8099, 8167, '2024-03-27'),
    (8167, 8286, '2024-03-29'),
    (8286, 8692, '2024-03-31'),
    (8692, 8867, '2024-04-02')
]

cursor.executemany('INSERT INTO follows VALUES (?, ?, ?)', follows_data)

# Insert data into 'tweets' table
tweets_data = [
    (10000, 6, '2023-01-01', 'Sample tweet 1', 134),
    (10001, 9, '2023-01-02', 'Another tweet', 380),
    (10002, 26, '2023-01-03', 'Hello, Twitter!', 469),
    (10003, 28, '2023-01-04', 'Testing the database', 546),
    (10004, 29, '2023-01-05', 'Python is great', 563),
    (10005, 48, '2023-01-06', 'SQLite is easy to use', 669),
    (10006, 106, '2023-01-07', 'My first tweet', 712),
    (10007, 120, '2023-01-08', 'Follow me for more', 746),
    (10008, 125, '2023-01-09', 'Tweeting from home', 776),
    (10009, 135, '2023-01-10', 'Enjoying the day', 91),
    (10010, 143, '2023-01-11', 'New tweet from user 91', 380),
    (10011, 152, '2023-01-12', 'Another tweet from user 134', 469),
    (10012, 167, '2023-01-13', 'Hello, Twitter! from user 380', 546),
    (10013, 173, '2023-01-14', 'Testing the database from user 469', 563),
    (10014, 207, '2023-01-15', 'Python is great from user 546', 669),
    (10015, 222, '2023-01-16', 'SQLite is easy to use from user 563', 712),
    (10016, 237, '2023-01-17', 'My first tweet from user 669', 746),
    (10017, 240, '2023-01-18', 'Follow me for more from user 712', 776),
    (10018, 250, '2023-01-19', 'Tweeting from home from user 746', 91),
    (10019, 273, '2023-01-20', 'Enjoying the day from user 776', 134),
    (10020, 354, '2023-01-21', 'First tweet from user 7272', 7321),
    (10021, 381, '2023-01-22', 'Tweeting for the first time!', 8167),
    (10022, 397, '2023-01-23', 'Hello Twitter! from user 8167', 8293),
    (10023, 417, '2023-01-24', 'Testing the tweeting functionality', 8333),
    (10024, 426, '2023-01-25', 'Excited to be on Twitter!', 7272)
    # Add more data here for tweets using the provided user IDs
]


cursor.executemany('INSERT INTO tweets VALUES (?, ?, ?, ?, ?)', tweets_data)

# Insert data into 'hashtags' table
hashtags_data = [
    ('#example1',),
    ('#example2',),
    ('#example3',),
    ('#example4',),
    ('#example5',),
    ('#example6',),
    ('#example7',),
    ('#example8',),
    ('#example9',),
    ('#example10',),
    ('#example11',),
    ('#example12',),
    ('#example13',),
    ('#example14',),
    ('#example15',),
    ('#example16',),
    ('#example17',),
    ('#example18',),
    ('#example19',),
    ('#example20',),
    # Add more data here for hashtags
]

cursor.executemany('INSERT INTO hashtags VALUES (?)', hashtags_data)

# Insert data into 'mentions' table
mentions_data = [
    (91, '#example1'),
    (134, '#example2'),
    (380, '#example3'),
    (469, '#example4'),
    (546, '#example5'),
    (563, '#example6'),
    (669, '#example7'),
    (712, '#example8'),
    (746, '#example9'),
    (776, '#example10'),
    (787, '#example11'),
    (823, '#example12'),
    (891, '#example13'),
    (912, '#example14'),
    (943, '#example15'),
    (987, '#example16'),
    (1012, '#example17'),
    (1045, '#example18'),
    (1076, '#example19'),
    (1123, '#example20'),
    # Add more data here for mentions using the provided user IDs
]


cursor.executemany('INSERT INTO mentions VALUES (?, ?)', mentions_data)

# Insert data into 'retweets' table
retweets_data = [
    (134, 91, '2023-01-02'),
    (380, 134, '2023-01-03'),
    (469, 380, '2023-01-04'),
    (546, 469, '2023-01-05'),
    (563, 546, '2023-01-06'),
    (669, 563, '2023-01-07'),
    (712, 669, '2023-01-08'),
    (746, 712, '2023-01-09'),
    (776, 746, '2023-01-10'),
    (91, 776, '2023-01-11'),
    (823, 787, '2023-01-12'),
    (891, 823, '2023-01-13'),
    (912, 891, '2023-01-14'),
    (943, 912, '2023-01-15'),
    (987, 943, '2023-01-16'),
    (1012, 987, '2023-01-17'),
    (1045, 1012, '2023-01-18'),
    (1076, 1045, '2023-01-19'),
    (1123, 1076, '2023-01-20'),
    # Add more data here for retweets using the provided user IDs
]
cursor.executemany('INSERT INTO retweets VALUES (?, ?, ?)', retweets_data)

# Insert data into 'lists' table
lists_data = [
    ('Example List 1', 91),
    ('Example List 2', 134),
    ('Example List 3', 380),
    ('Example List 4', 469),
    ('Example List 5', 546),
    ('Example List 6', 563),
    ('Example List 7', 669),
    ('Example List 8', 712),
    ('Example List 9', 746),
    ('Example List 10', 776),
    ('Example List 11', 823),
    ('Example List 12', 891),
    ('Example List 13', 912),
    ('Example List 14', 943),
    ('Example List 15', 987),
    ('Example List 16', 1012),
    ('Example List 17', 1045),
    ('Example List 18', 1076),
    ('Example List 19', 1123),
    # Add more data here for lists using the provided user IDs
]


cursor.executemany('INSERT INTO lists VALUES (?, ?)', lists_data)

# Insert data into 'includes' table
includes_data = [
    ('Example List 1', 134),
    ('Example List 1', 380),
    ('Example List 2', 469),
    ('Example List 2', 546),
    ('Example List 3', 563),
    ('Example List 3', 669),
    ('Example List 4', 712),
    ('Example List 4', 746),
    ('Example List 5', 776),
    ('Example List 5', 91),
    ('Example List 6', 823),
    ('Example List 6', 891),
    ('Example List 7', 912),
    ('Example List 7', 943),
    ('Example List 8', 987),
    ('Example List 8', 1012),
    ('Example List 9', 1045),
    ('Example List 9', 1076),
    ('Example List 10', 1123),
    ('Example List 10', 1189)
    # Add more data here for includes using the provided user IDs
]


cursor.executemany('INSERT INTO includes VALUES (?, ?)', includes_data)
# Step 5: Commit the changes
conn.commit()

# Step 6: Close the connection
conn.close()
