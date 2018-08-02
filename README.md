# Shuffle-simulator
Analysis of different kinds of shuffles

# Links
view the shuffles here:
* [Overhand](https://gfycat.com/WaryAcceptableAngelfish)
* [Riffle](https://gfycat.com/ForsakenDisfiguredChimpanzee)
* [Smoosh](https://gfycat.com/CraftyShinyAyeaye)

View the correlation graphs [here](https://imgur.com/gallery/GONMHJo)

# Files
Shuffles.py contains three shuffles implemented in python

VisualizeShuffles.py does the following:
* Runs various shuffles a set number of times on the same 'deck'
* Outputs the shuffling process as an mp4 file in /Video/
* Outputs the state of the deck after each shuffle as a PNG in /Shuffles/
* Outputs a graph of the correlations in /Plots/

Naturally this is disgustingly unmodular, for which I apologise profusely

# Requirements
* [Python 3.6+](https://www.python.org/downloads/)
* [opencv](https://opencv.org/)
* [matplotlib](https://matplotlib.org/) (only required for correlation graphs)

[Shuffling on wikipedia](https://en.wikipedia.org/wiki/Shuffling)