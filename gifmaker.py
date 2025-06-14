import pyautogui
import imageio
import pygame
import imageio
import math
import sys
import csv
import os
import time
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from tkinter import Tk, filedialog
output_file=""
def escolher_csv():
    global output_file
    root = Tk()
    root.withdraw()
    caminho = filedialog.askopenfilename(
        title="Selecionar ficheiro CSV",
        filetypes=[("Ficheiros CSV", "*.csv")]
    )
    output_file=caminho.replace(".csv",".gif")
    root.destroy()
    return caminho

def ler_faces_csv(caminho):
    faces = []
    with open(caminho, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 12:
                continue
            try:
                pontos = [list(map(float, row[i:i+3])) for i in range(0, 12, 3)]
                faces.append(pontos)
            except ValueError:
                continue
    return faces

def desenhar_faces(faces):
    glColor3f(0, 0, 0)  # faces negras
    glBegin(GL_QUADS)
    for face in faces:
        for ponto in face:
            glVertex3fv(ponto)
    glEnd()

def render_gif():
    global output_file
    caminho = escolher_csv()
    if not caminho or not os.path.exists(caminho):
        print("Ficheiro não encontrado.")
        return

    faces = ler_faces_csv(caminho)
    if not faces:
        print("Nenhuma face válida encontrada no ficheiro.")
        return
    
    pygame.init()
    display = (800, 600)
    
    DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Visualizador 3D - Faces do CSV")
    
    # Fundo amarelo
    glClearColor(1.0, 1.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    gluPerspective(45, (display[0] / display[1]), 0.1, 1000.0)
    glTranslatef(-10, -10, -50)

    angulo = 0
    tempo_ultima_rotacao = time.time()
    clock = pygame.time.Clock()


    running = True
    

    
    frames = []
    angle_step = 5  # graus por frame
    total_steps = int(360 / angle_step)

    for step in range(total_steps):
        clock.tick(60)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for evento in pygame.event.get():
            if evento.type == QUIT:
                running = False

        # Rotação automática a cada 1.5 segundos
        if time.time() - tempo_ultima_rotacao > 0.1:
            angulo += 1
            tempo_ultima_rotacao = time.time()

        glPushMatrix()
        glRotatef(angulo % 360, 0, 1, 0)  # Rotação no eixo Y
        desenhar_faces(faces)
        
        glPopMatrix()

        pygame.display.flip()
        # Captura da imagem
        screenshot = pyautogui.screenshot()
        frames.append(screenshot)
        


        
        

    # Save frames as a GIF
    frames[0].save(
        output_file,
        save_all=True,
        append_images=frames[1:],
        duration=1000 // 10,
        loop=0
    )

    print(f"GIF salvo em: "+output_file)
    pygame.quit()

print("\033c\033[43;30m\n")
render_gif()
