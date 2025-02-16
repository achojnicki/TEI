#!/usr/bin/env python3

import numpy as np
from PIL import Image
from sys import argv
from tqdm import tqdm



class converter:
	_data="""\
<html>
<body>
<style>
body {
	display: block;
	}
.img {
	display: grid;
	grid-template-columns: repeat(<_image_width_>, 1px);
	margin: 0px;
	padding: 0px;
}
.pixel {
	width: 1px;
	height: 1px;
 }

</style>"""

	def __init__(self):
		self._img=Image.open(argv[1])
		self._bitmap=np.array(self._img)
		self._output_file='data.html'

		self._data=self._data.replace('<_image_width_>', str(self._img.size[0]))
		self._convert()
		self._save()



	def cod(self,col):
		return f"""<div class="pixel" style="background:{col}"></div>"""


	def col(self,r,g,b):
		return '#%02x%02x%02x' % (r, g, b)


	def _convert(self):
		self._data+="""<div style="img">"""
		for x in tqdm(range(0,self._img.size[1], 1)):
			for y in range(0,self._img.size[0], 1):
				self._data+=self.cod(self.col(self._bitmap[x][y][0],self._bitmap[x][y][1],self._bitmap[x][y][2]))
		self._data+="</div></body></html>"

	def _save(self):
		with open(self._output_file,'w') as f:
			f.write(self._data)
			f.close()



if __name__=="__main__":
		c=converter()

