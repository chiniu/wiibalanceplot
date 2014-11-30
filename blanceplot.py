#!/usr/bin/python

import wiiboard
import pygame
import time
import os, math, random
from ConfigParser import ConfigParser

class WeightSprite(pygame.sprite.Sprite):
	"""This class describes a sprite containing the weight."""
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.weight = 0.0
		self.update()
		
	def update(self):
		global screen_res, sys_font_weight_fgcolour, sys_font_weight, screen_res
		
		if self.weight > 2:
			self.text = "%.2f" % self.weight
		else:
			self.text = "_.__"
			#print "LESS THAN 2"
		#while len(self.text) < 4:
		#	self.text = "0" + self.text
			
		self.image = sys_font_weight.render(self.text, True, sys_font_weight_fgcolour)

		self.rect = self.image.get_rect()
		self.rect.bottomright = screen_res


if True: 

#def main():
	board = wiiboard.Wiiboard()

	system_file = "system.ini"

	if not os.path.lexists(system_file):
		print "Problem: System configuration file (system.ini) doesn't exist."
		sys.exit(1)

	sconf = ConfigParser()
	sconf.read(system_file)


	xdisplay = sconf.get("display", "xdisplay")
	if len(xdisplay) > 1:
		# using alternate display.
		print "Attempting to use device", xdisplay, "instead of the default."
		os.putenv("DISPLAY", xdisplay)



	pygame.init()
	sys_font_weight = pygame.font.SysFont(sconf.get("font_weight", "face"), int(sconf.get("font_weight", "size")))

	sys_font_weight.set_italic(False)
	sys_font_weight.set_underline(False)

	bgcolour = (0, 0, 0)
	sys_font_weight_fgcolour = (255, 255, 255)
	screen_res = (int(sconf.get("display", "width")), int(sconf.get("display", "height")))
	refresh_delay = int(sconf.get("display", "refresh_delay"))

	screen_options = 0
	if int(sconf.get("display", "fullscreen")) >= 1 and len(xdisplay) <= 1:
		screen_options = screen_options | pygame.fullscreen

	if int(sconf.get("display", "double_buffers")) >= 1:
		screen_options = screen_options | pygame.DOUBLEBUF

	if int(sconf.get("display", "hardware_surface")) >= 1:
		screen_options = screen_options | pygame.HWSURFACE

	if int(sconf.get("display", "opengl")) >= 1:
		screen_options = screen_options | pygame.opengl

	screen = pygame.display.set_mode(screen_res, screen_options)
	pygame.display.set_caption("scales application")

	weight_sprite = WeightSprite()
	weight_sprite.weight = 40.33
	frame = 0
	
	address = board.discover()
	board.connect(address) #the wii board must be in sync mode at this time

	time.sleep(0.1)
	board.setLight(True)
	done = False

	while (not done):
		time.sleep(0.05)
		for event in pygame.event.get():
			if event.type == wiiboard.WIIBOARD_MASS:
		#		if (event.mass.totalWeight > 10):   #10kg. otherwise you would get alot of useless small events!
				if True:
					print "--mass event--  total weight: " + `event.mass.totalWeight` + ". top left: " + `event.mass.topLeft`
					weight_sprite.weight = event.mass.totalWeight
				#etc for topright, bottomright, bottomleft. buttonpressed and buttonreleased also available but easier to use in seperate event
					try:
						x_balance = (float(event.mass.topRight + event.mass.bottomRight) / float(event.mass.topLeft + event.mass.bottomLeft))
						if x_balance > 1:
							x_balance = (float(event.mass.topLeft + event.mass.bottomLeft) / float(event.mass.topRight + event.mass.bottomRight))
						else:
							x_balance = x_balance -1.
						y_balance = (float(event.mass.bottomRight + event.mass.bottomLeft) / float(event.mass.topRight + event.mass.topLeft))
						if y_balance > 1:
							y_balance = (float(event.mass.topRight + event.mass.topLeft) / float(event.mass.bottomRight + event.mass.bottomLeft))
						else:
							y_balance = y_balance -1.
					except:
						x_balance = 1.
						y_balance = 1.
	
					#print "readings:",readings

					screen.fill(bgcolour) # blank the screen.
	
					# line up the lines
					pygame.draw.line(screen, (0,0,255), (screen_res[0]/2,0), (screen_res[0]/2,screen_res[1]), 2)
					pygame.draw.line(screen, (0,0,255), (0,screen_res[1]/2), (screen_res[0],screen_res[1]/2), 2)
	
					weight_sprite.update()
	
					screen.blit(weight_sprite.image, weight_sprite.rect)
	
					xpos = (x_balance * (screen_res[0]/2)) + (screen_res[0]/2)
					ypos = (y_balance * (screen_res[1]/2)) + (screen_res[1]/2)
		
					#print "balance:", x_balance, y_balance
					#print "position:", xpos,ypos
					pygame.draw.circle(screen, (255,0,0), (int(xpos), int(ypos)), 5)
					pygame.display.flip()
					pygame.time.wait(refresh_delay)	


				
			elif event.type == wiiboard.WIIBOARD_BUTTON_PRESS:
				print "Button pressed!"

			elif event.type == wiiboard.WIIBOARD_BUTTON_RELEASE:
				print "Button released"
				done = True
			
			#Other event types:
			#wiiboard.WIIBOARD_CONNECTED
			#wiiboard.WIIBOARD_DISCONNECTED

	board.disconnect()
	pygame.quit()
	sys.exit(0)
"""
#Run the script if executed
if __name__ == "__main__":
	main()
"""
