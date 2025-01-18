import mysql.connector
from prettytable import PrettyTable

dbconfig = sakila_dbconfig = {
    'host': 'ich-db.ccegls0svc9m.eu-central-1.rds.amazonaws.com',
    'user': 'ich1',
    'password': 'password',
    'database': 'sakila'
}

def connect_to_db():
    return mysql.connector.connect(**dbconfig)

def search_movies_by_keyword(keyword):
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)
    query = "SELECT title FROM film WHERE title LIKE %s LIMIT 10"
    cursor.execute(query, (f"%{keyword}%",))
    results = cursor.fetchall()
    db.close()
    return results

def search_movies_by_genre_and_year(genre, year):
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)
    query = """
    SELECT title
    FROM film
    JOIN film_category fc ON film.film_id = fc.film_id
    JOIN category c ON fc.category_id = c.category_id
    WHERE c.name = %s AND film.release_year = %s
    LIMIT 10
    """
    cursor.execute(query, (genre, year))
    results = cursor.fetchall()
    db.close()
    return results


def log_search_query(query):
    db = connect_to_db()
    cursor = db.cursor()
    check_query = "SELECT id FROM search_queries WHERE query = %s"
    cursor.execute(check_query, (query,))
    result = cursor.fetchone()
    if result:
        update_query = "UPDATE search_queries SET search_count = search_count + 1 WHERE id = %s"
        cursor.execute(update_query, (result['id'],))
    else:
        insert_query = "INSERT INTO search_queries (query) VALUES (%s)"
        cursor.execute(insert_query, (query,))
    db.commit()
    db.close()


def get_popular_searches():
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)
    query = "SELECT query, COUNT(*) AS query_count FROM search_queries GROUP BY query ORDER BY query_count DESC LIMIT 10";
    cursor.execute(query)
    results = cursor.fetchall()
    db.close()
    return results


def search_movies_by_actor(actor_name):
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)
    query = """
    SELECT f.title
    FROM film f
    JOIN film_actor fa ON f.film_id = fa.film_id
    JOIN actor a ON fa.actor_id = a.actor_id
    WHERE CONCAT(a.first_name, ' ', a.last_name) LIKE %s
    LIMIT 10
    """
    cursor.execute(query, (f"%{actor_name}%",))
    results = cursor.fetchall()
    db.close()
    return results


def search_top_rated_movies():
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)
    query = """
    SELECT title, rating
    FROM film
    ORDER BY rating DESC
    LIMIT 10
    """
    cursor.execute(query)
    results = cursor.fetchall()
    db.close()
    return results


def search_longest_movies():
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)
    query = """
    SELECT title, length
    FROM film
    ORDER BY length DESC
    LIMIT 10
    """
    cursor.execute(query)
    results = cursor.fetchall()
    db.close()
    return results


def search_comedy_movies():
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)
    query = """
    SELECT f.title, f.description, f.release_year
    FROM film f
    JOIN film_category fc ON f.film_id = fc.film_id
    JOIN category c ON fc.category_id = c.category_id
    WHERE c.name = 'Comedy'
    LIMIT 10
    """
    cursor.execute(query)
    results = cursor.fetchall()
    db.close()
    return results


def search_movie_by_id(movie_id):
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)
    query = "SELECT title FROM film WHERE film_id = %s"
    cursor.execute(query, (movie_id,))
    result = cursor.fetchone()
    db.close()
    return result


def display_menu():
    print("""
    1: Search for a movie by 
    2: Search for films by genre and year
    3: View the top 10 queries
    4: Movie search by actors
    5: Movie search by id
    6: Search for movies by rating (top 10)
    7: Search for Comedy movies
    8: Search for the longest 10 movies
    9: Exit
    """)


def main():
    while True:
        display_menu()
        choice = input("Enter the action number: ")

        if choice == '1':
            keyword = input("Enter a search keyword: ")
            results = search_movies_by_keyword(keyword)
            if results:
                table = PrettyTable(['Title'])
                for row in results:
                    table.add_row([row['title']])
                print(table)
            else:
                print("Movies not found.")

        elif choice == '2':
            genre = input("Enter genre: ")
            year = input("Enter year: ")
            results = search_movies_by_genre_and_year(genre, year)
            if results:
                table = PrettyTable(['Title'])
                for row in results:
                    table.add_row([row['title']])
                print(table)
            else:
                print("Movies not found.")

        elif choice == '3':
            results = get_popular_searches()
            if results:
                table = PrettyTable(['Request', 'Number of requests'])
                for row in results:
                    table.add_row([row['query'], row['search_count']])
                print(table)
            else:
                print("No popular requests yet.")

        elif choice == '4':
            actor_name = input("Enter the actor's name: ")
            results = search_movies_by_actor(actor_name)
            if results:
                table = PrettyTable(['Title'])
                for row in results:
                    table.add_row([row['title']])
                print(table)
            else:
                print("No movies with this actor were found.")

        elif choice == '5':
            movie_id = input("Enter the movie ID: ")
            result = search_movie_by_id(movie_id)
            if result:
                print(f"The name of the movie: {result['title']}")
            else:
                print("The movie was not found.")

        elif choice == '6':
            results = search_top_rated_movies()
            if results:
                table = PrettyTable(['Title', 'Rating'])
                for row in results:
                    table.add_row([row['title'], row['rating']])
                print(table)
            else:
                print("Movies not found.")

        elif choice == '7':
            results = search_comedy_movies()
            if results:
                table = PrettyTable(['Title'])
                for row in results:
                    table.add_row([row['title']])
                print(table)
            else:
                print("No comedy films were found.")

        elif choice == '8':
            results = search_longest_movies()
            if results:
                table = PrettyTable(['Title', 'Length'])
                for row in results:
                    table.add_row([row['title'], row['length']])
                print(table)
            else:
                print("No long films were found.")

        elif choice == '9':
            print("Exiting the program.")
            break

        else:
            print("Wrong choice. Please select action 1 to 9.")


if __name__ == '__main__':
    main()
