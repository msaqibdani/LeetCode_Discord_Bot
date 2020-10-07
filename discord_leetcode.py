# IMPORT DISCORD.PY. ALLOWS ACCESS TO DISCORD'S API.
import discord

# IMPORT PYTHON URLOPEN
import requests


# IMPORT THE OS MODULE.
import os

# IMPORT JSON
import json

# IMPORT LOAD_DOTENV FUNCTION FROM DOTENV MODULE.
from dotenv import load_dotenv
import random


# LOADS THE .ENV FILE THAT RESIDES ON THE SAME LEVEL AS THE SCRIPT.
load_dotenv()

# GRAB THE API TOKEN FROM THE .ENV FILE.
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

#LEETCODE API
leetcode = 'https://leetcode.com/api/problems/all/'
leetcode_URL = 'https://leetcode.com/problems/'


#REQUESTING LEETCODE WEBSITE
req = requests.get(leetcode).json()




# CREATE A QUESTION CLASS
from typing import NamedTuple
class Question(NamedTuple):
	BACKEND_ID: int 			# ['stat']['question_id']
	FRONTEND_ID: int 			# ['stat']['frontend_question_id']
	TITLE: str 					# ['stat']['question__title']
	QUESTION_SLUG: str 			# ['stat']['question__slug']
	PAID: bool					# ['paid_only']
	NEW_QUESTION: bool			# ['stat'][is_new_question]
	ARTICLE_SLUG: str 			# ['stat']['question__article__slug']
	DIFFICULTY: int 			# ['difficulty']


# REFERENCE TO LEETCODE OBJECT
leetcode_object = req['stat_status_pairs']

# AN ARRAY OF QUESTION OBJECTS
array_questios = []

# A MAP OF QUESTIONS BASED ON DIFICULTY
question_difficulty = {3: [], 1:[], 2:[], 'all':[]}


# FUNCTION TO PUT OJECT IN ARRAY
def getQuestions(leetcode_object):

	for question in leetcode_object:
		q = Question(
			question['stat']['question_id'], 
			question['stat']['frontend_question_id'],
			question['stat']['question__title'],
			question['stat']['question__title_slug'],
			question['paid_only'],
			question['stat']['is_new_question'],
			question['stat']['question__article__slug'],
			question['difficulty']['level'])

		#ADD QUESTION TO AN ARRAY
		array_questios.append(q)

		#QUESTION LINK
		question_link = leetcode_URL + q.QUESTION_SLUG + '/'

		#ADD QUESTION_LINK TO ALL
		question_difficulty['all'].append(question_link)

		#ADD QUESTION_LINK BASED ON DIFFICULTY
		question_difficulty[q.DIFFICULTY].append(question_link)

		
def iterateQuestions(arr):
	for q in arr:
		for field in q:
			print(field)

		print("======")

getQuestions(leetcode_object)
#iterateQuestions(array_questios)
#print(question_difficulty)




# GETS THE CLIENT OBJECT FROM DISCORD.PY. CLIENT IS SYNONYMOUS WITH BOT.
bot = discord.Client()

# EVENT LISTENER FOR WHEN THE BOT HAS SWITCHED FROM OFFLINE TO ONLINE.
@bot.event
async def on_ready():
	# CREATES A COUNTER TO KEEP TRACK OF HOW MANY GUILDS / SERVERS THE BOT IS CONNECTED TO.
	guild_count = 0

	# LOOPS THROUGH ALL THE GUILD / SERVERS THAT THE BOT IS ASSOCIATED WITH.
	for guild in bot.guilds:
		# PRINT THE SERVER'S ID AND NAME.
		print(f"- {guild.id} (name: {guild.name})")

		# INCREMENTS THE GUILD COUNTER.
		guild_count = guild_count + 1

	# PRINTS HOW MANY GUILDS / SERVERS THE BOT IS IN.
	print("SampleDiscordBot is in " + str(guild_count) + " guilds.")



#based on difficulty
def questionDifficulty(arr):

	n = len(arr)
	number = random.randint(1, n)
	return arr[number]



# EVENT LISTENER FOR WHEN A NEW MESSAGE IS SENT TO A CHANNEL.
@bot.event
async def on_message(message):


	# CHECKS IF THE MESSAGE THAT WAS SENT IS EQUAL TO "HELLO".
	if message.content == "!problem":
		# SENDS BACK A MESSAGE TO THE CHANNEL.

		question_link_sending = questionDifficulty(question_difficulty['all'])
		await message.channel.send(question_link_sending)

	elif message.content == "!problem easy":
		question_link_sending = questionDifficulty(question_difficulty[1])
		await message.channel.send(question_link_sending)

	elif message.content == "!problem medium":
		question_link_sending = questionDifficulty(question_difficulty[2])
		await message.channel.send(question_link_sending)

	elif message.content == "!problem hard":
		question_link_sending = questionDifficulty(question_difficulty[3])
		await message.channel.send(question_link_sending)

	
	error_message = 'Message not found. Please use either one of the commands: ' + '\n' + '!problem easy, !problem medium, !problem hard'
	#await message.channel.send(error_message)



# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.
bot.run(DISCORD_TOKEN)

