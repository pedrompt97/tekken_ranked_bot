# Challenges Class
# by Tugaviciado (2019)

import discord
from competitors import competitor
import datetime

class challengec:
	challenger = None
	challenged = None
	StartDate = None
	DueDate = None
	GameDate = None
	challengerid = None
	challengedid = None
	challengerresult = None
	challengedresult = None
	result = None
	
	def __init__(self, challenger, challenged, startdate = datetime.datetime.now(), gamedate = None, challengerresult = None, challengedresult = None):
		self.challengerid = int(challenger)
		self.challengedid = int(challenged)
		self.StartDate = startdate
		self.DueDate = startdate + datetime.timedelta(days=14)
		self.GameDate = gamedate
		self.challengerresult = challengerresult
		self.challengedresult = challengedresult
		
	def updateusers(self, challenger, challenged):
		self.challenged = challenged
		self.challenger = challenger
		
	def printchallenge(self):
		if self.GameDate is None:
			enddate = "TBD"
			lim = "\t" + str(self.challenged.nome) + " has until " + str(self.DueDate.strftime('%d/%m/%Y')) + " to accept the challenge."
		else:
			enddate = self.GameDate.strftime('%d/%m/%Y')
			lim = ""
		chal = (str(self.challenger.nome) + ' vs ' + str(self.challenged.nome) + ' : ' + str(self.StartDate.strftime('%d/%m/%Y')) + '-' + str(enddate) + lim)
		return chal
		
	def acceptchallenge(self):
		self.GameDate = self.DueDate + datetime.timedelta(days=7)
		
	def printgamedate(self):
		return str(self.GameDate.strftime('%d/%m/%Y'))
		
	def updateresult(self, result, user):
		if user == self.challengerid:
			self.challengerresult = result
			
		elif user == self.challengedid:
			self.challengedresult = result
			
		if ((self.challengerresult is not None) and (self.challengedresult is not None)):
			if self.challengerresult != self.challengedresult:
				self.result = self.challengerresult
				rankdif = abs(self.challenger.rank - self.challenged.rank)
				self.challenger.updatepoints(self.result, rankdif)
				self.challenged.updatepoints(not self.result, rankdif)
				return 0
				
			else:
				return -1
	def forceresult(self, result):
		self.result = result
		rankdif = abs(self.challenger.rank - self.challenged.rank)
		self.challenger.updatepoints(self.result, rankdif)
		self.challenged.updatepoints(not self.result, rankdif)