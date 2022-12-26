import pygame, sys
from pygame.locals import *
from guizero import *
from tkinter import ttk, Label
from playsound import playsound
import random
import time
import speech_recognition as sr

cerrarVentana = False
categoria = -1
velocidad = -1

def nuevoBoton(forma,screen, rectangulo, texto, x1,y1,z1,x2,y2,z2):
    pygame.draw.rect(screen, (x1,y1,z1), rectangulo,0)
    aux = forma.render(texto, True, (x2,y2,z2))
    screen.blit(aux,(rectangulo.x+(rectangulo.width-aux.get_width())/2,rectangulo.y+(rectangulo.height-aux.get_height())/2))

def cuadroTexto(existe):
    def aux():
        nombre = entry.get()
        root.destroy()
        registro(existe,nombre)
        
    root=Tk()
    root.title("Datos")
    root.config(bg="#19DEC0")
    wtotal = root.winfo_screenwidth()
    htotal = root.winfo_screenheight()
    wventana = 200
    hventana = 100
    pwidth = round(wtotal/2-wventana/2)
    pheight = round(htotal/2-hventana/2)
    root.geometry(str(wventana-25)+"x"+str(hventana)+"+"+str(pwidth)+"+"+str(pheight))
    label = Label(root, text="Ingresa tu usuario")
    label.pack()
    label.config(bg="#19DEC0", fg="black",font=("Arial", 15))
    entry = ttk.Entry()
    entry.place(x=27,y=35)
    entry.config(width=13, font=("Arial", 13))
    boton = ttk.Button(text="Iniciar", command=aux, width=13)
    boton.place(x=45, y=70)
    root.mainloop()

def registro(existe, name):
    if(existe):
        file = open("usuarios/"+name+".txt", "r")
        nivel =  (int(file.read()))
        file.close()
        pictures(nivel, name, categoria, velocidad)
                
    else:
        file = open("usuarios/"+name+".txt", "w")
        file.write("3")
        file.close()
        pictures(3, name, categoria, velocidad)

def pictures(nivel, name, catego, veloci):
    def normalize(s):
        replacements = (
            ("á", "a"),
            ("é", "e"),
            ("í", "i"),
            ("ó", "o"),
            ("ú", "u"),
        )
        for a, b in replacements:
            s = s.replace(a, b).replace(a.upper(), b.upper())
        return s
    pensando = pygame.image.load("imagenes/pensandoH.gif")
    fuente_habla = pygame.font.SysFont("segoe print",50) 
    habla = fuente_habla.render("HABLA...",True, (255,0,0))
    escuche = fuente_habla.render("Te escuche :)",True, (255,0,0))
    pantalla.blit(fondo, (0,0))
    pantalla.blit(pensando, (100,100))
    pygame.display.flip()
    diccionario1 = {1:"cocodrilo",
                    2: "tigre",
                    3: "leon",
                    4: "elefante",
                    5: "jirafa",
                    6: "delfin",
                    7: "otorongo",
                    8: "pelicano",
                    9: "atun",
                    10: "gato"
    }
    diccionario2 = { 1: "lampara",
                     2: "cama",
                     3: "teclado",
                     4: "television",
                     5: "sillon",
                     6: "celular",
                     7: "bota",
                     8: "espejo",
                     9: "plato",
                     10: "camisa"  
    }
    diccionario3 = { 1: "alemania",
                     2: "argentina",
                     3: "francia",
                     4: "colombia",
                     5: "japon",
                     6: "rusia",
                     7: "mexico",
                     8: "chile",
                     9: "marruecos",
                     10: "peru"  
    }
    diccionario = [diccionario1,diccionario2,diccionario3]
    lista = [0,0,0,0,0,0,0,0,0,0] 
    playsound("audios_level/nivel"+str(nivel)+".mp3")  #-----
    playsound("audios_level/preparacion.mp3")
    orden = ""
    time.sleep(0.5)   
    for i in range(nivel):
        num = random.randint(1,10)
        while(lista[num-1] != 0):
            num = random.randint(1,10)
        lista[num-1] = 1
        orden+=diccionario[catego].get(num)+" "
        palabra = pygame.image.load("imagenes/"+diccionario[catego].get(num)+".jpg")
        pantalla.blit(fondo, (0,0))
        pantalla.blit(palabra,[200,100])
        pygame.display.flip()
        aux = "audios/"+diccionario[catego].get(num) +".mp3"
        playsound(aux) 
        time.sleep(veloci)
    
    pantalla.blit(fondo, (0,0))
    pantalla.blit(pensando, (100,50))
    pygame.display.flip()
    playsound("audios_level/audio-hablar.mp3")
    print("habla")
    pantalla.blit(habla, (300,450))
    pygame.display.flip()
    r = sr.Recognizer() 
    global cerrarVentana
    with sr.Microphone() as source:
        audio = r.listen(source)
        pantalla.blit(fondo, (0,0))
        pantalla.blit(pensando, (100,50))
        pantalla.blit(escuche, (220,450))
        pygame.display.flip()
        try:
            text = r.recognize_google(audio, language="es-ES")
            print('Digiste: '+ text)
            text = normalize(text).lower()+" "
            if(text == orden):
                print("Bien")        
                playsound("audios_level/excelente.mp3")
                file = open("usuarios/"+name+".txt", "w")
                file.write(str(nivel+1))
                file.close()
                pictures(nivel+1, name, catego, veloci)
            else:
                print("Mal")
                playsound("audios_level/Prueba de nuevo.mp3")
                cerrarVentana = True
        except:
            print('Ocurrio un error')
            cerrarVentana = True

            
pygame.init()
pantalla = pygame.display.set_mode((800,600))
pygame.display.set_caption("Juego de Memoria!")
fondo = pygame.image.load("imagenes/fondo-Claro.jpg").convert()
fuente_Titulo = pygame.font.SysFont("impact",50)
titulo = fuente_Titulo.render("Bienvenido al juego de memoria",True,(225,0,0))
fuente_label1 = pygame.font.SysFont("Helvetica",30)
label3 = fuente_label1.render("¿Tengo una cuenta?",True,(0,0,255))
label1 = fuente_label1.render("Elige la categoria que quieres memorizar",True,(0,0,255))
label2 = fuente_label1.render("Elige el nivel de velocidad",True,(0,0,255))

fuente_labelBoton = pygame.font.SysFont("Helvetica", 25)
fuente_salir = pygame.font.SysFont("Arial", 30)
fuente_boton = pygame.font.SysFont("Arial", 19)
rec_si = Rect(200,400,80,30)
rec_no = Rect(510,400,80,30)
rec_salir = Rect(325,500,150,50)
rec_animales = Rect(200,140,80,30)
rec_cosas = Rect(360,140,80,30)
rec_paises = Rect(510,140,80,30)
rec_facil = Rect(200,270,80,30)
rec_medio = Rect(360,270,80,30)
rec_dificil = Rect(510,270,80,30)


pantalla.blit(fondo, (0,0))
pantalla.blit(titulo, (60,0))
pygame.display.flip()
playsound("audios_level/welcome.mp3")
nuevoBoton(fuente_labelBoton,pantalla,rec_si,"SI",209,206,205,0,0,0)
nuevoBoton(fuente_labelBoton,pantalla,rec_no,"NO",209,206,205,0,0,0)
nuevoBoton(fuente_salir,pantalla,rec_salir,"SALIR",0,0,255,255,255,255)
nuevoBoton(fuente_boton,pantalla,rec_animales,"Animales",209,206,205,0,0,0)
nuevoBoton(fuente_boton,pantalla,rec_cosas,"Cosas",209,206,205,0,0,0)
nuevoBoton(fuente_boton,pantalla,rec_paises,"Países",209,206,205,0,0,0)
nuevoBoton(fuente_boton,pantalla,rec_facil,"Fácil",209,206,205,0,0,0)
nuevoBoton(fuente_boton,pantalla,rec_medio,"Medio",209,206,205,0,0,0)
nuevoBoton(fuente_boton,pantalla,rec_dificil,"Dificil",209,206,205,0,0,0)
pantalla.blit(label1, (120,80))
pantalla.blit(label2, (220,205))
pantalla.blit(label3, (260,335))
pygame.display.flip()

while True:
    for event in pygame.event.get():
        if cerrarVentana:
            pygame.quit()
            sys.exit()
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if(pygame.MOUSEBUTTONDOWN == event.type and pygame.BUTTON_LEFT==1):
            if(rec_si.collidepoint(pygame.mouse.get_pos())):
                nuevoBoton(fuente_labelBoton,pantalla,rec_si,"SI",0,255,0,0,0,0)
                nuevoBoton(fuente_labelBoton,pantalla,rec_no,"NO",209,206,205,0,0,0)
                pygame.display.flip()
                cuadroTexto(True)
        if(pygame.MOUSEBUTTONDOWN == event.type and pygame.BUTTON_LEFT==1):
            if(rec_no.collidepoint(pygame.mouse.get_pos())):
                nuevoBoton(fuente_labelBoton,pantalla,rec_no,"NO",0,255,0,0,0,0)
                nuevoBoton(fuente_labelBoton,pantalla,rec_si,"SI",209,206,205,0,0,0)
                pygame.display.flip()
                cuadroTexto(False)
        if(pygame.MOUSEBUTTONDOWN == event.type and pygame.BUTTON_LEFT==1):
            if(rec_animales.collidepoint(pygame.mouse.get_pos())):
                categoria = 0
                nuevoBoton(fuente_boton,pantalla,rec_animales,"Animales",0,255,0,0,0,0)
                nuevoBoton(fuente_boton,pantalla,rec_cosas,"Cosas",209,206,205,0,0,0)
                nuevoBoton(fuente_boton,pantalla,rec_paises,"Países",209,206,205,0,0,0)
        if(pygame.MOUSEBUTTONDOWN == event.type and pygame.BUTTON_LEFT==1):
            if(rec_cosas.collidepoint(pygame.mouse.get_pos())):
                categoria = 1
                nuevoBoton(fuente_boton,pantalla,rec_cosas,"Cosas",0,255,0,0,0,0)
                nuevoBoton(fuente_boton,pantalla,rec_animales,"Animales",209,206,205,0,0,0)
                nuevoBoton(fuente_boton,pantalla,rec_paises,"Países",209,206,205,0,0,0)
        if(pygame.MOUSEBUTTONDOWN == event.type and pygame.BUTTON_LEFT==1):
            if(rec_paises.collidepoint(pygame.mouse.get_pos())):
                categoria = 2
                nuevoBoton(fuente_boton,pantalla,rec_paises,"Países",0,255,0,0,0,0)
                nuevoBoton(fuente_boton,pantalla,rec_animales,"Animales",209,206,205,0,0,0)
                nuevoBoton(fuente_boton,pantalla,rec_cosas,"Cosas",209,206,205,0,0,0)
        if(pygame.MOUSEBUTTONDOWN == event.type and pygame.BUTTON_LEFT==1):
            if(rec_facil.collidepoint(pygame.mouse.get_pos())):
                velocidad = 2
                nuevoBoton(fuente_boton,pantalla,rec_facil,"Fácil",0,255,0,0,0,0)
                nuevoBoton(fuente_boton,pantalla,rec_medio,"Medio",209,206,205,0,0,0)
                nuevoBoton(fuente_boton,pantalla,rec_dificil,"Dificil",209,206,205,0,0,0)
        if(pygame.MOUSEBUTTONDOWN == event.type and pygame.BUTTON_LEFT==1):
            if(rec_medio.collidepoint(pygame.mouse.get_pos())):
                velocidad = 1
                nuevoBoton(fuente_boton,pantalla,rec_medio,"Medio",0,255,0,0,0,0)
                nuevoBoton(fuente_boton,pantalla,rec_facil,"Facil",209,206,205,0,0,0)
                nuevoBoton(fuente_boton,pantalla,rec_dificil,"Dificil",209,206,205,0,0,0)
        if(pygame.MOUSEBUTTONDOWN == event.type and pygame.BUTTON_LEFT==1):
            if(rec_dificil.collidepoint(pygame.mouse.get_pos())):
                velocidad = 0
                nuevoBoton(fuente_boton,pantalla,rec_dificil,"Dificil",0,255,0,0,0,0)
                nuevoBoton(fuente_boton,pantalla,rec_facil,"Facil",209,206,205,0,0,0)
                nuevoBoton(fuente_boton,pantalla,rec_medio,"Medio",209,206,205,0,0,0)
        if(pygame.MOUSEBUTTONDOWN == event.type and pygame.BUTTON_LEFT==1):
            if(rec_salir.collidepoint(pygame.mouse.get_pos())):
                pygame.quit()
                sys.exit()
        
        pygame.display.flip()

    