# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 21:32:58 2022

@author: ASH
"""

import cv2
import numpy as np

np.set_printoptions(suppress=True)

st_points = []
ed_points = []
def define_location(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print('Start Mouse Position: '+str(x)+', '+str(y))
        coor = np.array([x,y])
        st_points.append(coor)
        
    elif event == cv2.EVENT_LBUTTONUP:
        print('End Mouse Position: '+str(x)+', '+str(y))
        coor = np.array([x,y])
        ed_points.append(coor)

# Image Load -----------------------------------------------------
img = cv2.imread('./hutme.jpg', cv2.IMREAD_COLOR)

# cv2.namedWindow('image')
# cv2.setMouseCallback('image', define_location)
# cv2.imshow('image', img)

# while True:
#     if cv2.waitKey() == 27:
#         cv2.destroyAllWindows()
#         break

# st = st_points
# ed = ed_points
# ----------------------------------------------------------------

# Define height of pillar
# We assume that is 201cm
pillar_height = 201

# Define coordinates
person_coor = [np.array([327, 392]), np.array([329, 617])]

st = [np.array([411, 354]), np.array([398, 645]), np.array([548, 349]), np.array([549, 609])]
ed = [np.array([128, 377]), np.array([129, 534]), np.array([864, 370]), np.array([846, 575])]

# Homogeneous vectorize
st = np.append(st, np.ones((4,1), dtype=np.int), axis=1)
ed = np.append(ed, np.ones((4,1), dtype=np.int), axis=1)
person_coor = np.append(person_coor, np.ones((2,1), dtype=np.int), axis=1)

# Compute vanising point Vx
Vx = np.cross(np.cross(st[0], ed[0]),np.cross(st[1], ed[1]))
Vx = Vx/Vx[2]

# Compute vanising point Vy
Vy = np.cross(np.cross(st[2], ed[2]),np.cross(st[3], ed[3]))
Vy = Vy/Vy[2]

# Compute vanishing point V
V = np.cross(np.cross(ed[0], person_coor[1]),np.cross(Vx,Vy))
V = V/V[2]

# Compute t
T = np.cross(np.cross(V, person_coor[0]), np.cross(st[0], st[1]))
T = T/T[2]

person_height = pillar_height * (T[1]-st[1][1])/(st[0][1]-st[1][1])
print(person_height)

# print image with points and lines ---------------------------
vx = tuple(Vx[:2].astype(np.int))
vy = tuple(Vy[:2].astype(np.int))
v = tuple(V[:2].astype(np.int))
t = tuple(T[:2].astype(np.int))

cv2.namedWindow('image')
# vanishing line
cv2.line(img, vx, vy, (0,0,255),3)
# vanising point v
cv2.circle(img, v, 3, (255,0,0),-1,cv2.LINE_AA)
# line between v and t
cv2.line(img, v, t, (0,255,0),3)
# point t
cv2.circle(img, t, 3, (255,0,0),-1,cv2.LINE_AA)

cv2.imshow('image', img)

while True:
    if cv2.waitKey() == 27:
        cv2.destroyAllWindows()
        break
# -------------------------------------------------------------