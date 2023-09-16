import psycopg2
from getpass import getpass


def registration():
    username = input('Username: ')
    password = getpass()
    email = input('Email: ')

    try:
        connection = psycopg2.connect(
            host='ep-rapid-dream-463808-pooler.eu-central-1.aws.neon.tech',
            port='5432',
            database='neondb',
            user='roleksnellixxx',
            password='evxR6GO2pEIq'
        )

        cursor = connection.cursor()

        query = 'INSERT INTO users (username, password, email) VALUES (%s, %s, %s)'
        cursor.execute(query, (username, password, email))
        connection.commit()

        print('User successfully registered!')
    except Exception as error:
        print('An error occurred while registering user: ', error)
        


def login():
    pass


if __name__ == '__main__':
    registration()