import cv2
import numpy as np
import os

def classify_object(w, h):
    # Classifica como adulto se as condições forem atendidas
    if h > 160 and w > 50:
        return "Crianca"
    elif h > 100 and w > 30:
        return "Adulto"
    else:
        return "Animal"


def detect_and_count_objects(frame, background, min_area=1000):
    
    # Pega o frame atual
    fgMask = cv2.absdiff(background, frame)
    
    #Escala de cinza
    gray = cv2.cvtColor(fgMask, cv2.COLOR_BGR2GRAY)
    
    # Aplica um limiar binário para destacar as diferenças
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
    
    # Aplica um desfoque gaussiano (suavização)
    blur = cv2.GaussianBlur(thresh, (15, 15), 0)
    
    # Aplica operações morfológicas para limpeza
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

    # Erosão remove pequenos ruidos
    eroded = cv2.erode(blur, kernel, iterations=2)
    
    # Dilatação
    dilated = cv2.dilate(eroded, kernel, iterations=2)
    
    # Operação de abertura (remoção de ruídos internos)
    opened = cv2.morphologyEx(dilated, cv2.MORPH_OPEN, kernel, iterations=2)
    
    # Operação de fechamento (preenchimento de pequenos buracos)
    cleaned_mask = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel, iterations=2)
    
    # Encontra contornos na máscara limpa
    contours, _ = cv2.findContours(cleaned_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filtra contornos pequenos
    filtered_contours = [contour for contour in contours if cv2.contourArea(contour) > min_area]
    
    return filtered_contours

def process_video(video_path, output_folder, interval=2):
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"Erro ao abrir o vídeo: {video_path}")
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * interval)
    
    frame_count = 0
    saved_count = 0
    background = None
    alpha = 0.47  # Taxa de aprendizado para atualização do fundo

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Define ou atualiza o fundo
        if background is None:
            background = frame.astype("float")
            continue
        else:
            cv2.accumulateWeighted(frame, background, alpha)
            background_frame = cv2.convertScaleAbs(background)

        # Detecta e conta objetos
        contours = detect_and_count_objects(frame, background_frame)
        
        # Desenha os contornos e classifica os objetos no frame
        object_count = 0
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w > 50 and h > 50:  # Ajuste para filtrar objetos pequenos
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                #Classifica o objeto
                label = classify_object(w, h)
                cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                
                object_count += 1

        # Exibe o número de objetos detectados no frame
        cv2.putText(frame, f'Objetos detectados: {object_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        if frame_count % frame_interval == 0:
            frame_filename = os.path.join(output_folder, f"processed_frame_{saved_count:04d}.png")
            cv2.imwrite(frame_filename, frame)
            saved_count += 1
            
            cv2.imshow('Detecção de Movimento', frame)
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break
        
        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()

video_path = r'C:/Users/adria/Desktop/identifica-objetos/data/input/teste_01.mp4'
output_folder = r"C:\Users\adria\Desktop\identifica-objetos\data\output"
process_video(video_path, output_folder, interval=2)