from random import randint
from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm
from sys import argv

import numpy as np


class SanKyu:
	def __init__(self):
		self._width=500
		self._height=500
		self._font=ImageFont.truetype('comicbd.ttf', 300)

	def _generate_shape(self):
		img=Image.new(mode="RGBA", size=(self._width, self._height), color='black')
		draw=ImageDraw.Draw(img)
		draw.text((40,40), "39", font=self._font, fill="white")

		self._shape=np.array(img)
		self._shape_values=self._generate_noise_array(self._width, self._height)

	def _load_image(self):
		img=Image.open(argv[1])

		self._width=img.size[0]
		self._height=img.size[1]

		self._shape=np.array(img)
		self._shape_values=self._generate_noise_array(self._width, self._height)

	def _generate_noise_array(self, x,y):
		data=[]
		for _y in range(0, y):
			data.append([])
			for _x in range(0, x):
				r=randint(0,255)
				data[_y].append([r,r,r])

		data=np.array(data, dtype=np.uint8)
		data.reshape(x,y,3)
		return data

	def _apply_shape(self, frame):
		for y in tqdm(range(0,self._width, 1)):
			for x in range(0,self._height, 1):
				if self._shape[x][y][0]<150 and self._shape[x][y][1]<150 and self._shape[x][y][2]<150:
					frame[x][y][0]=self._shape_values[x][y][0]
					frame[x][y][1]=self._shape_values[x][y][1]
					frame[x][y][2]=self._shape_values[x][y][2]
		return frame



	def _generate_frame(self):
		frame=self._generate_noise_array(self._width, self._height)
		frame_with_shape=self._apply_shape(frame)
		img=Image.fromarray(frame).convert('RGB')
		return img



	def generate(self):
		if len(argv)>1:
			self._load_image()
		else:
			self._generate_shape()

		base_image = self._generate_frame()
		frames=[]
		for frame in range(10):
			frames.append(self._generate_frame())

		base_image.save("39.gif", save_all=True, append_images=frames, duration=50, loop=2)


if __name__=="__main__":
	sankyu=SanKyu()
	sankyu.generate()