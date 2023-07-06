import numpy as np
import cv2
import math

class AxisProjection:
    def __init__(self):
        pass

    def projection(self, window, alpha, gamma, pitch, yaw, roll, w, h, offsetx, offsety,title):
    
        def spherical_to_cartesian(rho, theta, phi):
            x = rho * np.sin(phi) * np.cos(theta)
            y = rho * np.sin(phi) * np.sin(theta)
            z = rho * np.cos(phi)
            return x, y, z

        linethickness = int(max(min(w,h)/(190),1))
        thickness = int(max(min(w,h)/(500),1))
        fontScale = min(w,h)/(1800)
        scaleline = min(w,h)/(1400)  # Adjust the scale here
        #print(i, scaleline)
        x2, y2, z2 = spherical_to_cartesian(scaleline, alpha, gamma)
        axis_points = np.float32([[0, 0, 0], [scaleline, 0, 0], [0, -scaleline, 0], [0, 0, scaleline], [x2, -y2, z2]])

        # rotate axis
        rotation_vector = np.array([np.radians(pitch), np.radians(yaw), np.radians(roll)], dtype=np.float32) #[x pitch, y roll, z yaw]
        translation_vector = np.array([0, 0, 5], dtype=np.float32)  # position of the coordinate system in relation to the camera.
        # Define the camera intrinsic parameters
        camera_matrix = np.array([[800, 0, w//2], [0, 800, h//2], [0, 0, 1]], dtype=np.float32)
        dist_coeffs = np.zeros((4, 1))

        # Project the 3D points onto the 2D image plane
        image_points, _ = cv2.projectPoints(axis_points, rotation_vector, translation_vector, camera_matrix, dist_coeffs)
        image_points += np.array([offsetx, offsety], dtype=np.float32)

        # Draw the projected axis lines on the image
        origin = tuple(image_points[0].reshape(2).astype(int))
        x_axis = tuple(image_points[1].reshape(2).astype(int))
        y_axis = tuple(image_points[2].reshape(2).astype(int))
        z_axis = tuple(image_points[3].reshape(2).astype(int))
        vec2 = tuple(image_points[4].reshape(2).astype(int))
    
        #draw axis
        cv2.line(window, origin, x_axis, (0, 0, 255), thickness=linethickness)  # Draw x-axis (red)
        cv2.line(window, origin, y_axis, (0, 255, 0), thickness=linethickness)  # Draw y-axis (green)
        cv2.line(window, origin, z_axis, (255, 0, 0), thickness=linethickness)  # Draw z-axis (blue)
        cv2.arrowedLine(window, origin, vec2, (255, 255, 255), thickness=linethickness)  # Draw second vector (white)

        title_loc = (int(w//2+offsetx), int(h//2+offsety*(9.5/10)))
        # Add labels to each axis
    
        cv2.putText(window, 'X', x_axis, cv2.FONT_HERSHEY_SIMPLEX,fontScale=fontScale, thickness=thickness, color = (0, 0, 255))
  
        cv2.putText(window, 'Y', y_axis, cv2.FONT_HERSHEY_SIMPLEX,fontScale=fontScale, thickness=thickness, color = (0, 255, 0))
        cv2.putText(window, 'Z', z_axis, cv2.FONT_HERSHEY_SIMPLEX,fontScale=fontScale, thickness=thickness, color = (255, 0, 0))
        cv2.putText(window, 'B', vec2, cv2.FONT_HERSHEY_SIMPLEX,fontScale=fontScale, thickness=thickness, color = (255, 255, 255))
        cv2.putText(window, title, title_loc, cv2.FONT_HERSHEY_SIMPLEX,fontScale=fontScale, thickness=thickness, color = (0, 255, 255))
   
        return window

    def draw_topview(self, window,alpha, gamma, window_width, window_height):
        title = "top"
        pitch,yaw,roll = 0,0,0
        offsetx, offsety = int((window_width/2)*(6.5/10)) , -int((window_height/2)*(7.4/10))#pixel offset from center 
        window = self.projection(window,alpha,gamma,pitch,yaw,roll,window_width, window_height, offsetx,offsety, title)
        return window
    
    def draw_sideview(self, window, alpha, gamma, window_width, window_height):
        #side view 
        title = "side"
        pitch,yaw,roll = 90,0,0
        offsetx, offsety = int((window_width/2)*(8.5/10)) , -int((window_height/2)*(7.4/10))#pixel offset from center 
        window = self.projection(window,alpha,gamma,pitch,yaw,roll,window_width, window_height, offsetx,offsety, title)
        return window

if __name__ == "__main__":
    window_width  = 480
    window_height =   270
    i= 100
    proj = AxisProjection()
    while True:
        i+=1
        window_width +=1 
        window_height +=1 
        window = np.zeros((window_height, window_width, 3), dtype=np.uint8)
        window.fill(0)
        
        # Define spherical coordinates for the second vector
        alpha = np.radians(i)  # Azimuthal angle (in degrees)
        gamma = np.radians(45)  # Polar angle (in degrees)
        proj.draw_topview(window,alpha,gamma,window_width,window_height)
        proj.draw_sideview(window,alpha,gamma,window_width,window_height)
        

        
        # Display the image
        cv2.imshow("Diametric Projection", window)

        if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
cv2.destroyAllWindows()