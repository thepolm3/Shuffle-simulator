import Shuffles
import os
import numpy as np
import time
import cv2
from datetime import datetime

DECK_SIZE = 52
NUMBER_OF_SHUFFLES = 40

PIXELS_PER_CARD = 10
IMG_WIDTH = DECK_SIZE * PIXELS_PER_CARD
IMG_HEIGHT = IMG_WIDTH
VERBOSITY = 1
VERBOSE_TIME = ("%Y-%m-%d %H:%M:%S   ","%H:%M:%S","%M:%S.%f", "%S.%f>")

TEXT_STYLE = 	{"fontFace"		: cv2.FONT_HERSHEY_SIMPLEX,
				"color" : (255, 255, 255),
				"fontScale" : 1,
				"lineType"	: 10}

#				Name 		Shuffle Function	FPS 	shuffles					Color
shuffles = ((	"overhand",	Shuffles.overhand,	10,		NUMBER_OF_SHUFFLES,			(230, 0, 0)),
			(	"riffle",	Shuffles.riffle,	60,		NUMBER_OF_SHUFFLES,			(0, 230, 0)),
			(	"smoosh",	Shuffles.corgi,		60,		NUMBER_OF_SHUFFLES,			(0, 0, 230)))

def get_text_dimensions(text):
	return cv2.getTextSize(str(text), TEXT_STYLE["fontFace"], TEXT_STYLE["fontScale"], TEXT_STYLE["lineType"])[0]

def create_dirs(path):
	if not os.path.exists(path):
		os.makedirs(path)

def color_map(item, max, color):
	return np.array(color)*(item/max)

def log(message, level = 1):
	if level > VERBOSITY:
		return 

	with open("Logs/log.txt", "a+") as log:
		ts = time.gmtime()
		message = '\t'*(level-1) + f'[{datetime.utcnow().strftime(VERBOSE_TIME[level - 1])[:-3]}] {message}\n'
		log.write(message)
		print(message, end = '')


try:
	import matplotlib.pyplot as plt
except Exception as error:
	log('Could not load matplotlib, No graphs will be created')
	log(error)
	plt = None

if plt:
	plt.figure(1)
	plt.ylim((0,1))
	ax = plt.subplot()
	ax.set_xlabel('Number Of Shuffles')
	ax.set_ylabel('Correlation Of Start Deck to Shuffled Deck')

width, height = DECK_SIZE * PIXELS_PER_CARD, IMG_HEIGHT



blank_deck = list(range(DECK_SIZE))

log(f'''*Program Begins
	DECK_SIZE:{DECK_SIZE}
	NUMBER_OF_SHUFFLES:{NUMBER_OF_SHUFFLES}
	IMG_DIMENSIONS:{IMG_WIDTH}x{IMG_HEIGHT}''')
for name, shuffle, fps, number_of_shuffles, color in shuffles:

	plotpath = f"Plots/{name}_correlations.png"
	datapath = f'Data/{name}.txt'
	imgpath = f'Shuffles/{name}/'
	videopath = f'Video/{name}.mp4v'

	open(datapath,'w+').close()	
	create_dirs(imgpath)

	log('Creating video object', 2)
	fourcc = cv2.VideoWriter_fourcc(*'mp4v')
	out = cv2.VideoWriter(videopath, fourcc, fps, (width, height), isColor = True)
	nframes = 0
	correlation = 1
	correlations = []

	deck = blank_deck.copy()

	for n in range(number_of_shuffles):

		log(f'Starting {name} shuffle {n}', 3)
		for deck in shuffle(deck, generator = True):

			img = np.zeros((height,width,3), np.uint8)
			text_w, text_h = get_text_dimensions(f'{correlation:.5f}')

			for i in range(DECK_SIZE):

				log(f'Creating column {i} of pixels', 4)
				pixel = PIXELS_PER_CARD*i
				r, g, b = color_map(deck[i], DECK_SIZE, color)
				img[:, pixel:pixel + PIXELS_PER_CARD] = (b, g, r)

			log('Adding text to frame', 3)
			cv2.putText(img, f"{n+1}", (10,IMG_HEIGHT - 10), **TEXT_STYLE)
			cv2.putText(img, f"{correlation:.5f}", (IMG_WIDTH - text_w - 10,IMG_HEIGHT - 10), **TEXT_STYLE)

			nframes += 1
			log(f'created frame {nframes}', 3)
			out.write(img)
			log(f'wrote frame {nframes}', 3)

		log(f'Finished {name} shuffle {n}', 2)
		
		correlation = abs(np.corrcoef(blank_deck,deck)[0,1])
		correlations.append(correlation)


		log(f'Writing shuffled deck to {datapath}', 2)
		with open(datapath,"a") as f:

			fill = len(str(DECK_SIZE))
			f.write(",".join(f'{i:0{fill}}' for i in deck) + "\n")
		
		log(f'outputting image to {imgpath}', 2)
		fill = len(str(number_of_shuffles))
		cv2.imwrite(f'{imgpath}{n+1:0{fill}}.png', img)

	log(f'Creating {videopath}', 1)
	out.release()
	cv2.destroyAllWindows()

	if plt:
		log(f'Adding {name} to correlation graph', 1)
		plt.figure(1)
		ax.plot(range(len(correlations)), correlations, color = color_map(1, 255, color), label = f'{name}')#


		log(f'Saving plot to {plotpath}', 1)
		plt.figure(name)
		ax2 = plt.subplot()
		ax2.plot(range(len(correlations)), correlations, color = color_map(1, 255, color))
		plt.ylim((0,1))
		plt.rcParams["figure.figsize"] = (8,8)
		plt.savefig(plotpath)

if plt:
	plotpath = "Plots/shuffle_correlations.png"
	log(f'Saving final plot to {plotpath}', 1)
	plt.figure(1)
	ax.legend(bbox_to_anchor = (1.05, 1), loc = 2, borderaxespad = 0.)
	plt.tight_layout()
	plt.rcParams["figure.figsize"] = (8,8)
	plt.savefig(plotpath)
		