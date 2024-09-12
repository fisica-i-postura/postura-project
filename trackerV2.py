import cv2
import mediapipe as mp

mp_pose = mp.solutions.pose

cap = cv2.VideoCapture("../postura-project/video/Bien_Caminata_Con_Peso.mp4")

if not cap.isOpened():
    print("Error: No se pudo abrir el video.")
    exit()

with open("right_ankle_coordinatesV2.txt", "w") as file:
    pose = mp_pose.Pose(
        static_image_mode=False,
        min_tracking_confidence=0.5
    )
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
               
        results = pose.process(frame_rgb)
                
        if results.pose_landmarks:           
            right_ankle = results.pose_landmarks.landmark[28]
            
            # Verificamos si la confianza de seguimiento es mayor a 0.5
            if right_ankle.visibility > 0.5:                
                print(right_ankle)
                
                # Guardamos las coordenadas en el archivo txt
                #file.write(f"{right_ankle.x},{right_ankle.y},{right_ankle.z}\n")  # Guardamos las coordenadas x, y, z
                file.write(str(right_ankle) + "\n")   

cap.release()
