import psycopg2
import dbSecret

class TriesExceeted(Exception):
	pass

class Database:
	def __init__(self):
		self.lock = False
		self.conn = self.connect()
		self.cur = self.conn.cursor()

	def __del__(self):
		if hasattr(self, "cur"):
			self.cur.close()
		if hasattr(self, "conn"):
			self.conn.close()

	def connect(self):
		conn = psycopg2.connect(
			user = dbSecret.dbusername, 
			password = dbSecret.dbpassword,
			host = dbSecret.dbhost,
			port = dbSecret.dbport,
			dbname = dbSecret.dbname 
		)
		return conn

	def createTables(self):
		self.executeCommit("""
			CREATE TABLE translations (
				id serial PRIMARY KEY,
				english TEXT NOT NULL,
				finnish TEXT NOT NULL,
				explanation TEXT
			)
		""")

	def getTranslations(self):
		ret = self.executeQuery("SELECT english, finnish, explanation FROM translations")
		formattedRet = [
				{
					"en": ele[0],
					"fi": ele[1],
					"expl": ele[2],
				}
				for ele in ret]
		return formattedRet

	def addTranslation(self, english, finnish, explanation = ""):
		self.executeCommit("INSERT INTO translations (english, finnish, explanation) VALUES (%s, %s, %s);", (english, finnish, explanation))

	def executeQuery(self, query, params = (), tries = 5):
		try:
			self.cur.execute(query, params)
			return self.cur.fetchall()
		except psycopg2.DatabaseError as ee:
			if tries <= 0:
				raise TriesExceeted()

			self.conn = self.connect()
			self.cur = self.conn.cursor()
			self.executeQuery(query, params, tries - 1)

	def executeCommit(self, query, params = (), tries = 5):
		try:
			self.cur.execute(query, params)
			self.conn.commit()
		except psycopg2.DatabaseError as ee:
			if tries <= 0:
				raise TriesExceeted()

			self.conn = self.connect()
			self.cur = self.conn.cursor()
			self.executeCommit(query, params, tries - 1)

db = Database()
