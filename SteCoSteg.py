#!/usr/bin/env python

#-*- encoding:utf-8 -*-

from PIL import Image
from codecs import encode
from base64 import b64encode, b64decode

def stealth(decoy,file):
	FILE=open(file,'rb')
	bytes=[]
	print('READING FILE...')
	try:
		byte=FILE.read(1)
		while byte:
# we will save the bytes
			bytes.append(ord(byte))
			byte=FILE.read(1)
	finally:
		FILE.close()
# a color is 3 bytes, so it has to be modulo 3
		if len(bytes)%3:
			bytes.append(ord('\x00'))
		if len(bytes)%3:
			bytes.append(ord('\x00'))
	image = Image.open(decoy,'r')
	image=image.convert('RGB')
	colors={}
	print('')
	print('ANALYZING IMAGE...')
	width, height = image.size
# let's make a list of used colors
	for x in range(width):
		for y in range(height):
			try:
				colors[image.getpixel((x,y))]+=1
			except:
				colors[image.getpixel((x,y))]=1
# let's apply Schwartzian Transformation for sorting, in order to mitigate the Python's compatibility problem
	colorsList = [(item[1], item) for item in colors.items()]
	colorsList.sort()
	colorsSorted = [value[1] for value in colorsList]
	length=len(bytes)
	size=len(colorsSorted)
	if size < length:
		print('')
		print('!DECOY HAS NOT ENOUGH SPACE FOR THE FILE!')
		print('')
		exit(1)
	substitutionColors={}
# let's replace our data by the order of the least used colors
	print('')
	print('ADAPTING COLORS...')
	for i in range(int(len(bytes)/3)):
		substitutionColors[colorsSorted[i][0]]=[(bytes[i*3],bytes[i*3+1],bytes[i*3+2]),i]
# even if we shuffle the pixel/color dictionary and the key will change, the modification order is still recoverable, thus the data
	print('')
	print('CONSTRUCTING IMAGE...')
	key=[]
	for i in range(len(substitutionColors)):
		key.append((0,0))
# -2 since, hex begins with 0x
	maxLength=max(len(hex(width))-2,len(hex(height))-2)
	for x in range(width):
		for y in range(height):
			try:
				key[substitutionColors[image.getpixel((x,y))][1]]=(x,y)
				image.putpixel( (x,y), substitutionColors[image.getpixel((x,y))][0])
			except: pass
	format='png'
	image.save(file+'.'+format,format)
	print('')
	print('SAVED TO '+file+'.'+format)
	print('')
	print('GENERATING KEY...')
	print('')
# for storage optimization, we will convert the key to hex in function of the image size and then Base64
	hexes=''
	for coordinate in key:
		for value in coordinate:
# might be buggy with small images < 16 pixels
			value=str(hex(value))[2:]
			if len(value) < maxLength:
				for i in range(int(maxLength-len(value))):
					value='0'+value
			hexes+=value
	try:
# Python 2
		string=''
		for i in range(int(len(hexes)/2)):
			string+=chr(int(hexes[i*2]+hexes[i*2+1],16))
		print('KEY : '+b64encode(string))
	except:
# Python 3
		string='b\''
		for i in range(int(len(hexes)/2)):
			string+='\\x'+hexes[i*2]+hexes[i*2+1]
		string+='\''
		string=eval(string)
		print('KEY : '+str(b64encode(string))[2:-1])
	print('')

def unstealth(decoy,file):
	key=input('KEY (or recovery JPEG image) : ')
	print('')
	wasFile=False
	if len(key)>4092:
		key=input('THE KEY IS TOO LONG, SPECIFY A FILE WITH THAT KEY : ')
		print('')
		FILE=open(key,'r')
		key=''
		for line in FILE:
			key+=line
		FILE.close()
		wasFile=True
	image = Image.open(decoy,'r')
	FILE=open(file,'wb')
	width, height = image.size
	maxLength=max(len(hex(width))-2,len(hex(height))-2)
	coordinates=[]
	decoded=False
# all we need, is to get the modified pixels in good order
	try:
		if not wasFile:
			recovery = Image.open(key,'r')
			recovery=recovery.convert('RGB')
			width2, height2 = recovery.size
			if width != width2 or height != height2:
				print('')
				print('!WRONG IMAGE SIZE!')
				print('')
				exit(1)
			colors={}
			colors2={}
			print('RECOVERING KEY... may take long')
			print('')
# let's make a list of used colors for each image
			for x in range(width):
				for y in range(height):
					try:
						colors[image.getpixel((x,y))]+=1
						colors2[recovery.getpixel((x,y))]+=1
					except:
						colors[image.getpixel((x,y))]=1
						colors2[recovery.getpixel((x,y))]=1
# let's apply Schwartzian Transformation for sorting, in order to mitigate the Python's compatibility problem and make a difference between both lists by storing and appending them to coordinates in the right order
			colorsList = [(item[1], item) for item in colors.items()]
			colorsList.sort()
			colorsSorted = [value[1] for value in colorsList]
			colors2List = [(item[1], item) for item in colors2.items()]
			colors2List.sort()
			colors2Sorted = [value[1] for value in colors2List]
			difference=list(set(colorsSorted)-set(colors2Sorted))
#			for value in range(int(len(difference))):
#				difference[value]=difference[value][0]
			total=len(difference)
			for pixel in colors2Sorted:
                                 if total == 0:
                                         break
                                 total-=1
                                 for x in range(width):
                                         for y in range(height):
                                                 if recovery.getpixel((x,y))==pixel[0]:
                                                         coordinates.append((x,y))
			decoded=True
	except:
		pass
	if not decoded:
# Base64 decoding
		try:
# Python 2
			key=b64decode(key).encode('hex')
		except:
# Python 3
			key=str(encode(b64decode(key),'hex'))[2:-1]
		for i in range(int(len(key)/maxLength/2)):
			coordinates.append((int(key[i*maxLength*2]+key[i*maxLength*2+1]+key[i*maxLength*2+2],16),int(key[i*maxLength*2+3]+key[i*maxLength*2+4]+key[i*maxLength*2+5],16)))
	print('CONSTRUCTING FILE...')
	print('')
	for coordinate in coordinates:
# because, tuplet and bytes difference
		try:
# Python 2
			FILE.write(chr(image.getpixel(coordinate)[0]))
			FILE.write(chr(image.getpixel(coordinate)[1]))
			FILE.write(chr(image.getpixel(coordinate)[2]))
		except:
# Python 3
			FILE.write(bytes([image.getpixel(coordinate)[0]]))
			FILE.write(bytes([image.getpixel(coordinate)[1]]))
			FILE.write(bytes([image.getpixel(coordinate)[2]]))
	image.close()
	FILE.close()
	print('SAVED TO '+file)
	print('')

# some style in purple
print("\033[35m")
print('')
print('  	                 |         ')
print('  	                / \        ')
print('  	               //V\\\       ')
print('  	              / \|/ \      ')
print('  	             /=/ v \=\     ')
print('  	            /         \    ')
print('  	           /           \   ')
print('  	          /             \  ')
print('  	         /   /|     |\   \ ')
print('  	        /   / \\\   // \   \\')
print('  	        \  /   \\\ //   \  /')
print('  	         \/   / \ / \   \/ ')
print('  	             / / V \ \     ')
print('  	            |_/     \_|    ')
print('')
print('   _____ _        _____      _____ _             ')
print('  / ____| |      / ____|    / ____| |            ')
print(' | (___ | |_ ___| |     ___| (___ | |_ ___  __ _ ')
print('  \___ \| __/ _ \ |    / _ \\\___ \| __/ _ \/ _` |')
print('  ____) | ||  __/ |___| (_) |___) | ||  __/ (_| |')
print(' |_____/ \__\___|\_____\___/_____/ \__\___|\__, |')
print('                                            __/ |')
print('                                           |___/ ')
print('')
print('           Stealth Colors Steganography')
print('')

# since, input functions varie in Python 2 and 3, we have to find the good-one
try:
	input=raw_input
except NameError: pass

decoy=input('INPUT IMAGE (JPEG to stealth and PNG to unstealth): ')
# GIF is possible, but can be buggy for recovery
print('')
file=input('FILE (input to stealth and output to unstealth): ')
print('')
image=Image.open(decoy,'r')
format=image.format
format=format.lower()
if format == 'png':
	unstealth(decoy,file)
elif format == 'jpeg':
	stealth(decoy,file)
else:
	print('!WRONG IMAGE FORMAT!')
	print('')
	exit(1)
