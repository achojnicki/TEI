#!/usr/bin/env python3

import numpy as np
from PIL import Image, ImageFilter
import PIL.ImageOps
from sys import argv
from tqdm import tqdm
from random import randint



class converter:
	_data="""\
<html>
<body>
<style>
body {
	display: block;
	}
table {
	margin: 0px;
	padding: 0px;
	border-spacing: 0px;
}
tr {
	margin: 0px;
	padding: 0px;
}
td {
	width: 1px;
	height: 1px;
	margin: 0px;
	padding: 0px;
}

</style>
<table style="float: left;border-spacing: 0px;background-image: url('https://s3.gifyu.com/images/bSx8M.gif')">"""

	def __init__(self):
		self._img=Image.open(argv[1])
		self._img=self._img.filter(ImageFilter.FIND_EDGES).convert('LA').convert('RGB')
		#self._img=PIL.ImageOps.invert(self._img)
		self._bitmap=np.array(self._img)
		self._output_file='data.html'
		self._convert()
		self._save()



	def cod(self, cls):
		return f"""<td class="{cls}"></td>"""

	def col(self,r,g,b):
		return '#%02x%02x%02x' % (r, g, b)

	def cod_bgc(self, col):
		return f"""<td style="background-color: {col}"></td>"""


	def _convert(self):
		for x in tqdm(range(0,self._img.size[1], 1)):
			self._data+="<tr>"
			for y in range(0,self._img.size[0], 1):
				if self._bitmap[x][y][0]<100 and self._bitmap[x][y][1]<100 and self._bitmap[x][y][2]<100:	
					#self._data+=self.cod_bgc(self.col(19,122,127))
					self._data+=self.cod("")

				else:
					r=randint(150,255)
					self._data+=self.cod_bgc(self.col(r,r,r))
					#self._data+=self.cod("")
			self._data+="</tr>"
		self._data+="</table>"

	def _save(self):
		with open(self._output_file,'w') as f:
			f.write(self._data)
			f.close()



if __name__=="__main__":
		c=converter()

