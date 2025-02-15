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
<table>"""

	def __init__(self):
		self._img=Image.open(argv[1])
		self._bitmap=np.array(self._img)
		self._output_file='data.html'
		self._convert()
		self._save()



	def cod(self,col):
		return f"""<td style="background-color: {col}"></td>"""


	def col(self,r,g,b):
		return '#%02x%02x%02x' % (r, g, b)


	def _convert(self):
		for x in tqdm(range(0,self._img.size[1], 1)):
			self._data+="<tr>"
			for y in range(0,self._img.size[0], 1):
					self._data+=self.cod(self.col(self._bitmap[x][y][0],self._bitmap[x][y][1],self._bitmap[x][y][2]))
			self._data+="</tr>"
		self._data+="</table></body></html>	"

	def _save(self):
		with open(self._output_file,'w') as f:
			f.write(self._data)
			f.close()



if __name__=="__main__":
		c=converter()

