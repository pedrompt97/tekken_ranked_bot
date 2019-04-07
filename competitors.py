# Players Class
# by Tugaviciado (2019)

import discord
	
class competitor:

	id = None
	pontos = None
	rank = None
	nome = None
	lastop = None
	challengesarray = None
	gamesarray = None
	oldrank = None
	games = None
	wins = None
	warns = None
	pc = None
	ps4 = None
	xbox = None
	nonearrrank = None
	
	def __init__(self, id = 0, nome = "", rank = 1, pontos = 0, lastop = -1, games = 0, wins = 0, warns = 0, pc = False, ps4 = False, xbox = False):
		self.id = int(id)
		self.nome = str(nome)
		self.pontos = float(pontos)
		self.rank = int(rank)
		self.lastop = int(lastop)
		self.games = int(games)
		self.wins = int(wins)
		self.warns = int(warns)
		self.pc = pc
		self.ps4 = ps4
		self.xbox = xbox
		self.nonearrank = False
		
	def getrank(self):
		return self.rank
		
	def getid(self):
		return self.id
		
	def getpontos(self):
		return self.pontos
		
	def getnome(self):
		return self.nome
		
	def rankconv(self):
		if self.rank == 1:
			return "Beginner"
		elif self.rank == 2:
			return "Silver"
		elif self.rank == 3:
			return "Light Blue"
		elif self.rank == 4:
			return "Green"
		elif self.rank == 5:
			return "Yellow"
		elif self.rank == 6:
			return "Orange"
		elif self.rank == 7:
			return "Red"
		elif self.rank == 8:
			return "Purple"
		elif self.rank == 9:
			return "True Blue"
		elif self.rank == 10:
			return "Emperor"
		elif self.rank == 11:
			return "Tekken King"
		elif self.rank == 12:
			return "Tekken God"
		elif self.rank == 13:
			return "True Tekken God"
		elif self.rank == 14:
			return "Tekken God Prime"
		else:
			return "Undefined"
			
	def ranktorole(self, channel):
		if self.rank == 1:
			return discord.utils.find(lambda m: m.name == 'Rank 1 Beginner', channel.guild.roles)
		elif self.rank == 2:
			return discord.utils.find(lambda m: m.name == 'Rank 2 Silver', channel.guild.roles)
		elif self.rank == 3:
			return discord.utils.find(lambda m: m.name == 'Rank 3 Light Blue', channel.guild.roles)
		elif self.rank == 4:
			return discord.utils.find(lambda m: m.name == 'Rank 4 Green', channel.guild.roles)
		elif self.rank == 5:
			return discord.utils.find(lambda m: m.name == 'Rank 5 Yellow', channel.guild.roles)
		elif self.rank == 6:
			return discord.utils.find(lambda m: m.name == 'Rank 6 Orange', channel.guild.roles)
		elif self.rank == 7:
			return discord.utils.find(lambda m: m.name == 'Rank 7 Red', channel.guild.roles)
		elif self.rank == 8:
			return discord.utils.find(lambda m: m.name == 'Rank 8 Purple', channel.guild.roles)
		elif self.rank == 9:
			return discord.utils.find(lambda m: m.name == 'Rank 9 True Blue', channel.guild.roles)
		elif self.rank == 10:
			return discord.utils.find(lambda m: m.name == 'Rank 10 Emperor', channel.guild.roles)
		elif self.rank == 11:
			return discord.utils.find(lambda m: m.name == 'Rank 11 Tekken King', channel.guild.roles)
		elif self.rank == 12:
			return discord.utils.find(lambda m: m.name == 'Rank 12 Tekken God', channel.guild.roles)
		elif self.rank == 13:
			return discord.utils.find(lambda m: m.name == 'Rank 13 True Tekken God', channel.guild.roles)
		else: # 14
			return discord.utils.find(lambda m: m.name == 'Rank 14 Tekken God Prime', channel.guild.roles)	
			
	def updatepoints(self, result, rankdif):
		self.games += 1
		if result is True:
			self.wins += 1
			if rankdif == 0:
				self.pontos += 1
			else:
				self.pontos += 0.5
		else:
			if rankdif == 0:
				self.pontos -= 1
			else:
				self.pontos -= 0.5
		if self.pontos < -1 and self.rank == 1:
			self.pontos = -1
		elif self.pontos > 5 and self.rank == 14:
			self.pontos = 5
		self.updaterank()

	def updaterank(self):
		self.oldrank = self.rank
		if self.rank == 1:
			if self.pontos >= 1:
				self.rank += 1
				self.pontos = 0
	
		elif self.rank in range(2,5):
			if self.pontos >= 2:
				self.rank += 1
				self.pontos = 0
			elif self.pontos <= -2:
				self.rank -= 1
				self.pontos = 0
			
		elif self.rank in range(6,9):
			if self.pontos >= 3:
				self.rank += 1
				self.pontos = 0
			elif self.pontos <= -3:
				self.rank -= 1
				self.pontos = 0
	
		elif self.rank in range(10,12):
			if self.pontos >= 4:
				self.rank += 1
				self.pontos = 0
			elif self.pontos <= -4:
				self.rank -= 1
				self.pontos = 0
	
		elif self.rank == 13:
			if self.pontos >= 5:
				self.rank += 1
				self.pontos = 0
			elif self.pontos <= -5:
				self.rank -= 1
				self.pontos = 0
		elif self.rank == 14:
			if self.pontos <= -5:
				self.rank -= 1
				self.pontos = 0
		return
		

	def updatelastop(self, opid):
		self.lastop = opid

	def incremmentwarn(self):
		warn += 1
		if warn >= 3:
			warn = 3
	
	def decrementwarn(self):
		warn -= 1
		if warn <= 0:
			warn = 0
			
	def updateplatform(self, pc = None, ps4 = None, xbox = None):
		if pc is not None:
			self.pc = pc
		if ps4 is not None:
			self.ps4 = ps4
		if xbox is not None:
			self.xbox = xbox