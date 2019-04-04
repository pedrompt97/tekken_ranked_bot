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
scope = ['https://spreadsheets.google.com/feeds']

client = gspread.authorize(creds)

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1YR4zEnhQM9JJRNoBh7q_tkmBpLDaz80uYPEOzYi94s8'
COMPS_RANGE_NAME = 'competitors!A2:K'
CHA_RANGE_NAME = 'challenges!A2:J'

class googlesheets:
	def __init__(self):
		"""Shows basic usage of the Sheets API.
		Prints values from a sample spreadsheet.
		"""
		#creds = None
		creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
		# The file token.pickle stores the user's access and refresh tokens, and is
		# created automatically when the authorization flow completes for the first
		# time.
		# if os.path.exists('token.pickle'):
			# with open('token.pickle', 'rb') as token:
				# creds = pickle.load(token)
		# # If there are no (valid) credentials available, let the user log in.
		# if not creds or not creds.valid:
			# if creds and creds.expired and creds.refresh_token:
				# creds.refresh(Request())
			# else:
				# flow = InstalledAppFlow.from_client_secrets_file(
					# 'credentials.json', SCOPES)
				# creds = flow.run_local_server()
			# # Save the credentials for the next run
			# with open('token.pickle', 'wb') as token:
				# pickle.dump(creds, token)

		self.service = build('sheets', 'v4', credentials=creds)

	def loadcha(self):
		# Call the Sheets API
		sheet = self.service.spreadsheets()
		result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
									range=CHA_RANGE_NAME).execute()
		values = result.get('values', [])
		
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
		sheet = self.service.spreadsheets()
		result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
									range=COMPS_RANGE_NAME).execute()
		values = result.get('values', [])
		
		compsdict = {}
		if not values:
			print('Competitors: No data found.')
		else:
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
		sheet = self.service.spreadsheets()
		result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
									range=COMPS_RANGE_NAME).execute()
		
		values = result.get('values', [])
		
		if not values:
			range_name = "competitors!A2:K2"
		else:
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
		result = self.service.spreadsheets().values().update(
			spreadsheetId=SPREADSHEET_ID, range=range_name,
			valueInputOption='USER_ENTERED', body=body).execute()

	def updatecha(self, challenge):
		sheet = self.service.spreadsheets()
		result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=CHA_RANGE_NAME).execute()
		
		values = result.get('values',[])
		
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
		result = self.service.spreadsheets().values().update(
			spreadsheetId=SPREADSHEET_ID, range=range_name,
			valueInputOption='USER_ENTERED', body=body).execute()
			
	def removecha(self, challenge):
		sheet = self.service.spreadsheets()
		result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=CHA_RANGE_NAME).execute()
		
		values = result.get('values',[])
		
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
		result = self.service.spreadsheets().values().update(
			spreadsheetId=SPREADSHEET_ID, range=range_name,
			valueInputOption='USER_ENTERED', body=body).execute()
			
if __name__ == '__main__':
	gsheet = googlesheets()
	gsheet.load()
