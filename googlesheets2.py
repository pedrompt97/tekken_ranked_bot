# googlesheets.py
# by Tugaviciado(2019)

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from competitors import competitor
from challengecs import challengec
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# If modifying these scopes, delete the file token.pickle.
#SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1YR4zEnhQM9JJRNoBh7q_tkmBpLDaz80uYPEOzYi94s8'
COMPS_RANGE_NAME = 'Competitors!A2:K'
CHA_RANGE_NAME = 'Challenges!A2:J'

class googlesheets2:
	def __init__(self):
		"""Shows basic usage of the Sheets API.
		Prints values from a sample spreadsheet.
		"""
		scope = ['https://spreadsheets.google.com/feeds']
		creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
		self.client = gspread.authorize(creds)

	def loadcha(self):
		# Call the Sheets API
		sheet = self.client.open_by_url("https://docs.google.com/spreadsheets/d/1YR4zEnhQM9JJRNoBh7q_tkmBpLDaz80uYPEOzYi94s8/edit#gid=1912482006")
		result = sheet.values_get(CHA_RANGE_NAME)
		values = result['values']
		
		chalist = []
		if not values:
			print('Challenges: No data found.')
		else:
			#print('id, nome, rank, pontos')
			for row in values:
				if (row != []):
					# Creates a list to be used in the bot
					startdate = datetime.datetime.strptime(row[2], '%d/%m/%Y')
					
					if row[4] == 'None':
						gamedate = None
					else:
						gamedate = datetime.datetime.strptime(row[4], '%d/%m/%Y')
						
					if row[5] == 'None':
						challengerres = None
					else:
						if row[5] == 'TRUE':
							challengerres = True
						else:
							challengerres = False
							
					if row[6] == 'None':
						challengedres = None
					else:
						if row[6] == 'TRUE':
							challengedres = True
						else:
							challengedres = False
					
					newchal = challengec(int(row[0]), int(row[1]), startdate, gamedate, challengerres, challengedres)
					chalist.append(newchal)
					# Print columns A and D, which correspond to indices 0 and 3.
					#print('%d, %s, %d, %d' % (int(row[0]), row[1], int(row[2]), int(row[3])))
		return chalist
		
	def loadcomps(self):
		# Call the Sheets API
		sheet = self.client.open_by_url("https://docs.google.com/spreadsheets/d/1YR4zEnhQM9JJRNoBh7q_tkmBpLDaz80uYPEOzYi94s8/edit#gid=2069009913")
		result = sheet.values_get(COMPS_RANGE_NAME)
		
		
		compsdict = {}
		if not result:
			print('Competitors: No data found.')
		else:
			values = result['values']
			#print('id, nome, rank, pontos')
			for row in values:
				if (row != []):
					# Creates a dictionary to be used in the bot
					pc = False
					ps4 = False
					xbox = False
					if row[8] == "TRUE":
						pc = True
					if row[9] == "TRUE":
						ps4 = True
					if row[10] == "TRUE":
						xbox = True						
					compsdict[int(row[0])] = competitor(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], pc, ps4, xbox)
					# Print columns A and D, which correspond to indices 0 and 3.
					#print('%d, %s, %d, %d' % (int(row[0]), row[1], int(row[2]), int(row[3])))
		return compsdict
	
	def updatecomps(self, player):
		sheet = self.client.open_by_url("https://docs.google.com/spreadsheets/d/1YR4zEnhQM9JJRNoBh7q_tkmBpLDaz80uYPEOzYi94s8/edit#gid=2069009913")
		result = sheet.values_get(COMPS_RANGE_NAME)
		
		
		if not result:
			range_name = "competitors!A2:K2"
		else:
			values = result['values']
			i = 2
			first_av = None
			for row in values:
				if (row == []):
					first_av = i
				else:
					if int(row[0]) == int(player.id):
						range_name = "competitors!A"+str(i)+":K"+str(i)
						break
					else:
						i += 1
				if first_av != None:
					i = first_av
				range_name = "competitors!A"+str(i)+":K"+str(i)
			
		values = [
			[
				str(player.id), str(player.nome), str(player.rank), str(player.pontos), str(player.lastop), str(player.games), str(player.wins), str(player.warns), str(player.pc), str(player.ps4), str(player.xbox)
			]
		]
		
		body = {
			'values': values
		}
		params = {}
		params['valueInputOption'] = 'USER_ENTERED'
		result = sheet.values_update(range = range_name, body = body, params = params)

	def updatecha(self, challenge):
		sheet = self.client.open_by_url("https://docs.google.com/spreadsheets/d/1YR4zEnhQM9JJRNoBh7q_tkmBpLDaz80uYPEOzYi94s8/edit#gid=1912482006")
		result = sheet.values_get(CHA_RANGE_NAME)
		values = result['values']
		
		if not values:
			range_name = "challenges!A2:J2"
		else:
			i = 2
			first_av = None
			for row in values:
				if (row == []):
					first_av = i
				else:
					if int(row[0]) == int(challenge.challengerid) and int(row[1]) == int(challenge.challengedid) and row[2] == challenge.StartDate.strftime('%d/%m/%Y'):
						range_name = "challenges!A"+str(i)+":J"+str(i)
						break
					else:
						i += 1
				if first_av != None:
					i = first_av
				range_name = "challenges!A"+str(i)+":J"+str(i)
				
		if challenge.GameDate is not None:
			gamedate = str(challenge.GameDate.strftime('%d/%m/%Y'))
		else:
			gamedate = None
			
		values = [
			[
				str(challenge.challengerid), str(challenge.challengedid), str(challenge.StartDate.strftime('%d/%m/%Y')), str(challenge.DueDate.strftime('%d/%m/%Y')), str(gamedate), str(challenge.challengerresult), str(challenge.challengedresult), str(challenge.result), str(challenge.challenger.nome), str(challenge.challenged.nome)
			]
		]
		
		body = {
			'values': values
		}
		
		params = {}
		params['valueInputOption'] = 'USER_ENTERED'
		result = sheet.values_update(range = range_name, body = body, params = params)
			
	def removecha(self, challenge):
		sheet = self.client.open_by_url("https://docs.google.com/spreadsheets/d/1YR4zEnhQM9JJRNoBh7q_tkmBpLDaz80uYPEOzYi94s8/edit#gid=1912482006")
		result = sheet.values_get(CHA_RANGE_NAME)
		values = result['values']
		
		if not values:
			range_name = "challenges!A2:J2"
		else:
			i = 2
			first_av = None
			for row in values:
				if (row == []):
					first_av = i
				else:
					if int(row[0]) == int(challenge.challengerid) and int(row[1]) == int(challenge.challengedid) and row[2] == challenge.StartDate.strftime('%d/%m/%Y'):
						range_name = "challenges!A"+str(i)+":J"+str(i)
						break
					else:
						i += 1
				if first_av != None:
					i = first_av
				range_name = "challenges!A"+str(i)+":J"+str(i)
			
		values = [
			[
				"", "", "", "", "", "", "", "", "", ""
			]
		]
		
		body = {
			'values': values
		}
		
		params = {}
		params['valueInputOption'] = 'USER_ENTERED'
		result = sheet.values_update(range = range_name, body = body, params = params)
			
if __name__ == '__main__':
	gsheet = googlesheets()
	gsheet.load()
