# -*- coding: utf-8 -*-
from pygame.locals import * 

class Camera(object):
    def __init__(self, width, height):
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target, width = 1200, height = 705):

		l, t, _, _ = target.rect
		_, _, w, h = self.state
		l, t, _, _ = -l+width/2, -t+height/2, w, h

		l = min(0, l)                           # stop scrolling at the left edge
		l = max(-(self.state.width-width), l)   # stop scrolling at the right edge
		t = max(-(self.state.height-height), t) # stop scrolling at the bottom
		t = min(0, t)                           # stop scrolling at the top
		self.state = Rect(l, t, w, h)
		return Rect(l, t, w, h)

