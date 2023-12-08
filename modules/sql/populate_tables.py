import sqlite3
import random
from datetime import date, timedelta

def SetUp():
  conn = sqlite3.connect('./test.db')
  c = conn.cursor()
  return conn, c

def CreateTable(conn, c):

  #Creating the table to operate on
  c.execute("""create table users (
    usr         int,
    pwd	        text,
    name        text,
    email       text,
    city        text,
    timezone    float,
    primary key (usr)
  );""")
  conn.commit()

  c.execute("""create table follows (
    flwer       int,
    flwee       int,
    start_date  date,
    primary key (flwer,flwee),
    foreign key (flwer) references users,
    foreign key (flwee) references users
  );""")
  conn.commit()

  c.execute("""create table tweets (
    tid	        int,
    writer      int,
    tdate       date,
    text        text,
    replyto     int,
    primary key (tid),
    foreign key (writer) references users,
    foreign key (replyto) references tweets
  );""")
  conn.commit()

  c.execute("""create table hashtags (
    term        text,
    primary key (term)
  );""")
  conn.commit()

  c.execute("""create table mentions (
    tid         int,
    term        text,
    primary key (tid,term),
    foreign key (tid) references tweets,
    foreign key (term) references hashtags
  );""")
  conn.commit()

  c.execute("""create table retweets (
    usr         int,
    tid         int,
    rdate       date,
    primary key (usr,tid),
    foreign key (usr) references users,
    foreign key (tid) references tweets
  );""")
  conn.commit()

  c.execute("""create table lists (
    lname        text,
    owner        int,
    primary key (lname),
    foreign key (owner) references users
  );""")
  conn.commit()

  c.execute("""create table includes (
    lname       text,
    member      int,
    primary key (lname,member),
    foreign key (lname) references lists,
    foreign key (member) references users
  );""")
  conn.commit()

def CleanTable(conn, c):
  c.execute("""drop table if exists users;""")
  c.execute("""drop table if exists follows;""")
  c.execute("""drop table if exists tweets;""")
  c.execute("""drop table if exists hashtags;""")
  c.execute("""drop table if exists mentions;""")
  c.execute("""drop table if exists retweets;""")
  c.execute("""drop table if exists lists;""")
  c.execute("""drop table if exists includes;""")
  conn.commit()

def PopulateTable(conn, c):
        # Insert 50 sample users
    c.executemany(
        "INSERT INTO users (usr, pwd, name, email, city, timezone) VALUES (?, ?, ?, ?, ?, ?);",
        [
            (1, 'password1', 'John Doe', 'john@example.com', 'New York', -5.0),
            (2, 'password2', 'Jane Smith', 'jane@example.com', 'Los Angeles', -8.0),
            (3, 'password3', 'Bob Johnson', 'bob@example.com', 'Chicago', -6.0),
            (4, 'password4', 'Alice Brown', 'alice@example.com', 'Houston', -6.0),
            (5, 'password5', 'Eve Wilson', 'eve@example.com', 'Miami', -5.0),
            (6, 'password6', 'Charlie Lee', 'charlie@example.com', 'San Francisco', -8.0),
            (7, 'password7', 'Grace White', 'grace@example.com', 'Boston', -5.0),
            (8, 'password8', 'David Hall', 'david@example.com', 'Dallas', -6.0),
            (9, 'password9', 'Sophia Clark', 'sophia@example.com', 'Seattle', -8.0),
            (10, 'password10', 'Liam Wilson', 'liam@example.com', 'Denver', -7.0),
            (11, 'password11', 'Olivia Davis', 'olivia@example.com', 'Austin', -6.0),
            (12, 'password12', 'Noah Harris', 'noah@example.com', 'San Diego', -8.0),
            (13, 'password13', 'Ava Martin', 'ava@example.com', 'Portland', -8.0),
            (14, 'password14', 'Liam Martinez', 'liam@example.com', 'Seattle', -8.0),
            (15, 'password15', 'Emma Jones', 'emma@example.com', 'Chicago', -6.0),
            (16, 'password16', 'William White', 'william@example.com', 'Los Angeles', -8.0),
            (17, 'password17', 'Olivia Garcia', 'olivia@example.com', 'San Francisco', -8.0),
            (18, 'password18', 'Logan Smith', 'logan@example.com', 'New York', -5.0),
            (19, 'password19', 'Sophia Johnson', 'sophia@example.com', 'Miami', -5.0),
            (20, 'password20', 'Elijah Taylor', 'elijah@example.com', 'Houston', -6.0),
            (21, 'password21', 'Ava Davis', 'ava@example.com', 'Boston', -5.0),
            (22, 'password22', 'Mia Brown', 'mia@example.com', 'Dallas', -6.0),
            (23, 'password23', 'Lucas Harris', 'lucas@example.com', 'San Diego', -8.0),
            (24, 'password24', 'Mason Martin', 'mason@example.com', 'Portland', -8.0),
            (25, 'password25', 'Ella Johnson', 'ella@example.com', 'San Francisco', -8.0),
            (26, 'password26', 'Aiden Smith', 'aiden@example.com', 'Los Angeles', -8.0),
            (27, 'password27', 'Sofia Lee', 'sofia@example.com', 'Chicago', -6.0),
            (28, 'password28', 'Ethan Wilson', 'ethan@example.com', 'New York', -5.0),
            (29, 'password29', 'Jackson Clark', 'jackson@example.com', 'Austin', -6.0),
            (30, 'password30', 'Madison Martin', 'madison@example.com', 'Seattle', -8.0),
            (31, 'password31', 'Avery Harris', 'avery@example.com', 'San Francisco', -8.0),
            (32, 'password32', 'Aria Davis', 'aria@example.com', 'San Diego', -8.0),
            (33, 'password33', 'Evelyn Brown', 'evelyn@example.com', 'Chicago', -6.0),
            (34, 'password34', 'Sebastian Smith', 'sebastian@example.com', 'Los Angeles', -8.0),
            (35, 'password35', 'Liam Williams', 'liam@example.com', 'San Francisco', -8.0),
            (36, 'password36', 'Ella Lewis', 'ella@example.com', 'Houston', -6.0),
            (37, 'password37', 'Michael Johnson', 'michael@example.com', 'New York', -5.0),
            (38, 'password38', 'Abigail Martin', 'abigail@example.com', 'Miami', -5.0),
            (39, 'password39', 'Mia Smith', 'mia@example.com', 'Dallas', -6.0),
            (40, 'password40', 'Ethan Turner', 'ethan@example.com', 'Portland', -8.0),
            (41, 'password41', 'Oliver Allen', 'oliver@example.com', 'San Francisco', -8.0),
            (42, 'password42', 'Amelia Wright', 'amelia@example.com', 'Los Angeles', -8.0),
            (43, 'password43', 'Harper Davis', 'harper@example.com', 'Chicago', -6.0),
            (44, 'password44', 'Lucas Hill', 'lucas@example.com', 'New York', -5.0),
            (45, 'password45', 'Aiden Perez', 'aiden@example.com', 'Austin', -6.0),
            (46, 'password46', 'Evelyn Allen', 'evelyn@example.com', 'Seattle', -8.0),
            (47, 'password47', 'Jackson Bennett', 'jackson@example.com', 'San Francisco', -8.0),
            (48, 'password48', 'Sophia Torres', 'sophia@example.com', 'San Diego', -8.0),
            (49, 'password49', 'Lucy Reed', 'lucy@example.com', 'Chicago', -6.0),
            (50, 'password50', 'Avery Hill', 'avery@example.com', 'Los Angeles', -8.0)
        ]
    )
    conn.commit()

    
        # Generate 100 sample follow relationships
    follow_entries = []
    existing_pairs = set()

    for i in range(1, 101):
        flwer = random.randint(1, 50)  # Random follower ID (assuming user IDs from 1 to 50)
        flwee = random.randint(1, 50)  # Random followee ID (assuming user IDs from 1 to 50)

        while flwer == flwee or (flwer, flwee) in existing_pairs:
            # Ensure the follower and followee are not the same and the pair is unique
            flwer = random.randint(1, 50)
            flwee = random.randint(1, 50)

        existing_pairs.add((flwer, flwee))
        start_date = date.today() - timedelta(days=random.randint(1, 365))  # Random start date in the last year

        follow_entries.append((flwer, flwee, start_date))

    # Insert the follow entries
    c.executemany(
        "INSERT INTO follows (flwer, flwee, start_date) VALUES (?, ?, ?);",
        follow_entries
    )
    conn.commit()

    
        # Generate 100 sample tweets
    tweet_entries = []

    for tid in range(1, 101):
        writer = random.randint(1, 50)  # Random writer ID (assuming user IDs from 1 to 50)
        tdate = date.today() - timedelta(days=random.randint(1, 365))  # Random tweet date in the last year
        text = f"Sample tweet {tid}"
        
        # Randomly set a replyto value (either None or another tweet ID)
        if tid == 1: 
          replyto = None
        else:
            replyto = random.choice([None, random.randint(1, tid - 1)])
        tweet_entries.append((tid, writer, tdate, text, replyto))

    # Insert the tweet entries
    c.executemany(
        "INSERT INTO tweets (tid, writer, tdate, text, replyto) VALUES (?, ?, ?, ?, ?);",
        tweet_entries
    )
    conn.commit()


        # Generate 100 sample hashtags
    hashtag_entries = []

    for i in range(1, 101):
        term = f"#hashtag{i}"
        hashtag_entries.append((term,))

    # Insert the hashtag entries
    c.executemany(
        "INSERT INTO hashtags (term) VALUES (?);",
        hashtag_entries
    )
    conn.commit()


        # Generate 100 sample mentions
    mention_entries = []

    for i in range(1, 101):
        tid = random.randint(1, 100)  # Assuming you have 100 tweets in the tweets table
        term = f"#hashtag{i}"
        mention_entries.append((tid, term))

    # Insert the mention entries
    c.executemany(
        "INSERT INTO mentions (tid, term) VALUES (?, ?);",
        mention_entries
    )
    conn.commit()


        # Generate 100 sample retweets
    retweet_entries = []
    existing_pairs = set()

    for i in range(1, 101):
        usr = random.randint(1, 50)  # Assuming you have 50 users in the users table
        tid = random.randint(1, 100)  # Assuming you have 100 tweets in the tweets table

        while (usr, tid) in existing_pairs:
            # Ensure the (usr, tid) pair is unique
            usr = random.randint(1, 50)
            tid = random.randint(1, 100)

        existing_pairs.add((usr, tid))
        rdate = date.today() - timedelta(days=random.randint(1, 365))  # Random retweet date in the last year

        retweet_entries.append((usr, tid, rdate))

    # Insert the retweet entries
    c.executemany(
        "INSERT INTO retweets (usr, tid, rdate) VALUES (?, ?, ?);",
        retweet_entries
    )
    conn.commit()


        # Generate 100 sample lists
    list_entries = []

    for i in range(1, 101):
        lname = f"List{i}"
        owner = random.randint(1, 50)  # Assuming you have 50 users in the users table
        list_entries.append((lname, owner))

    # Insert the list entries
    c.executemany(
        "INSERT INTO lists (lname, owner) VALUES (?, ?);",
        list_entries
    )
    conn.commit()


        # Generate 100 sample list memberships
    include_entries = []

    for i in range(1, 101):
        lname = f"List{i}"
        member = random.randint(1, 50)  # Assuming you have 50 users in the users table
        include_entries.append((lname, member))

    # Insert the list membership entries
    c.executemany(
        "INSERT INTO includes (lname, member) VALUES (?, ?);",
        include_entries
    )
    conn.commit()


def main_pop():
  conn, c = SetUp()
  CleanTable(conn, c)
  CreateTable(conn, c)
  PopulateTable(conn, c)
  conn.close()


if __name__ == "__main__":
    main_pop()