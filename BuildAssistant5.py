# ------- TO DO -------

# "Cancel" after adding champs/items still adds them
# Synergies don't have icons
# Scroll wheel clicks things
# Color-code synergies?
# Scan for items while playing (click to toggle in the meantime?)
	# Check mark for obtained



# -------------------------- LIBRARIES --------------------------

import time
import pygame, sys
import pygame.gfxdraw
from pygame.locals import *
import json
import os


# -------------------------- CLEAR CONSOLE --------------------------

#import os
os.system('cls' if os.name == 'nt' else 'clear')
print("")



# -------------------------- INITIALIZE -------------------------- 

pygame.init()
frameRate = 30
winX = 640
winY = 880
win = pygame.display.set_mode((winX, winY), 0, 32)
pygame.display.set_caption('Build Monitor')
FPSCLOCK = pygame.time.Clock()

BLACK = (0, 0, 0)
DGREY = (50, 50, 50)
GREY = (100, 100, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
COST1 = (57, 77, 90)
COST2 = (8, 146, 16)
COST3 = (16, 121, 214)
COST4 = (189, 20, 214)
COST5 = (214, 166, 16)
ARIAL_12 = pygame.font.SysFont('Arial', 12)
text12Height = 10
ARIAL_18 = pygame.font.SysFont('Arial', 18)
text18Height = 32



# -------------------------- DATA --------------------------

buildList = []

set_folder = 'set5'

# Read build list
textLocation = os.path.join(set_folder, 'buildList.txt')
if not os.path.exists(textLocation):
	with open(textLocation, 'w') as newTXTbuilds:
		pass
with open(textLocation, 'r') as TXTbuilds:
	for index, line in enumerate(TXTbuilds):
		buildList.append(line.rstrip())

# Read build JSON
jsonLocation = os.path.join(set_folder, 'builds.json')
if not os.path.exists(jsonLocation):
	with open(jsonLocation, 'w') as newJSONbuilds:
		pass
with open(jsonLocation) as JSONbuilds:
	builds = json.load(JSONbuilds)
# Read champion JSON
jsonLocation = os.path.join(set_folder, 'champions.json')
with open(jsonLocation) as JSONchampions:
	champions = json.load(JSONchampions)
for index,value in enumerate(champions):
	if value['name'] == 'Target Dummy':
		champions.pop(index)
# Read item JSON
jsonLocation = os.path.join(set_folder, 'items.json')
with open(jsonLocation) as JSONitems:
	items = json.load(JSONitems)
for index,value in reversed(list(enumerate(items))):
	if value['id'] > 99:
		items.pop(index)
full_items = list(filter(lambda value: value['id'] >= 10, items))


# -------------------------- FUNCTIONS -------------------------- 

def readJSON():
	buildList = []
	# Read build list
	textLocation = os.path.join(set_folder, 'buildList.txt')
	with open(textLocation, 'r') as TXTbuilds:
		for index, line in enumerate(TXTbuilds):
			buildList.append(line.rstrip())

	# Read build JSON
	jsonLocation = os.path.join(set_folder, 'builds.json')
	with open(jsonLocation) as JSONbuilds:
		builds = json.load(JSONbuilds)
	# Read champion JSON
	jsonLocation = os.path.join(set_folder, 'champions.json')
	with open(jsonLocation) as JSONchampions:
		champions = json.load(JSONchampions)
	# Read item JSON
	jsonLocation = os.path.join(set_folder, 'items.json')
	with open(jsonLocation) as JSONitems:
		items = json.load(JSONitems)
	
	return(buildList, builds, champions, items)


def saveToJSON():
	textLocation = os.path.join(set_folder, 'buildList.txt')
	with open(textLocation, 'w') as outputFile:
		for i in buildList:
			outputFile.write(i)
			outputFile.write('\n')
	jsonLocation = os.path.join(set_folder, 'builds.json')
	with open(jsonLocation, 'w') as JSONbuilds:
		json.dump(builds, JSONbuilds)

def checkShopping(activeBuild):
	buildData = next((item for item in builds if item["name"] == activeBuild),None)
	shoppingList = {}
	for champion in buildData["carries"]:
		for j in buildData["carries"][champion]:
			for k in str(j):
				if k in shoppingList:
					shoppingList[k] += 1
				else:
					shoppingList[k] = 1
	shoppingSorted = {key: value for key, value in sorted(shoppingList.items(), key=lambda k: k[1], reverse=True)}
	return(shoppingSorted)



def drawText(text, textColor, textSize, posX, posY):
	font = pygame.font.SysFont('Arial', textSize)
	win.blit(font.render(text, True, textColor),font.render(text, True, textColor).get_rect(topleft=(posX, posY)))

def drawTextBlock(text, textColor, textSize, boxColor, boxPosX, boxPosY, boxSizeX=winX, boxSizeY=text18Height):
	font = pygame.font.SysFont('Arial', textSize)
	pygame.draw.rect(win, boxColor, [boxPosX, boxPosY, boxSizeX, boxSizeY])
	win.blit(font.render(text, True, textColor),font.render(text, True, textColor).get_rect(center=(boxPosX+boxSizeX/2, boxPosY+boxSizeY/2)))

def drawMinusButton(iconRadius, iconCenterX, iconCenterY):
	pygame.draw.circle(win, RED, (int(iconCenterX),int(iconCenterY)), iconRadius)
	pygame.draw.rect(win, WHITE, [iconCenterX-iconRadius/2, iconCenterY-2, iconRadius*1.2, iconRadius/2])

def drawPlusButton(iconRadius, iconCenterX, iconCenterY):
	plusThickness = 0.2
	plusLength = 0.75
	pygame.draw.circle(win, WHITE, (int(iconCenterX),int(iconCenterY)), int(iconRadius))
	pygame.draw.rect(win, BLACK, [iconCenterX-iconRadius*plusLength, iconCenterY-iconRadius*plusThickness+1, iconRadius*plusLength*2, iconRadius*plusThickness*2])
	pygame.draw.rect(win, BLACK, [iconCenterX-iconRadius*plusThickness, iconCenterY-iconRadius*plusLength, iconRadius*plusThickness*2, iconRadius*plusLength*2])

def drawArrow(activeFlag, sizeX, sizeY, iconPointX, iconPointY):
	color = WHITE if activeFlag else DGREY
	pygame.draw.rect(win, color, [iconPointX-sizeX, iconPointY-sizeY/6, sizeX-sizeY, sizeY/3])
	pygame.draw.polygon(win, color, ((iconPointX, iconPointY), (iconPointX-sizeY, iconPointY+sizeY/2), (iconPointX-sizeY, iconPointY-sizeY/2)))

def imagePathChamp(champName):
	champPrefix = "TFT" + set_folder.replace("set", '') + "_"
	champName = champName.replace(' ', '').replace("'", '').split("_")
	fileName = champPrefix + "{0}.png".format(champName[-1])
	return os.path.join(set_folder, 'champions', fileName)

def imagePathItem(itemID):
	if itemID < 10:
		fileName = "0{0}.png".format(itemID)
	else:
		fileName = "{0}.png".format(itemID)
	return os.path.join(set_folder,'items', fileName)

def drawChampionIcon(champion, cost, activeFlag, boxPosX, boxPosY, boxSize=64):
	borderThickness = 3
	if champion != None:
		if cost != 0:
			if cost == 1:
				costColor = COST1
			if cost == 2:
				costColor = COST2
			if cost == 3:
				costColor = COST3
			if cost == 4:
				costColor = COST4
			if cost >= 5:
				costColor = COST5
			pygame.draw.rect(win, costColor, [boxPosX-borderThickness, boxPosY-borderThickness, boxSize+borderThickness*2, boxSize+borderThickness*2])
		try:
			icon = pygame.image.load(imagePathChamp(champion))
		except:
			print(champion)
		icon = pygame.transform.scale(icon, (64, 64))
		win.blit(icon, (boxPosX, boxPosY))
		if not activeFlag:
			darkenImage(icon, boxPosX, boxPosY)
	else:
		pygame.draw.rect(win, WHITE, [boxPosX-borderThickness, boxPosY-borderThickness, boxSize+borderThickness*2, boxSize+borderThickness*2])
		pygame.draw.rect(win, BLACK, [boxPosX, boxPosY, boxSize, boxSize])
		drawPlusButton(boxSize/3, boxPosX+boxSize/2, boxPosY+boxSize/2)

def drawItemIcon(item, activeFlag, posX, posY, size=32):
	if item != None:
		icon = pygame.image.load(imagePathItem(item))
		resizedIcon = pygame.transform.scale(icon, (size, size))
		win.blit(resizedIcon, (posX, posY))
		if not activeFlag:
			darkenImage(resizedIcon, posX, posY)
	else:
		drawPlusButton(size/2, posX+size/2, posY+size/2)

def darkenImage(imageName, x, y):
	darkenPercentage = 0.7
	dark = pygame.Surface(imageName.get_size()).convert_alpha()
	dark.fill((0, 0, 0, darkenPercentage*255))
	win.blit(dark, (x, y))
	




def deleteBuild(selectedBuild):
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					return()
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouseX, mouseY = pygame.mouse.get_pos()
				if mouseY > winY-text18Height:
					# Delete
					if mouseX > winX/2:
						del buildList[selectedBuild]
						del builds[selectedBuild]
						saveToJSON()
						return()
					# Cancel
					else:
						return()
		
		win.fill(BLACK)
		
		# Draw "Delete build?" instruction
		drawTextBlock("Delete build?", WHITE, 18, RED, 0, 0)
		# Draw build name
		drawTextBlock(buildList[selectedBuild], WHITE, 18, BLACK, winX/3, winY/3+text18Height*selectedBuild, winX/3, text18Height-2)
		# Draw [Delete] button
		drawTextBlock("[Delete]", RED, 18, BLACK, winX/2, winY-text18Height, winX/2, text18Height)
		# Draw [Cancel] button
		drawTextBlock("[Cancel]", BLACK, 18, RED, 0, winY-text18Height, winX/2, text18Height)

		pygame.display.update()
		FPSCLOCK.tick(frameRate)


def editBuildName(selectedBuild):
	cursor = 1
	nameString = buildList[selectedBuild]
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				# Apply
				if event.key == pygame.K_RETURN:
					buildList[selectedBuild] = nameString
					builds[selectedBuild]["name"] = nameString
					saveToJSON()
					return()
				# Escape
				elif event.key == pygame.K_ESCAPE:
					return()
				# Backspace
				elif event.key == pygame.K_BACKSPACE:
					nameString = nameString[:-1]
				# Other keys
				elif event.unicode.isalnum():
					if len(nameString) < 26:
						nameString += event.unicode
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouseX, mouseY = pygame.mouse.get_pos()
				if mouseY > winY-text18Height:
					# Apply
					if mouseX > winX/2:
						buildList[selectedBuild] = nameString
						builds[selectedBuild]["name"] = nameString
						saveToJSON()
						return()
					# Cancel
					else:
						return()
		
		win.fill(BLACK)
		
		# Draw "Edit name" instruction
		drawTextBlock("Edit name:", WHITE, 18, BLACK, 0, 0)
		# Draw build name
		pygame.draw.rect(win, BLUE, [winX/3, winY/3+text18Height*selectedBuild, winX/3, text18Height-2])
		if cursor <= frameRate/2:
			nameStringPlus = nameString
		else:
			nameStringPlus = nameString + '|'
		win.blit(ARIAL_18.render(nameStringPlus, True, WHITE),ARIAL_18.render(nameString, True, WHITE).get_rect(center=(winX/2, winY/3+text18Height*(selectedBuild+0.5)-1)))
		# Draw [Apply] button
		drawTextBlock("[Apply]", BLACK, 18, GREEN, winX/2, winY-text18Height, winX/2, text18Height)
		# Draw [Cancel] button
		drawTextBlock("[Cancel]", BLACK, 18, RED, 0, winY-text18Height, winX/2, text18Height)
		
		cursor += 1
		if cursor > frameRate:
			cursor = 1
			
		pygame.display.update()
		FPSCLOCK.tick(frameRate)


def addBuild():
	cursor = 1
	nameString = ''
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				# Apply
				if event.key == pygame.K_RETURN:
					buildList.append(nameString)
					builds.append({"name": nameString, "champions": [], "carries": {}})
					saveToJSON()
					return()
				# Escape
				elif event.key == pygame.K_ESCAPE:
					return()
				# Backspace
				elif event.key == pygame.K_BACKSPACE:
					nameString = nameString[:-1]
				# Other keys
				elif event.unicode.isalnum():
					if len(nameString) < 26:
						nameString += event.unicode
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouseX, mouseY = pygame.mouse.get_pos()
				if mouseY > winY-text18Height:
					# Apply
					if mouseX > winX/2:
						buildList.append(nameString)
						builds.append({"name": nameString, "champions": [], "carries": {}})
						saveToJSON()
						return()
					# Cancel
					else:
						return()
		
		win.fill(BLACK)
		
		# Draw "Type name" instruction
		drawTextBlock("Type name:", WHITE, 18, BLACK, 0, 0)
		# Draw build name
		pygame.draw.rect(win, BLUE, [winX/3, winY/3+text18Height*len(buildList), winX/3, text18Height])
		if cursor <= frameRate/2:
			nameStringPlus = nameString
		else:
			nameStringPlus = nameString + '|'
		win.blit(ARIAL_18.render(nameStringPlus, True, WHITE),ARIAL_18.render(nameString, True, WHITE).get_rect(center=(winX/2, winY/3+text18Height*(len(buildList)+0.5))))
		# Draw [Add] button
		drawTextBlock("[Add]", BLACK, 18, GREEN, winX/2, winY-text18Height, winX/2, text18Height)
		# Draw [Cancel] button
		drawTextBlock("[Cancel]", BLACK, 18, RED, 0, winY-text18Height, winX/2, text18Height)
		
		cursor += 1
		if cursor > frameRate:
			cursor = 1
		pygame.display.update()
		FPSCLOCK.tick(frameRate)


def editBuildList():
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					return
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouseX, mouseY = pygame.mouse.get_pos()
				if mouseY > winY-text18Height:
					return()
				for i in range(len(buildList)):
					# "Build" row
					if mouseY > winY/3+text18Height*i and mouseY < winY/3+text18Height*(i+1):
						# "Delete" column
						if mouseX > winX/4-10 and mouseX < winX/4+10:
							deleteBuild(i)
						# "Name" column
						elif mouseX > winX/3 and mouseX < winX*2/3:
							editBuildName(i)
					# "Add" button
					elif mouseY > winY/3+text18Height*len(buildList) and mouseY < winY/3+text18Height*(len(buildList)+1) and mouseX > winX/4-10 and mouseX < winX/4+10:
						if len(buildList) < 10:
							addBuild()
						
						
		win.fill(BLACK)
		
		# Draw "Edit build" instruction
		drawTextBlock("Edit a build:", WHITE, 18, BLACK, 0, 0)
		# Draw build list
		for i in range(len(buildList)):
			# Build name
			drawTextBlock(buildList[i], WHITE, 18, BLUE, winX/3, winY/3+text18Height*i, winX/3, text18Height-2)
			# Delete button
			drawMinusButton(9, winX/4, winY/3+text18Height*(i+0.5))
		# Add button
		if len(buildList) < 10:
			drawPlusButton(9, winX/4, winY/3+text18Height*(len(buildList)+0.5))
		# Draw [Done editing] button
		drawTextBlock("[Done editing]", BLACK, 18, GREEN, 0, winY-text18Height)

		pygame.display.update()
		FPSCLOCK.tick(frameRate)




def selectScreen():
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouseX, mouseY = pygame.mouse.get_pos()
				if mouseY > winY-text18Height:
					editBuildList()
				for i in range(len(buildList)):
					if mouseY > winY/3+text18Height*i and mouseY < winY/3+text18Height*(i+1):
						return(buildList[i])
						
		win.fill(BLACK)
		
		# Draw "Select build" instruction
		drawTextBlock("Select your build:", WHITE, 18, BLACK, 0, 0)
		# Draw build list
		for i in range(len(buildList)):
			drawTextBlock(buildList[i], WHITE, 18, BLUE, 0, winY/3+text18Height*i, winX, text18Height-2)
		# Draw [Edit builds] button
		drawTextBlock("[Edit builds]", BLACK, 18, GREY, 0, winY-text18Height)
		
		pygame.display.update()
		FPSCLOCK.tick(frameRate)





def selectItem(activeBuild, activeChampion, itemSlot):
	rowHeight = 88
	colWidth = 96
	buildData = next((item for item in builds if item["name"] == activeBuild),None)
	activeChampion = buildData["champions"][activeChampion]
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					return
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouseX, mouseY = pygame.mouse.get_pos()
				if mouseY > text18Height and mouseY < winY-text18Height:
					row = 0
					column = 0
					for itemIndex in range(len(full_items)):
						if column > 5:
							column = 0
							row += 1
						if (mouseX-24)//colWidth == column and (mouseY-24)//rowHeight == row:
							# Append item
							if full_items[itemIndex]["id"] not in buildData["carries"][activeChampion]:
								if itemSlot < len(buildData["carries"][activeChampion]):
									buildData["carries"][activeChampion][itemSlot] = full_items[itemIndex]["id"]
								else:
									buildData["carries"][activeChampion].append(full_items[itemIndex]["id"])
							# Swap items
							else:
								i = buildData["carries"][activeChampion].index(full_items[itemIndex]["id"])
								buildData["carries"][activeChampion][i],buildData["carries"][activeChampion][itemSlot] = buildData["carries"][activeChampion][itemSlot],buildData["carries"][activeChampion][i]
							return()
						column += 1
				if mouseY > winY-text18Height:
					# Remove
					if mouseX > winX/2:
						if itemSlot < len(buildData["carries"][activeChampion]):
							del buildData["carries"][activeChampion][itemSlot]
						return()
						#buildData["carries"][activeChampion][itemSlot] = None
						
					# Cancel
					else:
						return()
	
		win.fill(BLACK)
		
		# Draw "Select item:" button
		drawTextBlock("Select item:", WHITE, 18, BLACK, 0, 0)
		# Draw item grid
		row = 0.5
		column = 0
		lastCost = 1
		for index in range(len(full_items)):
			if column > 5:
				column = 0
				row += 1
			# Item Icon
			drawItemIcon(full_items[index]["id"], True, colWidth*column+60, rowHeight*row)
			# Item Name
			drawTextBlock(full_items[index]["name"], WHITE, 12, BLACK, colWidth*column+40, rowHeight*row+40, 64, 12)
			# Increment
			column += 1
		# Draw [Remove] button
		drawTextBlock("[Remove]", BLACK, 18, RED, winX/2, winY-text18Height, winX/2, text18Height)
		# Draw [Cancel] button
		drawTextBlock("[Cancel]", WHITE, 18, BLACK, 0, winY-text18Height, winX/2, text18Height)

		
		pygame.display.update()
		FPSCLOCK.tick(frameRate)





def selectChampion(activeBuild, championSlot):
	rowHeight = 88
	colWidth = 80
	championsByCost = sorted(champions, key=lambda k: k['cost'])
	
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					return
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouseX, mouseY = pygame.mouse.get_pos()
				if mouseY > text18Height and mouseY < winY-text18Height:
					row = 0
					column = 0
					for index in range(len(championsByCost)):
						if column > 7 or championsByCost[index]["cost"] > lastCost:
							column = 0
							row += 1
							lastCost = championsByCost[index]["cost"]
						if (mouseX)//colWidth == column and (mouseY-41)//rowHeight == row:
							buildData = next((item for item in builds if item["name"] == activeBuild),None)
							# Append champion
							if championsByCost[index]["name"] not in buildData["champions"]:
								if championSlot < len(buildData["champions"]):
									buildData["champions"][championSlot] = championsByCost[index]["name"]
								else:
									buildData["champions"].append(championsByCost[index]["name"])
							# Swap champions
							else:
								i = buildData["champions"].index(championsByCost[index]["name"])
								buildData["champions"][i],buildData["champions"][championSlot] = buildData["champions"][championSlot],buildData["champions"][i]
							return()
						column += 1
				if mouseY > winY-text18Height:
					# Remove
					if mouseX > winX/2:
						buildData = next((item for item in builds if item["name"] == activeBuild),None)
						if championSlot < len(buildData["champions"]):
							del buildData["champions"][championSlot]
						return()
						#buildData["champions"][championSlot] = None
						
					# Cancel
					else:
						return()
	
		win.fill(BLACK)
		
		# Draw "Select champion:" button
		drawTextBlock("Select champion:", WHITE, 18, BLACK, 0, 0)
		# Draw champion grid
		row = 0.5
		column = 0
		lastCost = 1
		for index in range(len(championsByCost)):
			if "Dummy" in championsByCost[index]["championId"] or "Training" in championsByCost[index]["championId"] or "Void" in championsByCost[index]["championId"] or "Emblem" in championsByCost[index]["championId"] or "Dragon" in championsByCost[index]["championId"] or "Egg" in championsByCost[index]["championId"]:
				continue
			if column > 7 or championsByCost[index]["cost"] > lastCost:
				column = 0
				row += 1
				lastCost = championsByCost[index]["cost"]
			# Champion Icon
			drawChampionIcon(championsByCost[index]["championId"], championsByCost[index]["cost"], True, colWidth*column+8, rowHeight*row)
			# Champion Name
			drawTextBlock(championsByCost[index]["name"], WHITE, 12, BLACK, colWidth*column+8, rowHeight*row+68, 64, 12)
			# Increment
			column += 1
		# Draw [Remove] button
		drawTextBlock("[Remove]", BLACK, 18, RED, winX/2, winY-text18Height, winX/2, text18Height)
		# Draw [Cancel] button
		drawTextBlock("[Cancel]", WHITE, 18, BLACK, 0, winY-text18Height, winX/2, text18Height)
		
		pygame.display.update()
		FPSCLOCK.tick(frameRate)



def editBuild(activeBuild):
	global buildList,builds,champions,items
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				# Apply
				if event.key == pygame.K_RETURN:
					return()
				# Escape
				elif event.key == pygame.K_ESCAPE:
					return()
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouseX, mouseY = pygame.mouse.get_pos()
				buildData = next((item for item in builds if item["name"] == activeBuild),None)
				# Change build
				if mouseY < text18Height:
					return
				# Select row
				elif mouseY < winY-text18Height:
					for row in range(len(buildData["champions"])+1):
						if mouseY > (row+1)*80 and mouseY < (row+2)*80-16:
							# Select champion
							if mouseX > winX/3 and mouseX < winX/3+64:
								selectChampion(activeBuild, row)
							# Toggle carry
							elif mouseX > winX*2/3-48 and mouseX < winX*2/3-24:
								if buildData["champions"][row] in buildData["carries"]:
									buildData["carries"].pop(buildData["champions"][row])
								else:
									buildData["carries"][buildData["champions"][row]] = []
							# Select item
							elif mouseX > winX*2/3+(0*80): #and mouseX < winX*2/3+(2*80):
								if buildData["champions"][row] in buildData["carries"]:
									for column in range(len(buildData["carries"][buildData["champions"][row]])+1):
										if mouseX > winX*2/3+(column*80) and mouseX < winX*2/3+((column+1)*80):
											selectItem(activeBuild, row, column)
				elif mouseY > winY-text18Height:
					# Apply
					if mouseX > winX/2:
						delChamps = []
						for champ in buildData["carries"]:
							if champ not in buildData["champions"]:
								delChamps.append(champ)
						for champ in delChamps:
							buildData["carries"].pop(champ)
						saveToJSON()
						return()
					# Cancel
					else:
						buildList,builds,champions,items = readJSON()
						return()
	
		win.fill(BLACK)
		
		# Draw build name
		drawTextBlock(activeBuild, WHITE, 18, BLACK, 0, 0)
		# Draw "Select component to edit" instruction
		drawTextBlock("Select component to edit", BLACK, 18, BLUE, 0, text18Height)
		# Draw components
		row = 1
		rowHeight = 80
		buildData = next((item for item in builds if item["name"] == activeBuild),None)
		for champion in buildData["champions"]:
			if champion:
				# Champion Icon
				champData = next((item for item in champions if item["name"] == champion),None)
				drawChampionIcon(champion, champData["cost"], True, winX/3, rowHeight*row)
				# Champion Name
				drawText(champion, DGREY, 18, winX/3+64+16, rowHeight*row+(rowHeight/3))
				# Selected Carries
				if champion in buildData["carries"]:
					drawArrow(True, 20, 12, winX*2/3-24, rowHeight*row+(rowHeight/3)+12)
				else:
					drawArrow(False, 20, 12, winX*2/3-24, rowHeight*row+(rowHeight/3)+12)
				# Champion Items
				if champion in buildData["carries"]:
					buildColumn = 0
					for j in buildData["carries"][champion]:
						drawItemIcon(j, True, winX*2/3+(buildColumn*80), rowHeight*row)
						# Item Components
						subColumn = -1
						for k in str(j):
							drawItemIcon(int(k), False, winX*2/3+(buildColumn*80)+(subColumn*16), rowHeight*row+rowHeight/2, 24)
							subColumn = subColumn*(-1)
						buildColumn += 1
					if len(buildData["carries"][champion]) < 3:
						drawItemIcon(None, True, winX*2/3+(buildColumn*80), rowHeight*row)
				# Champion Synergies
				champData = next((item for item in champions if item["name"] == champion),None)
				synergyColumn = 0
				synergyPrefix = set_folder.capitalize() + "_"
				for j in champData["traits"]:
					j = j.replace(synergyPrefix, '')
					drawText(j, DGREY, 12, 12+synergyColumn*60, rowHeight*row+(rowHeight/6)+synergyColumn*12)
					synergyColumn += 1
				# Increment
			else:
				drawChampionIcon(champion, champData["cost"], True, winX/3, rowHeight*row)
			row += 1
		# Add champion button
		if row < 10:
			drawChampionIcon(None, 0, True, winX/3, rowHeight*row)
		# Draw [Apply] button
		drawTextBlock("[Apply]", BLACK, 18, GREEN, winX/2, winY-text18Height, winX/2, text18Height)
		# Draw [Cancel] button
		drawTextBlock("[Cancel]", BLACK, 18, RED, 0, winY-text18Height, winX/2, text18Height)

		
		pygame.display.update()
		FPSCLOCK.tick(frameRate)



def recipeScreen(activeBuild):
	buildData = next((item for item in builds if item["name"] == activeBuild),None)

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					return
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouseX, mouseY = pygame.mouse.get_pos()
				if mouseY < text18Height*2:
					return
				if mouseY > winY-text18Height:
					editBuild(activeBuild)
	
		win.fill(BLACK)
		
		# Draw build name
		drawTextBlock(activeBuild, WHITE, 18, BLACK, 0, 0)
		# Draw [CHANGE BUILD] button
		drawTextBlock("[Change build]", BLACK, 18, BLUE, 0, text18Height)
		row = 1
		rowHeight = 80
		for champion in buildData["champions"]:
			if champion:
				# Champion Icon
				champData = next((item for item in champions if item["name"] == champion),None)
				drawChampionIcon(champion, champData["cost"], True, winX/3, rowHeight*row)
				# Champion Name
				drawText(champion, WHITE, 18, winX/3+64+16, rowHeight*row+(rowHeight/3))
				# Champion Items
				if champion in buildData["carries"]:
					buildColumn = 0
					for j in buildData["carries"][champion]:
						drawItemIcon(j, True, winX*2/3+(buildColumn*80), rowHeight*row)
						# Item Components
						subColumn = -1
						for k in str(j):
							drawItemIcon(int(k), True, winX*2/3+(buildColumn*80)+(subColumn*16), rowHeight*row+rowHeight/2, 24)
							subColumn = subColumn*(-1)
						buildColumn += 1
				# Champion Synergies
				champData = next((item for item in champions if item["name"] == champion),None)
				synergyColumn = 0
				synergyPrefix = set_folder.capitalize() + "_"
				for j in champData["traits"]:
					j = j.replace(synergyPrefix, '')
					drawText(j, WHITE, 12, 12+synergyColumn*60, rowHeight*row+(rowHeight/6)+synergyColumn*12)
					synergyColumn += 1
				# Increment
			row += 1
		# Draw shopping list
		shoppingList = checkShopping(activeBuild)
		shoppingColumn = 0
		for item, qty in shoppingList.items():
			drawItemIcon(int(item), True, 40+(shoppingColumn*40), 800, 24)
			drawTextBlock(str(qty), WHITE, 12, BLACK, 40+(shoppingColumn*40), 830, 24, text12Height)
			shoppingColumn += 1
		# Draw [Edit build] button
		drawTextBlock("[Edit build]", BLACK, 18, GREY, 0, winY-text18Height)
		
		pygame.display.update()
		FPSCLOCK.tick(frameRate)


	


# -------------------------- MAIN --------------------------

def main():
	while True:
		recipeScreen(selectScreen())

main()





