# botteste.py
# by Tugaviciado (2019)

import asyncio
import discord
import csv
import datetime
from sglobby import lobbies
from googlesheets2 import googlesheets2 as googlesheets
from competitors import competitor
from challengecs import challengec


from discord.ext import commands

sglobbyversionNumber = "1.3.1"
tkrankversionNumber = "0.1"

description = "Hello, I am RankedBot v" + tkrankversionNumber + " by Tugaviciado. I'm a dedicated discord bot that focuses on supporting a local Tekken ranked system.\nHere are my commands:\n"
tfile = open("token.txt")
TOKEN = tfile.read()

bot = commands.Bot(command_prefix='r!', description=description, help_command = None)

compsdict = {}
challenges = []
started = False
server = None
defchannel = None
		
##############################################
#	Open backup files
##############################################

spreadsheet = googlesheets()

compsdict = spreadsheet.loadcomps()
challenges = spreadsheet.loadcha()

for chainit in challenges:
	initchallenged = compsdict[int(chainit.challengedid)]
	initchallenger = compsdict[int(chainit.challengerid)]
	chainit.updateusers(challenger = initchallenger, challenged = initchallenged)

#try:
#	with open('./competitors.csv') as compsfile:
#		csv_reader = csv.DictReader(compsfile)
#		for row in csv_reader:
#			compsdict[int(row["id"])] = competitor(row["id"], row["nome"], row["rank"], row["pontos"])
#except FileNotFoundError:
#	pass	
	
# try:
	# with open('./challenges.csv') as challengesfile:
		# cha_reader = csv.DictReader(challengesfile)
		# for row in cha_reader:
			# challenges.append(challengec(challenger = row["Challenger-id"], challenged = row["Challenged-id"], startdate = datetime.datetime.strptime(row["DataDesafio"], '%Y/%m/%d') ))
# except FileNotFoundError:
	# pass

async def check_challenges():
	await bot.wait_until_ready()
	while not bot.is_closed():
		if started:
			now = datetime.datetime.now()
			nowdelta = now - datetime.timedelta(days=3)
			for i in challenges:
				if i.GameDate is None:
					if i.DueDate.strftime('%d/%m/%Y') == nowdelta.strftime('%d/%m/%Y'):
						await defchannel.send("{0.mention}, you have unnaccepted challenges that expire in 3 days. If you don't accept, it will be considered a loss. Please check your challenges with !mychallenge, and accept all challenges".format(discord.utils.find(lambda m: m.id == i.challenged.id, server.members)))
					elif i.DueDate.strftime('%d/%m/%Y') == now.strftime('%d/%m/%Y'):
						winner = discord.utils.find(lambda m: m.id == i.challenger.id, server.members)
						loser = discord.utils.find(lambda m: m.id == i.challenged.id, server.members)
						await defchannel.send("{0.mention}, you failed to accept a challenge given by {1.name}. The game was considered a loss.".format(loser,winner))
						tmprolew = i.challenger.ranktorole(defchannel)
						tmprolel = i.challenged.ranktorole(defchannel)
						
						i.forceresult(True)
						
						spreadsheet.updatecomps(i.challenged)
						spreadsheet.updatecomps(i.challenger)
						
						if i.challenger.rank != i.challenger.oldrank:
							role = i.challenger.ranktorole(defchannel)
							await winner.remove_roles(tmprolew, tmprolel)
							await winner.add_roles(role)
						
						if i.challenged.rank != i.challenged.oldrank:
							role = i.challenged.ranktorole(defchannel)
							await loser.remove_roles(tmprolew, tmprolel)
							await loser.add_roles(role)
						
						spreadsheet.removecha(i)
					
						for a,v in enumerate(challenges):
							if i == v:
								del challenges[a]
								break
								
								
				else:
					if i.GameDate.strftime('%d/%m/%Y') == nowdelta.strftime('%d/%m/%Y'):
						await defchannel.send("{0.mention} and {1.mention}, you have an unplayed game that expires in 3 days. If you don't report the result too many times, it will be considered a loss to both. Please report all played games and play unplayed ones".format(discord.utils.find(lambda m: m.id == i.challenged.id, server.members), discord.utils.find(lambda m: m.id == i.challenger.id, server.members)))
					elif i.GameDate.strftime('%d/%m/%Y') == now.strftime('%d/%m/%Y'):
						i.challenger.incrementwarn()
						i.challenged.incrementwarn()
						
						spreadsheet.removecha(i)
					
						for a,v in enumerate(challenges):
							if i == v:
								del challenges[a]
								break
						
						rankdif = abs(i.challenger.rank-i.challenged.rank)
						
						if i.challenger.warn == 3:
							tmprole = i.challenger.ranktorole(defchannel)
							i.challenger.updatepoints(False, rankdif)
							loser = discord.utils.find(lambda m: m.id == i.challenger.id, server.members)
							
							spreadsheet.updatecomps(i.challenger)
							if i.challenger.rank != i.challenger.oldrank:
								role = i.challenger.ranktorole(defchannel)
								await loser.remove_roles(rmprole)
								await loser.add_roles(role)
								
						if i.challenged.warn == 3:
							tmprole = i.challenged.ranktorole(defchannel)
							i.challenged.updatepoints(False, rankdif)
							loser = discord.utils.find(lambda m: m.id == i.challenged.id, server.members)
							
							spreadsheet.updatecomps(i.challenged)
							if i.challenged.rank != i.challenged.oldrank:
								role = i.challenged.ranktorole(defchannel)
								await loser.remove_roles(rmprole)
								await loser.add_roles(role)
					
					
		await asyncio.sleep(5) # task runs every 24 hours
		
async def check_competitors():
	await bot.wait_until_ready()
	while not bot.is_closed():
		if started:
			for i,v in compsdict.items():
				discprof = discord.utils.find(lambda m: m.id == v.id, server.members)
				pc = False
				ps4 = False
				xbox = False
				
		
##############################################
#	Bot Commands
##############################################
	
@bot.event
async def on_ready():
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('-------')
	print("LOADED: test bot\n")
	bot.loop.create_task(check_challenges())
	
@bot.command(hidden = True)
@commands.has_permissions(manage_messages=True)
async def kill(ctx):
	await ctx.message.delete()
	# csvwname = './competitors.csv'
	# a = 0
	# while True:
		# try:
			# with open(csvwname, mode='w', newline='') as csv_file:
				# fieldnames = ['id','nome','rank', 'pontos']
				# writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
				# writer.writeheader()
				# for i, k in compsdict.items():
					# writer.writerow({'id':k.id, 'nome':k.nome, 'rank':k.rank,'pontos':k.pontos})
				# pass
			# break
		# except PermissionError:
			# csvwname = './competitors_' + str(a) + '.csv'
			# a += 1
			# continue
		# else:
			# break
			
	# csvwname = './challenges.csv'
	# a = 0
	# while True:
		# try:
			# with open(csvwname, mode='w', newline='') as csv_file:
				# fieldnames = ['Challenger-id','Challenger-nome','Challenger-rank', 'Challenged-id','Challenged-nome','Challenged-rank', 'DataDesafio', 'Prazo']
				# writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
				# writer.writeheader()
				# for i in challenges:
					# writer.writerow({'Challenger-id':i.challengerid, 'Challenger-nome':i.challenger.nome, 'Challenger-rank': i.challenger.rank, 'Challenged-id':i.challengedid, 'Challenged-nome':i.challenged.nome, 'Challenged-rank':i.challenged.rank,'DataDesafio':i.StartDate.strftime('%Y/%m/%d'), 'Prazo':i.DueDate.strftime('%Y/%m/%d')})
				# pass
			# break
		# except PermissionError:
			# csvwname = './competitors_' + str(a) + '.csv'
			# a += 1
			# continue
		# else:
			# break
	exit()

class admininstration(commands.Cog):
	def __init__(self,bot):
		self.bot = bot
		
	@commands.command()
	@commands.has_permissions(manage_messages=True)
	async def adminhelp(self, ctx):
		await ctx.message.delete()
		dms = ctx.author.dm_channel
		if dms == None:
			await ctx.author.create_dm()
			dms = ctx.author.dm_channel
		await dms.send("Teste")
		
	@commands.command(hidden=True)
	@commands.has_permissions(manage_messages=True)
	async def start(self, ctx):
		await ctx.message.delete()
		
		global server
		server = ctx.channel.guild
		
		global defchannel
		defchannel = ctx.channel
		
		global started
		started = True
		await ctx.send("Bot has started")
		
	@commands.command(hidden=True)
	@commands.has_permissions(manage_messages=True)
	async def reset(self, ctx):
		await ctx.message.delete()
		
		global server
		global defchannel
		global started
		started = False
		
		global compsdict
		global challenges
		compsdict = {}
		challenges = []
		
		compsdict = spreadsheet.loadcomps()
		challenges = spreadsheet.loadcha()

		for chainit in challenges:
			initchallenged = compsdict[int(chainit.challengedid)]
			initchallenger = compsdict[int(chainit.challengerid)]
			chainit.updateusers(challenger = initchallenger, challenged = initchallenged)
			
		started = True
		
		await ctx.send("Bot data reloaded", delete_after=10)
	
	#admin only - list all challenges
	@commands.command(hidden=True)
	@commands.has_permissions(manage_messages=True)
	async def listchallenges(self, ctx):
		await ctx.message.delete()
		for i in challenges:
			await ctx.send(i.printchallenge(), delete_after=10)
		
		
	
class rankeds(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot

	#register self into ranked system
	@commands.command()
	async def register(self, ctx, op1: str = "", op2: str = "", op3: str = ""):
		author = ctx.message.author
		await ctx.message.delete()
		
		plats = []
		plats.append(op1)
		plats.append(op2)
		plats.append(op3)
		inv = 'invalid platform(s) '
		pc = False
		ps4 = False
		xbox = False
		newplat = ""
		
		for i in plats:
			if i == "pc":
				pc = True
				newplat += "PC\n"
			elif i == "ps4":
				ps4 = True
				newplat += "PS4\n"
			elif i == "xbox":
				xbox = True
				newplat += "XBOX\n"
			elif i == "":
				pass
			else:
				inv += i + " "
		
		
		if inv != 'invalid platform(s) ':
			await ctx.send("{0.name}, ".format(author) + inv)
		
		if not pc and not ps4 and not xbox:
			await ctx.send("{0.name}, no platform registered. Please register with at least one platform".format(author))
			return
		
		if int(author.id) not in compsdict.keys():
			comp = competitor(id = author.id, nome = str(author.name), pc = pc, ps4 = ps4, xbox = xbox)
			compsdict[int(comp.id)] = comp
			spreadsheet.updatecomps(comp)
			await ctx.send('Registration done:\nName: {0.name}\nID: {0.id}\nRank: {1.rank} - '.format(author,comp) + str(comp.rankconv()) + "\n\nPlatforms: " + newplat, delete_after=10)
			role = comp.ranktorole(ctx.channel)
			await author.add_roles(role)
		else:
			com = compsdict[int(author.id)]
			if pc:
				com.updateplatform(pc = True)
			if ps4:
				com.updateplatform(ps4 = True)
			if xbox:
				com.updateplatform(xbox = True)
			await ctx.send('{0.name} already registered. Updated platforms'.format(author), delete_after=10)
			spreadsheet.updatecomps(com)
		
		role = compsdict[int(author.id)].ranktorole(ctx.channel)
		await author.add_roles(role)
		
		

	#get own information
	@commands.command()
	async def myinfo(self, ctx):
		""" Displays user info """
		author = ctx.message.author
		await ctx.message.delete()
		
		if int(author.id) in compsdict.keys():
			comp = compsdict[int(author.id)]
			await ctx.send('Competitor Info:\nName: {0.nome}\n\nRank {0.rank} - '.format(comp) + str(comp.rankconv()) + '\n{0.pontos} points'.format(comp), delete_after=10)
		else:
			await ctx.send('{0.name}, you are not a registered member. To register, type !register'.format(author), delete_after=10)
	
	#get a list of players of similar ranks
	@commands.command()
	async def getopponents(self, ctx):
		author = ctx.message.author
		await ctx.message.delete()
		
		
		if int(author.id) in compsdict.keys():
			me = compsdict[int(author.id)]
			
			# Get players of the same rank
			msg = "**Players of the same rank as {0.name}**\n".format(author)
			for i,v in compsdict.items():
				if v.rank == me.rank and v.id != me.id:
					msg += '{0.name}\n'.format(discord.utils.find(lambda m: m.id == v.id, ctx.channel.guild.members))
			
			msg += "\n\n**Players one rank higher than {0.name}**\n".format(author)
			
			# Get players one rank higher
			for i,v in compsdict.items():
				if v.rank == (me.rank)+1 and v.id != me.id:
					msg += '{0.name}\n'.format(discord.utils.find(lambda m: m.id == v.id, ctx.channel.guild.members))
		
			await ctx.send(msg)
			
		else:
			await ctx.send('{0.name}, you are not a registered member. To register, type !register'.format(author), delete_after=10)
			
	
	#challenge a player
	@commands.command()
	async def challenge(self, ctx, user: discord.User = None):
		author = ctx.message.author
		await ctx.message.delete()
		
		if user is None:
			await ctx.send('{0.name}, wrong command. To challenge someone, type !challenge <mention_to_player>, eg. !challenge {0.mention}'.format(author), delete_after=10)
			return
			
		elif user == author:
			await ctx.send('{0.name}, you cannot challenge yourself. Challenge someone else.'.format(author))
			return
		
		elif int(author.id) in compsdict.keys():
			if int(user.id) in compsdict.keys():
				newchal = challengec(challenger = int(author.id), challenged = int(user.id))
				initchallenged = compsdict[int(newchal.challengedid)]
				initchallenger = compsdict[int(newchal.challengerid)]
				newchal.updateusers(challenger = initchallenger, challenged = initchallenged)
				
				if int(newchal.challenger.lastop) == int(newchal.challenged.id):
					await ctx.send('{0.name}, your last game was with {1.name}. Challenge someone else'.format(author,user))
					return
				
				rankdif = abs(newchal.challenger.rank - newchal.challenged.rank)
				if rankdif > 1:
					await ctx.send('{0.name}, {1.name} is 2 or more ranks apart from you. Challenge someone with a closer rank.'.format(author, user))
					return
				elif newchal.challenger.rank > newchal.challenged.rank:
					await ctx.send('{0.name}, your rank is highter than {1.name}. Challenge someone of the same rank or higher'.format(author, user))
					return
					
				for i in challenges:
					if ((newchal.challenger == i.challenger and newchal.challenged == i.challenged) or (newchal.challenged == i.challenger and newchal.challenger == i.challenged)):
						await ctx.send('{0.name}, there is already a challenge between you and {1.name}'.format(author,user))
						return
				challenges.append(newchal)
				spreadsheet.updatecha(newchal)
				await ctx.send('{0.mention}, you were challenged by {1.mention}. The challenge was added to your list of challenges.\nType !mychallenges to check your challenges.\nType !accept <challenge_number> to accept this challenge.'.format(user, author))
			else:
				await ctx.send('{0.name} is not a registered member'.format(user), delete_after=10)
		else:
			await ctx.send('{0.name}, you are not a registered member. To register, type !register'.format(author), delete_after=10)
			
	
	
	#list own challenges
	@commands.command()
	async def mychallenges(self, ctx):
		await ctx.message.delete()
		author = ctx.message.author
		
		if int(author.id) in compsdict.keys():
			me = compsdict[int(author.id)]
			me.challengesarray = []
			me.gamesarray = []
			a = 1
			b = 1
			mes = ""
			anne = ""
			for i in challenges:
				if int(i.challenged.id) == int(author.id):
					me.challengesarray.append(i)
					me.gamesarray.append(i)
					mes += str(a) + " - " + i.printchallenge() + "\n"
					a += 1
				elif int(i.challenger.id) == int(author.id):
					anne += str(b) + " - " + i.printchallenge() + "\n"
					b +=1
			
			answer = ""
			if a == 1:
				answer += "{0.name}, you have no pending challenges to accept".format(author)
			else:
				answer += "{0.name}, you have active challenges:\n".format(author) + mes
				
			answer += "\n\n\n"
			
			if b == 1:
				answer += "{0.name}, no one is currently being challenged by your".format(author)
			else:
				answer += "{0.name}, you have challenged someone:\n".format(author) + anne
				
			await ctx.send(answer)	
			
		else:
			await ctx.send('{0.name}, you are not a registered member. To register, type !register'.format(author))
			
	#list own games
	@commands.command()
	async def mygames(self, ctx):
		await ctx.message.delete()
		author = ctx.message.author
		
		if int(author.id) in compsdict.keys():
			me = compsdict[int(author.id)]
			me.gamesarray = []
			a = 1
			for i in challenges:
				if i.GameDate is not None:
					if int(i.challenged.id) == int(author.id) or int(i.challenger.id) == int(author.id):
						me.gamesarray.append(i)
						mes = str(a) + " - " + i.printchallenge() + "\n"
						a += 1
			if a == 1:
				await ctx.send("{0.name}, you have no pending games to play".format(author))
			else:
				await ctx.send("{0.name}, you have games to play:\n".format(author) + mes)
		else:
			await ctx.send('{0.name}, you are not a registered member. To register, type !register'.format(author))
			
			
	#accept challenge - needs an id obtained through mychallenges
	@commands.command()
	async def accept(self, ctx, matchid: int=None):
		await ctx.message.delete()
		author = ctx.message.author
		if matchid is None:
			await ctx.send('{0.name}, you command is invalid. To accept a challenge, type !accept <challenge_number>'.format(author), delete_after=10)
			return

		if int(author.id) in compsdict.keys():
			me = compsdict[int(author.id)]
			if not me.challengesarray:
				await ctx.send('{0.name}, you have no active challenges or the challenge number you accepted was invalid. To check the challenge numbers, type !mychallenges.'.format(author), delete_after=10)
				return
			cha = me.challengesarray[matchid-1]
			cha.acceptchallenge()
			guy = discord.utils.find(lambda m: m.id == cha.challenger.id, ctx.channel.guild.members)
			await ctx.send('{0.mention}, {1.mention} has accepted your challenge. You both have until '.format(guy, author) + cha.printgamedate() + ' to finish your match.')
			spreadsheet.updatecha(cha)
					
		else:
			await ctx.send('{0.name}, you are not a registered member. To register, type !register'.format(author))
			
	@commands.command()
	async def report(self, ctx, matchid: int, result : str):
		await ctx.message.delete()
		author = ctx.message.author
		if int(author.id) in compsdict.keys():
			me = compsdict[int(author.id)]
			cha = me.gamesarray[matchid-1]
			if result == 'win':
				matchres = True
			elif result == 'lose':
				matchres = False
			else:
				await ctx.send('Invalid result. Result can only either be win or lose')
				matchres = None
			if matchres is not None:
				tmprolew = cha.challenger.ranktorole(ctx.channel)
				tmprolel = cha.challenged.ranktorole(ctx.channel)
				test = cha.updateresult(matchres, int(author.id))
				if matchres is True:
					wonlose = 'won'
				else:
					wonlose = 'lost'
				await ctx.send ('{0.name}, match result reported. You '.format(author) + wonlose + '.')
				if test == 0:	
					winner = None
					loser = None
					w1 = None
					l1 = None
					if cha.result is True:
						w1 = cha.challenger
						l1 = cha.challenged
						winner = discord.utils.find(lambda m: m.id == cha.challenger.id, ctx.channel.guild.members)
						loser = discord.utils.find(lambda m: m.id == cha.challenged.id, ctx.channel.guild.members)
					else:
						w1 = cha.challenged
						l1 = cha.challenger
						winner = discord.utils.find(lambda m: m.id == cha.challenged.id, ctx.channel.guild.members)
						loser = discord.utils.find(lambda m: m.id == cha.challenger.id, ctx.channel.guild.members)
					await ctx.send ('Match result recorded. {0.name} won againt {1.name}'.format(winner, loser))
					
					cha.challenger.updatelastop(int(cha.challenged.id))
					cha.challenged.updatelastop(int(cha.challenger.id))
					
					cha.challenger.decrementwarn()
					cha.challenged.decrementwarn()
					
					
					spreadsheet.updatecomps(cha.challenged)
					spreadsheet.updatecomps(cha.challenger)
					if winner is not None and w1 is not None and w1.rank != w1.oldrank:
						role = w1.ranktorole(ctx.channel)
						await winner.remove_roles(tmprolew, tmprolel)
						await winner.add_roles(role)
					if loser is not None and l1 is not None and l1.rank != l1.oldrank:
						role = l1.ranktorole(ctx.channel)
						await loser.remove_roles(tmprolew, tmprolel)
						await loser.add_roles(role)
					
					spreadsheet.removecha(cha)
					
					for i,v in enumerate(challenges):
						if cha == v:
							del challenges[i]
							break
				
				elif test == -1:
					await ctx.send ('Match result incoherent between two players. {0.mention} and {1.mention}, one has to win and one has to lose. Please report correctly'.format(discord.utils.find(lambda m: m.id == cha.challenger.id, ctx.channel.guild.members), discord.utils.find(lambda m: m.id == cha.challenged.id, ctx.channel.guild.members)))
					spreadsheet.updatecha(cha)
				else:
					spreadsheet.updatecha(cha)
		else:
			await ctx.send('{0.name}, you are not a registered member. To register, type !register'.format(author))
		
			
bot.add_cog(rankeds(bot))
bot.add_cog(lobbies(bot))
bot.add_cog(admininstration(bot))
bot.run(TOKEN)
