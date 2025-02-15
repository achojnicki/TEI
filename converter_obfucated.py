#!/usr/bin/env python3

import numpy as np
from PIL import Image
from sys import argv
from tqdm import tqdm
from random import choice, randint


COLOR_TEMPLATE=""".<_ident_> {background: <_color_>;} """


class converter:

	def __init__(self):
		self._colors={}
		self._idents=[]

		self._table_class=self._seed()
		self._tr_class=self._rand_ident()
		self._td_class=self._rand_ident()
		self._hidden_class=self._rand_ident()

		self._idents.append(self._table_class)
		self._idents.append(self._tr_class)
		self._idents.append(self._td_class)
		self._idents.append(self._hidden_class)	
		


		self._style="""body {display: block;} .<_table_class_> {margin: 0px; padding: 0px; border-spacing: 0px;} .<_tr_class_> {margin: 0px;padding: 0px;} .<_td_class_> {width: 1px;height: 1px;margin: 0px;padding: 0px;}.<_hidden_class_> {display: none;}""".replace('<_table_class_>', self._table_class).replace('<_tr_class_>',self._tr_class).replace('<_td_class_>', self._td_class).replace("<_hidden_class_>", self._hidden_class)

		self._table="""<table id="table" class="<_table_class_>">""".replace("<_table_class_>", self._table_class)

		self._data="""<html><head><style><_style_></style></head><body><_table_></body></html>"""

		self._img=Image.open(argv[1])
		self._bitmap=np.array(self._img)
		self._output_file="data.html"
		self._convert()
		self._compose()
		self._save()

	def _append_style(self, ident, color):
		self._style+=COLOR_TEMPLATE.replace('<_ident_>', ident).replace('<_color_>', color)


	def _seed(self):	
		ident=""
		for a in range(12):
			ident+=chr(randint(97, 122))
		return ident

	def _rand_ident(self):
		ident=self._table_class if len(self._idents)==0 else self._idents[randint(0, len(self._idents)-1)]
		base=str(ident)
		while True:
			index=randint(1,len(base)-1)
			ident=base[0:index]+chr(randint(97,122))+base[index+1:len(base)]
			if ident!=base and ident not in self._idents:
				break
			base=str(ident)

		return ident

	def _build_pixel(self,classes):

		cl=""
		for c in classes:
			cl+=c+" "

		return f"""<td class="{cl}"></td>"""


	def _color_hex(self,r,g,b):
		return '#%02x%02x%02x' % (r, g, b)

	def _compose(self):
		self._data=self._data.replace('<_style_>', self._style).replace('<_table_>', self._table).replace('<_hidden_class_>', self._hidden_class)

	def _convert(self):
		for x in tqdm(range(0,self._img.size[1], 1)):
			self._table+="""<tr class="<_tr_class_>">""".replace("<_tr_class_>", self._tr_class)
			for y in range(0,self._img.size[0], 1):

					color=[self._bitmap[x][y][0], self._bitmap[x][y][1], self._bitmap[x][y][2]]
					color_hex=self._color_hex(*color)

					if color_hex not in self._colors:
						while True:
							ident=self._rand_ident()
							if ident not in self._idents:
								break
						self._colors[self._color_hex(*color)]=ident
						self._idents.append(ident)
						self._append_style(ident=ident, color=color_hex)
					else:
						ident=self._colors[color_hex]

					self._table+=self._build_pixel([self._td_class, ident])

					if choice([True, False]) and len(self._idents)>0:
						ident=self._idents[randint(0, len(self._idents)-1)]
						self._table+=self._build_pixel([self._hidden_class, ident])

			self._table+="</tr>"
		self._table+="</table>"


	def _save(self):
		with open(self._output_file,'w') as f:
			f.write(self._data)
			f.close()



if __name__=="__main__":
		c=converter()

