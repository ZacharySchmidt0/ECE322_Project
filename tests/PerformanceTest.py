import time
import os
import sys
import sqlite3
import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.sql import populate_tables as db
from modules.Tweeter import Tweeter

DATABASE_PATH = './test.db'

def time_function(func, *args, **kwargs):
    start_time = time.time()
    func(*args, **kwargs)
    end_time = time.time()
    execution_time = end_time - start_time
    return execution_time

def delete_database():
    conn = None
    try:
        # Attempt to connect to the database in read-only mode
        conn = sqlite3.connect(f"file:{DATABASE_PATH}?mode=ro", uri=True)
        conn.close()
    except sqlite3.OperationalError:
        # The database may not exist, or there could be an issue connecting to it
        pass

    # Close any existing connections
    if conn:
        conn.close()

    if os.path.exists(DATABASE_PATH):
        try:
            os.remove(DATABASE_PATH)
            print("Database deleted successfully.")
        except PermissionError:
            print("Unable to delete the database file. Make sure the database connection is closed.")
    else:
        print("Database file does not exist.")

def populate_performance_test(num_runs=5, delay_between_runs=1):
    total_create_table_time = 0
    total_populate_table_time = 0
    total_clean_table_time = 0
    total_main_pop_time = 0

    for run in range(1, num_runs + 1):
        print(f"Run {run}:")
        delete_database()

        conn, c = db.SetUp()

        try:
            # Measure CreateTable performance
            create_table_time = time_function(db.CreateTable, conn, c)
            total_create_table_time += create_table_time
            conn.commit()

            # Measure PopulateTable performance
            populate_table_time = time_function(db.PopulateTable, conn, c)
            total_populate_table_time += populate_table_time
            conn.commit()

            # Measure CleanTable performance
            clean_table_time = time_function(db.CleanTable, conn, c)
            total_clean_table_time += clean_table_time
            conn.commit()

            # Measure the entire program performance
            main_pop_time = time_function(db.main_pop)
            total_main_pop_time += main_pop_time
            conn.commit()

            print(f"CreateTable execution time: {create_table_time:.8f} seconds")
            print(f"PopulateTable execution time: {populate_table_time:.8f} seconds")
            print(f"CleanTable execution time: {clean_table_time:.8f} seconds")
            print(f"Entire program execution time: {main_pop_time:.8f} seconds")

        except Exception as e:
            print(f"An error occurred: {e}")
            conn.rollback()
        finally:
            conn.close()

        # Introduce delay between runs
        time.sleep(delay_between_runs)

    # Calculate and print the average times
    avg_create_table_time = total_create_table_time / num_runs
    avg_populate_table_time = total_populate_table_time / num_runs
    avg_clean_table_time = total_clean_table_time / num_runs
    avg_main_pop_time = total_main_pop_time / num_runs

    print("\nAverage execution times:")
    print(f"CreateTable: {avg_create_table_time:.6f} seconds")
    print(f"PopulateTable: {avg_populate_table_time:.6f} seconds")
    print(f"CleanTable: {avg_clean_table_time:.6f} seconds")
    print(f"Entire program: {avg_main_pop_time:.6f} seconds")

    print("\nPerformance test completed.")

# only functionalities are checked and not methods involving inquirerPy
def tweeter_performance_test(tweeter, iterations=5):
    total_start_time = time.time()
    conn = None  # Initialize connection variable outside the try block

    for i in range(iterations):
        print(f"Run {i}:")
        try:
            start_time = time.time()
            tweeter.get_next_user_id()
            end_time = time.time()
            print(f"get_next_user_id execution time: {end_time - start_time} seconds")

            start_time = time.time()
            tweeter.get_next_tweet_id()
            end_time = time.time()
            print(f"get_next_tweet_id execution time: {end_time - start_time} seconds")

            start_time = time.time()
            example_user = ('password', 'John Dont', 'johnt@gmail.com', 'Eggmonton', 1.0)
            tweeter.insert_user(*example_user)
            end_time = time.time()
            print(f"insert_user execution time: {end_time - start_time} seconds")

            start_time = time.time()
            tweeter.search_for_user_query('Hill')
            end_time = time.time()
            print(f"search_for_user_query execution time: {(end_time - start_time)} seconds")

            start_time = time.time()
            tweeter.search_for_tweets_query([], ['Sample'])
            end_time = time.time()
            print(f"search_for_tweets_query execution time: {(end_time - start_time)} seconds")

            start_time = time.time()
            tweeter.follow_user(i+2)
            end_time = time.time()
            print(f"follow_user execution time: {end_time - start_time - 1} seconds") # -1 to account for the sleep timer

            start_time = time.time()
            tweeter.get_tweet_statistics(1)
            end_time = time.time()
            print(f"get_tweet_statistics execution time: {end_time - start_time} seconds")

            start_time = time.time()
            tweeter.insert_retweet(i+1)
            end_time = time.time()
            print(f"insert_retweet execution time: {end_time - start_time} seconds")

            start_time = time.time()
            example_tweet = (1, datetime.date.today(), "Test tweet")
            tweeter.insert_tweet(*example_tweet)
            end_time = time.time()
            print(f"insert_tweet execution time: {end_time - start_time} seconds")

            start_time = time.time()
            tweeter.get_followers()
            end_time = time.time()
            print(f"get_followers execution time: {end_time - start_time} seconds")

            start_time = time.time()
            tweeter.get_follow_feed_tweets()
            end_time = time.time()
            print(f"get_follow_feed_tweets execution time: {end_time - start_time} seconds")

        except Exception as e:
            print(f"An error occurred: {e}")
            # If an exception occurs, close the connection and break out of the loop
            if conn:
                conn.close()
            break
        finally:
            # Close the connection in the finally block
            if conn:
                conn.close()

    total_end_time = time.time()
    total_execution_time = total_end_time - total_start_time
    average_execution_time = total_execution_time / iterations

    print(f"\nAverage execution time for all methods: {average_execution_time} seconds")

def disconnect_all_connections(database_path):
    try:
        # Connect to the database in read-only mode
        conn = sqlite3.connect(f"file:{database_path}?mode=ro", uri=True)

        # Execute a PRAGMA statement to disconnect all other connections
        conn.execute("PRAGMA busy_timeout = 3000")
        conn.execute("PRAGMA wal_checkpoint(FULL)")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    populate_performance_test()
    try:
        tweeter = Tweeter('test.db')
        tweeter.user_id = 1
        tweeter_performance_test(tweeter)
    finally:
        tweeter.close_connection()