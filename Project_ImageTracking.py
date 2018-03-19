# import the necessary packages:
import numpy as np
import time
import cv2
import easygui

# Read video file to frames
video = cv2.VideoCapture("Track_test5.mp4")
ret, frame = video.read()

# Get gray image of first frame 
frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)	

# Function1: Drag mouse to select tracking target 
global pointLD, pointLU, template, template_w, template_h
def mouse_draw(event,x,y,flags,param): 
	global pointLD, pointLU, template, template_w, template_h
	image = frame.copy()
	if event == cv2.EVENT_LBUTTONDOWN:
		# Get x,y coordinates of first selected point
		pointLD = (x,y)
	elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON):
		# Show a red rectangle when dragging the mouse
		cv2.rectangle(img=image, pt1=pointLD, pt2=(x,y), color=(0,0,255), thickness=1)
		cv2.imshow("Target Selection", image)
	elif event == cv2.EVENT_LBUTTONUP:
		# Get x,y coordinates of second selected point
		pointLU = (x,y)
		# Show the final green selected target with a green rectangle
		cv2.rectangle(img=image, pt1=pointLD, pt2=pointLU, color=(0,255,0), thickness=1)
		cv2.imshow("Target Selection", image)
		# Save the selected target as the template in gray scale
		template = frame_gray[pointLD[1]:pointLU[1], pointLD[0]:pointLU[0]]
		# Get size of selected area 
		template_w = pointLU[0] - pointLD[0]
		template_h = pointLU[1] - pointLD[1]

# Target selection 
while True:
	cv2.namedWindow("Target Selection") 
	cv2.setMouseCallback("Target Selection", mouse_draw) 
	cv2.imshow("Target Selection", frame)
	# Press any key to reselect target, press "q" to quit target selection
	key = cv2.waitKey(0)
	if key == ord("q"):
		break
		
# Show the selected template		
# cv2.imshow("Template", template)
# key = cv2.waitKey(0)

# Target tracking 
global point1, point2, point1_old, point2_old
point1_old = pointLD
point2_old = pointLU
for i in range(0,600):
    # Get a new frame each time 
	ret, frame = video.read()
	frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	
	# Find tracking target in the new frame by matching algorithm 
	# Set value of matching standard 
	match_standard = 0.9
	# Matching similar target by selected template 
	match_value = cv2.matchTemplate(frame_gray, template, cv2.TM_CCOEFF_NORMED) 
	# Find location of matched area
	location = np.where(match_value >= match_standard)
	
	# Get location of matched area and draw a rectangle to show the target 
	# Get x,y coordinates of target  
	loc = zip(*location[::-1])
	for pointT in loc[0:5]:
	# Draw rectangle (green)
		point1 = pointT
		point2 = (pointT[0]+template_w, pointT[1]+template_h)
		cv2.rectangle(frame, pt1=point1, pt2=point2, color=(0,255,0), thickness=1)
	
	# Use matched target as the updated template 
	# If there's no big changes, use old template as the updated template
	if abs(point1[0] - point1_old[0])<=1 and abs(point1[1] - point1_old[1])<=1:
		template = frame_gray[point1_old[1]:point2_old[1],point1_old[0]:point2_old[0]]
	else:
		template = frame_gray[point1[1]:point2[1],point1[0]:point2[0]]
		point1_old = point1
		point2_old = point2
		
	cv2.imshow("Tracking Target", frame)
	key = cv2.waitKey(50) 
	if key == ord('q'):
		break
	
cv2.destroyAllWindows()
	
	
	
	
