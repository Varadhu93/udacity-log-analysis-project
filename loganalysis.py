#!/usr/bin/env python3
'''
loganalysis.py - Implementation of the log analysis project
'''
import psycopg2
from datetime import datetime

DBNAME = "news"


def mostPopularArticles():
    '''
    Returns the three most popular articles
    '''
    try:
        db = psycopg2.connect(database=DBNAME)
    except psycopg2.OperationalError as e:
        print("unable to connect error: %s " % e)
    cur = db.cursor()
    query = """SELECT title, slug, views
            FROM articles
            INNER JOIN(
                SELECT path, count(path) as views
                FROM log
                GROUP BY log.path
            ) as log
            ON log.path = '/article/' || articles.slug
            ORDER BY views desc
            LIMIT 3
            """
    cur.execute(query)
    popularArticles = cur.fetchall()
    for row in popularArticles:
        print("{} -- {} views".format(row[0], str(row[2])))
    db.close()
    return popularArticles


def mostPopularAuthor():
    '''
    Returns the most popular authors of all time
    '''
    try:
        db = psycopg2.connect(database=DBNAME)
    except psycopg2.OperationalError as e:
        print("unable to connect error: %s " % e)
    cur = db.cursor()
    query = """
            SELECT name, views
            FROM authors
            JOIN(
                SELECT sub.author, views
                FROM(
                    SELECT author, count(*) as views
                    FROM articles
                    JOIN log
                    ON log.path = '/article/' || articles.slug
                    GROUP BY author
                    ORDER BY views DESC
                    )sub
                    )sub2
                ON sub2.author = authors.id
            """
    cur.execute(query)
    popularAuthors = cur.fetchall()
    for row in popularAuthors:
        print("{} -- {} views".format(row[0], str(row[1])))
    db.close()
    return popularAuthors


def mostErrorsDay():
    '''
    Returns the day with error percentage > 1
    '''
    try:
        db = psycopg2.connect(database=DBNAME)
    except psycopg2.OperationalError as e:
        print("unable to connect error: %s " % e)
    cur = db.cursor()
    query_requestsPerDay = """
                            CREATE OR REPLACE VIEW requests_per_day AS
                            SELECT
                            COUNT(*)::numeric as num, time::date as day
                            FROM log
                            GROUP BY day
                            ORDER BY day DESC;
                        """
    cur.execute(query_requestsPerDay)
    query_errorsPerDay = """
                            CREATE OR REPLACE VIEW errors_per_day AS
                            SELECT
                            COUNT(*)::numeric as num, time::date as day
                            FROM log
                            WHERE status !='200 OK'
                            GROUP BY day
                            ORDER BY day DESC;
                        """
    cur.execute(query_errorsPerDay)
    query_errorPercentage = """
                                CREATE OR REPLACE VIEW day_with_most_error
                                AS(
                                    SELECT * FROM(
                                    SELECT TO_CHAR
                                    (requests_per_day.day,'Mon DD, YYYY'),
                                    (errors_per_day.num::float/requests_per_day.num::float)*100
                                    AS error_percentage
                                    FROM requests_per_day, errors_per_day
                                    WHERE
                                    requests_per_day.day=errors_per_day.day)
                                    AS result WHERE error_percentage > 1);
                            """
    cur.execute(query_errorPercentage)
    query_results = "SELECT * FROM day_with_most_error;"
    cur.execute(query_results)
    results = cur.fetchall()
    for row in results:
        errorRoundOff = round(row[1], 1)
        print("{} -- {} %% errors".format(row[0], errorRoundOff))
    db.close()
    return results


if __name__ == '__main__':
    '''
    Log Analysis execution point
    '''
    print("1. Three most popular articles of all time: ")
    print("---------------------------------------------")
    mostPopularArticles()
    print("---------------------------------------------")
    print("2. Most popular authors: ")
    print("---------------------------------------------")
    mostPopularAuthor()
    print("---------------------------------------------")
    print("3. Day with most error percentage > 1: ")
    mostErrorsDay()
    print("---------------------------------------------")
