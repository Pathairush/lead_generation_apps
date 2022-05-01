import sqlite3

import sqlite3
conn = sqlite3.connect('lead_data.db')
c = conn.cursor()

# Reference : https://docs.oracle.com/cd/E13210_01/wlcs/docs35/campdev/schecamp.htm
def create_table():
    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS campaign
        (
            campaign_id INTEGER PRIMARY KEY,
            campaign_name TEXT,
            campaign_uid TEXT,
            is_active INTEGER,
            is_shutdown INTEGER,
            modified_date DATE,
            sponsor TEXT,
            description TEXT,
            value_proposition TEXT,
            goal_description TEXT,
            start_date DATE,
            end_date DATE
        )
        '''
    )
    c.execute('CREATE TABLE IF NOT EXISTS campaign_member(lead TEXT, customer_number TEXT, email TEXT, postdate DATE, status DATE)')


def add_data(author,title,article,postdate):
	c.execute('INSERT INTO blogtable(author,title,article,postdate) VALUES (?,?,?,?)',(author,title,article,postdate))
	conn.commit()

def view_all_notes():
	c.execute('SELECT * FROM blogtable')
	data = c.fetchall()
	return data

def view_all_titles():
	c.execute('SELECT DISTINCT title FROM blogtable')
	data = c.fetchall()
	return data

def get_blog_by_title(title):
	c.execute('SELECT * FROM blogtable WHERE title="{}"'.format(title))
	data = c.fetchall()
	return data

def get_blog_by_author(author):
	c.execute('SELECT * FROM blogtable WHERE author="{}"'.format(author))
	data = c.fetchall()
	return data

def delete_data(title):
	c.execute('DELETE FROM blogtable WHERE title="{}"'.format(title))
	conn.commit()