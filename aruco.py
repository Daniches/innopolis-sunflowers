import cv2.aruco as aruco

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_50)

def findMarkers(img):
   	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    	parameters =  aruco.DetectorParameters_create()
    	corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, 	parameters=parameters)
    	return(corners, ids)

def markerDistance(img):
	corners, ids = findMarkers(frame)
        if ids is None:
            return 1
        for i in range(len(ids)):
            id = ids[i][0]
            print(id)
            if id in (1, 2):
                paper_corners[id-1] = (corners[i][0][0][0], corners[i][0][0][1])
	return ((paper_corners[0][0]-paper_corners[1][0])**2 + (paper_corners[0][1]-paper_corners[1][1]))**(1/2)