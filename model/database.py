import sqlite3
import json
import os
import collections

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "garrulous.db")
conn = sqlite3.connect(db_path)
db_cursor = conn.cursor()

class database(object):
	def __init__(self):
		super(database, self).__init__()
    # Read
	# Read All Users
	def ReadUsers(self):
		db_cursor.execute("SELECT uid, first_name, last_name, email, password FROM users")
		rows = db_cursor.fetchall()
		objects_list = []
		for row in rows:
			d = collections.OrderedDict()
			d['uid'] = row[0]
			d['first_name'] = row[1]
			d['last_name'] = row[2]
			d['email'] = row[3]
			d['password'] = row[4]
			objects_list.append(d)
		return json.dumps(objects_list)

	# Read User Information By User ID.
	def ReadUserByUID(self,uid):
		uid = (uid,)
		db_cursor.execute('SELECT uid, first_name, last_name, email, password FROM users WHERE uid=?', uid)
		rows = db_cursor.fetchall()
		objects_list = []
		for row in rows:
			d = collections.OrderedDict()
			d['uid'] = row[0]
			d['first_name'] = row[1]
			d['last_name'] = row[2]
			d['email'] = row[3]
			d['password'] = row[4]
			objects_list.append(d)
		return json.dumps(objects_list)

	# Read About User By User ID.
	def ReadAboutUserByUID(self, uid):
		db_cursor.execute('SELECT age, about_me, location, university FROM about_user WHERE uid=?', (uid))
		rows = db_cursor.fetchall()
		objects_list = []
		for row in rows:
			d = collections.OrderedDict()
			d['age'] = row[0]
			d['about_me'] = row[1]
			d['location'] = row[2]
			d['university'] = row[3]
			objects_list.append(d)
		return json.dumps(objects_list)

	# Read Messages By User ID.
	def ReadMessageByUID(self, uid, sender_id):
		db_cursor.execute('SELECT uid_message_from, uid_message_to, subject, \
			message, is_read, date_time WHERE uid_message_to=? AND uid_message_from=?',\
			(uid, sender_id))
		objects_list = []
		for row in rows:
			d = collections.OrderedDict()
			d['uid_message_from'] = row[0]
			d['uid_message_to'] = row[1]
			d['subject'] = row[2]
			d['is_read'] = row[3]
			d['date_time'] = row[4]
		return uid

	# Read Friendships By User ID.
	def ReadFriendshipsByUID(self, uid):
		try:
			db_cursor.execute("SELECT uid_connected_with FROM friendships WHERE uid=?", (uid))
			rows = db_cursor.fetchall()
			objects_list = []
			for row in rows:
				d = collections.OrderedDict()
				d['uid_connected_with'] = row[0]
				objects_list.append(d)
		except Exception, e:
			raise e
		print uid

    # Create
    # Create New User
	def CreateUser(self, first_name, last_name, email, password):
		try:
			db_cursor.execute("INSERT INTO users (first_name,last_name,email,password) \
				VALUES (?,?,?,?) ", (first_name, last_name, email, password))
		except Exception, e:
			raise e

    # Create User table if it does not exist.
	def CreateUserTable(self):
		db_cursor.execute("")

	# Create About User table if it does not exist.
	def CreateAboutUserTable(self):
		db_cursor.execute()

	# Create Friendship Table if it does not exist.
	def CreateFriendshipTable(self):
		db_cursor.execute()

	# Create Message Table if it does not exist. 	
	def CreateMessagesTable(self):
		try:
			db_cursor.execute("")
		except Exception, e:
			raise e

    # Update
	def UpdateAboutUserbyUID(self, uid, age, about_me, location, university):
		try:
			db_cursor.execute("UPDATE about_user SET age=?, about_me=?, location=?, university=? \
				WHERE uid=?", (age, about_me, location, university, uid))
		except Exception, e:
			raise e

	def UpdateUserByUID(self, uid, first_name, last_name, email, password):
		try:
			db_cursor.execute("UPDATE users SET first_name=?, last_name=?, email=?, password=? \
				WHERE uid=?", (first_name, last_name, email, password, uid))
		except Exception, e:
			raise e

	# Delete
	def DeleteFriend(self,uid, friend_uid):
		try:
			db_cursor.execute("DELETE FROM friendships WHERE uid= ? AND uid_connected_with=?", \
				(uid, friend_uid))
		except Exception, e:
			raise e

