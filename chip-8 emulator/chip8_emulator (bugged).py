import pygame,sys,random,math,tkinter
from tkinter import filedialog
from pygame.locals import *

pygame.init()

BLACK=pygame.color.THECOLORS["black"]
WHITE=pygame.color.THECOLORS["white"]
TAILLEMEMOIRE=4096
ADRESSEDEBUT=512
NOIR=0
BLANC=1
l=64 #nombre de pixels suivant la largeur
L=32 #nombre de pixels suivant la longueur
DIMPIXEL=8 #pixel carré de côté 8
WIDTH=l*DIMPIXEL #largeur de l'écran
HEIGHT=L*DIMPIXEL #longueur de l'écran

VITESSECPU=4 #nombre d'opérations par tour
FPS=16 #pour le rafraîchissement

NBROPCODE=35

class CPU:
   def __init__(self):
       self.memoire=[0 for i in range(TAILLEMEMOIRE)]
       self.V=[0 for i in range(16)] #le registre
       self.I=0 #stocke une adresse mémoire ou dessinateur
       self.saut=[0 for i in range(16)] #pour gérer les sauts dans « mémoire »,16 au maximum
       self.nbrsaut=0 #stocke le nombre de sauts effectués pour ne pas dépasser 16
       self.compteurJeu=0 #compteur pour la synchronisation
       self.compteurSon=0 #compteur pour le son
       self.pc=ADRESSEDEBUT #pour parcourir le tableau « mémoire »
       self.touche=[False for i in range(16)]
       
       
   def decompter(self):
       if self.compteurJeu>0:
          self.compteurJeu-=1
       if self.compteurSon>0:
          self.compteurSon-=1
          

   def recupererOpcode(self):
       return (cpu.memoire[cpu.pc]<<8)+cpu.memoire[cpu.pc+1] 

cpu=CPU() #déclaration de notre CPU


class PIXEL:
   def __init__(self,x,y):
       self.position=pygame.Rect([x,y,DIMPIXEL,DIMPIXEL]) #regroupe l'abscisse et l'ordonnée

       self.couleur=0 #comme son nom l'indique, c'est la couleur

ecran=pygame.Surface((WIDTH,HEIGHT))
carre=[pygame.Surface((DIMPIXEL,DIMPIXEL))for i in range(2)]
carre[0].fill(BLACK)
carre[1].fill(WHITE)
#pixel=[[PIXEL(i*DIMPIXEL,j*DIMPIXEL)for i in range(l)]for j in range(L)]
pixel=[[PIXEL(i*DIMPIXEL,j*DIMPIXEL)for j in range(L)]for i in range(l)]

def initialiserPixel():
    global pixel
    #pixel=[[PIXEL(i*DIMPIXEL,j*DIMPIXEL)for i in range(l)]for j in range(L)]
    pixel=[[PIXEL(i*DIMPIXEL,j*DIMPIXEL)for j in range(L)]for i in range(l)]
    
def initialiserEcran():
   global ecran
   #Ouverture de la fenêtre Pygame
   ecran = pygame.display.set_mode((WIDTH,HEIGHT),) #ajoutez RESIZABLE ou FULLSCREEN
   #Titre
   pygame.display.set_caption("chip-8 emulateur")

def effacerEcran():
    #Pour effacer l'écran, on remet tous les pixels en noir
    for raw in pixel:
       for p in raw:
           p.couleur=NOIR;
    #on repeint l'écran en noir

    ecran.fill(BLACK)

def dessinerPixel(pixel):
    """pixel.couleur peut prendre deux valeurs :
       0, auquel cas on dessine lepixel en noir,
       ou 1, on dessine alors le pixel en blanc"""
    ecran.blit(carre[pixel.couleur],pixel.position)

def updateEcran():
   #On dessine tous les pixels à l'écran
   for x in range(l):
       for y in range(L):
           dessinerPixel(pixel[x][y])
   pygame.display.flip() #on affiche les modifications

def pause():
    continuer=1
    while continuer:
       #Limitation de vitesse de la boucle
       #30 frames par secondes suffisent
       pygame.time.Clock().tick(30)
       
       for event in pygame.event.get():    #Attente des événements
           if event.type == QUIT:
               continuer = 0
               pygame.quit()
               sys.exit()
            
           if event.type == KEYDOWN:
              continuer=0

def listen():
    continuer=1       
    for event in pygame.event.get():    #Attente des événements
        if event.type == QUIT:
            continuer = 0
            pygame.quit()
            sys.exit()
         
        if event.type == KEYDOWN:
           if event.key == K_7:
              cpu.touche[0x0]=True
           elif event.key == K_8:
              cpu.touche[0x1]=True
           elif event.key == K_9:
              cpu.touche[0x2]=True
           elif event.key == K_0:
              cpu.touche[0x3]=True
           elif event.key == K_i:
              cpu.touche[0x4]=True
           elif event.key == K_o:
              cpu.touche[0x5]=True
           elif event.key == K_p:
              cpu.touche[0x6]=True
           elif event.key == K_k:
              cpu.touche[0x7]=True
           elif event.key == K_l:
              cpu.touche[0x8]=True
           elif event.key == K_m:
              cpu.touche[0x9]=True
           elif event.key == K_r:
              cpu.touche[0xa]=True
           elif event.key == K_t:
              cpu.touche[0xb]=True
           elif event.key == K_y:
              cpu.touche[0xc]=True
           elif event.key == K_f:
              cpu.touche[0xd]=True
           elif event.key == K_g:
              cpu.touche[0xe]=True
           elif event.key == K_h:
              cpu.touche[0xf]=True
        elif event.type == KEYUP:
           if event.key == K_7:
              cpu.touche[0x0]=False
           elif event.key == K_8:
              cpu.touche[0x1]=False
           elif event.key == K_9:
              cpu.touche[0x2]=False
           elif event.key == K_0:
              cpu.touche[0x3]=False
           elif event.key == K_i:
              cpu.touche[0x4]=False
           elif event.key == K_o:
              cpu.touche[0x5]=False
           elif event.key == K_p:
              cpu.touche[0x6]=False
           elif event.key == K_k:
              cpu.touche[0x7]=False
           elif event.key == K_l:
              cpu.touche[0x8]=False
           elif event.key == K_m:
              cpu.touche[0x9]=False
           elif event.key == K_r:
              cpu.touche[0xa]=False
           elif event.key == K_t:
              cpu.touche[0xb]=False
           elif event.key == K_y:
              cpu.touche[0xc]=False
           elif event.key == K_f:
              cpu.touche[0xd]=False
           elif event.key == K_g:
              cpu.touche[0xe]=False
           elif event.key == K_h:
              cpu.touche[0xf]=False
    return continuer

def attendAppui(b3):
   attend=1
   continuer=1
   while attend:
      for event in pygame.event.get():    #Attente des événements
           if event.type == QUIT:
               continuer = 0
               attend=0
               pygame.quit()
               sys.exit()
            
           if event.type == KEYDOWN:
              if event.key == K_7:
                 cpu.V[b3]=0x0;cpu.touche[0x0]=True;attend=0
              elif event.key == K_8:
                 cpu.V[b3]=0x1;cpu.touche[0x1]=True;attend=0
              elif event.key == K_9:
                 cpu.V[b3]=0x2;cpu.touche[0x2]=True;attend=0
              elif event.key == K_0:
                 cpu.V[b3]=0x3;cpu.touche[0x3]=True;attend=0
              elif event.key == K_i:
                 cpu.V[b3]=0x4;cpu.touche[0x4]=True;attend=0
              elif event.key == K_o:
                 cpu.V[b3]=0x5;cpu.touche[0x5]=True;attend=0
              elif event.key == K_p:
                 cpu.V[b3]=0x6;cpu.touche[0x6]=True;attend=0
              elif event.key == K_k:
                 cpu.V[b3]=0x7;cpu.touche[0x7]=True;attend=0
              elif event.key == K_l:
                 cpu.V[b3]=0x8;cpu.touche[0x8]=True;attend=0
              elif event.key == K_m:
                 cpu.V[b3]=0x9;cpu.touche[0x9]=True;attend=0
              elif event.key == K_r:
                 cpu.V[b3]=0xa;cpu.touche[0xa]=True;attend=0
              elif event.key == K_t:
                 cpu.V[b3]=0xb;cpu.touche[0xb]=True;attend=0
              elif event.key == K_y:
                 cpu.V[b3]=0xc;cpu.touche[0xc]=True;attend=0
              elif event.key == K_f:
                 cpu.V[b3]=0xd;cpu.touche[0xd]=True;attend=0
              elif event.key == K_g:
                 cpu.V[b3]=0xe;cpu.touche[0xe]=True;attend=0
              elif event.key == K_h:
                 cpu.V[b3]=0xf;cpu.touche[0xf]=True;attend=0
   return continuer

   
def main():
   #pygame.init()
   initialiserEcran()
   initialiserPixel()
   chargerFont()
   
   continuer=1;demarrer=0;compteur=0;
   if len(sys.argv)>=2:
      jeu=sys.argv[1]
   else:
      tk_root = tkinter.Tk()
      tk_root.withdraw()
      jeu =filedialog.askopenfilename()
   demarrer=chargerJeu(jeu)
   if demarrer==1:
      while continuer:
          continuer=listen() #afin de pouvoir quitter l'émulateur
          for compteur in range(VITESSECPU):
              interpreterOpcode(cpu.recupererOpcode())
          """if self.compteurSon!=0:
             Mix_PlayChannel(0, son, 0)  #permet de jouer le bip sonore
             self.compteurSon=0"""          
          updateEcran()
          cpu.decompter()
          pygame.time.delay(FPS) #une pause de 16 ms         
   pause()
   

def initialiserJump():
   #la Chip 8 peut effectuer 35 opérations, chaque opération possédant son masque
   #idem, chaque opération possède son propre identifiant  
   jump={'masque':[None]*NBROPCODE,'id':[None]*NBROPCODE}
   
   jump['masque'][0]= 0x0000; jump['id'][0]=0x0FFF; # 0NNN 
   jump['masque'][1]= 0xFFFF; jump['id'][1]=0x00E0; # 00E0 
   jump['masque'][2]= 0xFFFF; jump['id'][2]=0x00EE; # 00EE 
   jump['masque'][3]= 0xF000; jump['id'][3]=0x1000; # 1NNN 
   jump['masque'][4]= 0xF000; jump['id'][4]=0x2000; # 2NNN 
   jump['masque'][5]= 0xF000; jump['id'][5]=0x3000; # 3XNN 
   jump['masque'][6]= 0xF000; jump['id'][6]=0x4000; # 4XNN 
   jump['masque'][7]= 0xF00F; jump['id'][7]=0x5000; # 5XY0 
   jump['masque'][8]= 0xF000; jump['id'][8]=0x6000; # 6XNN
   jump['masque'][9]= 0xF000; jump['id'][9]=0x7000; # 7XNN 
   jump['masque'][10]= 0xF00F; jump['id'][10]=0x8000; # 8XY0 
   jump['masque'][11]= 0xF00F; jump['id'][11]=0x8001; # 8XY1 
   jump['masque'][12]= 0xF00F; jump['id'][12]=0x8002; # 8XY2 
   jump['masque'][13]= 0xF00F; jump['id'][13]=0x8003; # BXY3 
   jump['masque'][14]= 0xF00F; jump['id'][14]=0x8004; # 8XY4 
   jump['masque'][15]= 0xF00F; jump['id'][15]=0x8005; # 8XY5 
   jump['masque'][16]= 0xF00F; jump['id'][16]=0x8006; # 8XY6 
   jump['masque'][17]= 0xF00F; jump['id'][17]=0x8007; # 8XY7 
   jump['masque'][18]= 0xF00F; jump['id'][18]=0x800E; # 8XYE 
   jump['masque'][19]= 0xF00F; jump['id'][19]=0x9000; # 9XY0 
   jump['masque'][20]= 0xF000; jump['id'][20]=0xA000; # ANNN 
   jump['masque'][21]= 0xF000; jump['id'][21]=0xB000; # BNNN 
   jump['masque'][22]= 0xF000; jump['id'][22]=0xC000; # CXNN 
   jump['masque'][23]= 0xF000; jump['id'][23]=0xD000; # DXYN 
   jump['masque'][24]= 0xF0FF; jump['id'][24]=0xE09E; # EX9E 
   jump['masque'][25]= 0xF0FF; jump['id'][25]=0xE0A1; # EXA1 
   jump['masque'][26]= 0xF0FF; jump['id'][26]=0xF007; # FX07 
   jump['masque'][27]= 0xF0FF; jump['id'][27]=0xF00A; # FX0A 
   jump['masque'][28]= 0xF0FF; jump['id'][28]=0xF015; # FX15 
   jump['masque'][29]= 0xF0FF; jump['id'][29]=0xF018; # FX18 
   jump['masque'][30]= 0xF0FF; jump['id'][30]=0xF01E; # FX1E 
   jump['masque'][31]= 0xF0FF; jump['id'][31]=0xF029; # FX29 
   jump['masque'][32]= 0xF0FF; jump['id'][32]=0xF033; # FX33 
   jump['masque'][33]= 0xF0FF; jump['id'][33]=0xF055; # FX55 
   jump['masque'][34]= 0xF0FF; jump['id'][34]=0xF065; # FX65
   return jump

jp=initialiserJump()

def recupererAction(opcode):
   resultat=None
   for action in range(1,NBROPCODE):
       resultat= jp['masque'][action]&opcode #On récupère les bits concernés par le test, l'identifiant de l'opcode
       if resultat == jp['id'][action]: #On a trouvé l'action à effectuer
          #print(hex(resultat),hex(jp['id'][action]),action)
          break #Plus la peine de continuer la boucle car la condition n'est vraie qu'une seule fois
   return action #on renvoie l'indice de l'action à effectuer

def interpreterOpcode(opcode):
   b3=(opcode&(0x0F00))>>8 #on prend les 4 bits représentant X
   b2=(opcode&(0x00F0))>>4 #idem pour Y
   b1=(opcode&(0x000F)) #les 4 bits de poids faible
   b4= recupererAction(opcode)
   
   #if b4==0:
      #Cet opcode n'est pas implémenté
   if b4==1:
      #00E0 : efface l'écran
      effacerEcran()
   elif b4==2:
      #00EE : revient du saut
      if cpu.nbrsaut>0:
         cpu.nbrsaut-=1
         cpu.pc=cpu.saut[cpu.nbrsaut]     
   elif b4==3:
      #1NNN : effectue un saut à l'adresse 1NNN
      cpu.pc=(b3<<8)+(b2<<4)+b1 #on prend le nombre NNN (pour le saut)
      cpu.pc-=2 #on verra pourquoi à la fin
      
   elif b4==4:
      #2NNN : appelle le sous-programme en NNN, mais on revient ensuite
      cpu.saut[cpu.nbrsaut]=cpu.pc #on reste là où on était
      if cpu.nbrsaut<15:
         cpu.nbrsaut+=1
      cpu.pc=(b3<<8)+(b2<<4)+b1 #on prend le nombre NNN (pour le saut)
      cpu.pc-=2 #on verra pourquoi à la fin
      
   elif b4==5:
      #3XNN saute l'instruction suivante si VX est égal à NN.
      if cpu.V[b3]==((b2<<4)+b1):
         cpu.pc+=2     
   elif b4==6:
      #4XNN saute l'instruction suivante si VX et NN ne sont pas égaux.
      if cpu.V[b3]!=((b2<<4)+b1):
         cpu.pc+=2
      
   elif b4==7:
      #5XY0 saute l'instruction suivante si VX et VY sont égaux.
      if cpu.V[b3]==cpu.V[b2]:
         cpu.pc+=2
      
   elif b4==8:
      #6XNN définit VX à NN.
      cpu.V[b3]=(b2<<4)+b1
   elif b4==9:
      #7XNN ajoute NN à VX.
      cpu.V[b3]+=(b2<<4)+b1
   elif b4==10:
      #8XY0 définit VX à la valeur de VY.
      cpu.V[b3]=cpu.V[b2]
   elif b4==11:
      #8XY1 définit VX à VX OR VY.
      cpu.V[b3]=cpu.V[b3]|cpu.V[b2]
   elif b4==12:
      #8XY2 définit VX à VX AND VY.
      cpu.V[b3]=cpu.V[b3]&cpu.V[b2]
   elif b4==13:
      #8XY3 définit VX à VX XOR VY.
      cpu.V[b3]=cpu.V[b3]^cpu.V[b2]
   elif b4==14:
     #8XY4 ajoute VY à VX. VF est mis à 1 quand il y
     #a un dépassement de mémoire (carry), et à 0 quand il n'y en pas.
      if cpu.V[b3]+cpu.V[b2]>255:
         cpu.V[0xF]=1 #cpu.V[15]
      else:
         cpu.V[0xF]=0 #cpu.V[15]
      cpu.V[b3]+=cpu.V[b2];
      
   elif b4==15:
     #8XY5 VY est soustraite de VX. VF est mis à 0
     #quand il y a un emprunt, et à 1 quand il n'y a en pas.
      if cpu.V[b3]<cpu.V[b2]:
         cpu.V[0xF]=0 #cpu.V[15]
      else:
         cpu.V[0xF]=1 #cpu.V[15]
      cpu.V[b3]-=cpu.V[b2]
      
   elif b4==16:
     #8XY6 décale (shift) VX à droite de 1 bit. VF
     #est fixé à la valeur du bit de poids faible de VX avant le décalage.
      cpu.V[0xF]=(cpu.V[b3]&(0x01))
      cpu.V[b3]=(cpu.V[b3]>>1)
      
   elif b4==17:
     #8XY7 VX = VY - VX. VF est mis à 0 quand il y a
     #un emprunt et à 1 quand il n'y en a pas.
      if cpu.V[b2]<cpu.V[b3]:
         cpu.V[0xF]=0 #cpu.V[15]
      else:
         cpu.V[0xF]=1 #cpu.V[15]
      cpu.V[b3]=cpu.V[b2]-cpu.V[b3]      
   elif b4==18:
     #8XYE décale (shift) VX à gauche de 1 bit. VF
     #est fixé à la valeur du bit de poids fort de VX avant le décalage.
      cpu.V[0xF]=(cpu.V[b3]>>7)
      cpu.V[b3]=(cpu.V[b3]<<1)     
   elif b4==19:
     #9XY0 saute l'instruction suivante si VX et VY ne sont pas égaux.
      if cpu.V[b3]!=cpu.V[b2]:
         cpu.pc+=2      
   elif b4==20:
     #ANNN affecte NNN à I.
      cpu.I=(b3<<8)+(b2<<4)+b1
   elif b4==21:
     #BNNN passe à l'adresse NNN + V0.
     cpu.pc=(b3<<8)+(b2<<4)+b1+cpu.V[0]
     cpu.pc-=2;
      
   elif b4==22:
     #CXNN définit VX à un nombre aléatoire inférieur à NN.
      cpu.V[b3]=random.randint(0,(b2<<4)+b1)
      #print(opcode&0X00FF,cpu.V[b3])
   elif b4==23:
     #DXYN dessine un sprite aux coordonnées (VX, VY).
     dessinerEcran(b1,b2,b3)
   elif b4==24:
     #EX9E saute l'instruction suivante si la clé stockée dans VX est pressée.
     if cpu.touche[cpu.V[b3]]==1:  #1 = pressé ; 0 = relâché
        cpu.pc+=2
   elif b4==25:
     #EXA1 saute l'instruction suivante si la clé stockée dans VX n'est pas pressée.
     #print(hex(b3))
     if cpu.touche[cpu.V[b3]]==0: #1 = pressé ; 0 = relâché
        cpu.pc+=2      
   elif b4==26:
     #FX07 définit VX à la valeur de la temporisation.
      cpu.V[b3]=cpu.compteurJeu
   elif b4==27:
     #FX0A attend l'appui sur une touche et la stocke ensuite dans VX.
     attendAppui(b3)
   elif b4==28:
      #FX15 définit la temporisation à VX.

      cpu.compteurJeu=cpu.V[b3]
   elif b4==29:
     #FX18 définit la minuterie sonore à VX.
      cpu.compteurSon=cpu.V[b3]
   elif b4==30:
     #FX1E ajoute VX a I. VF est mis à 1 quand il y a
     #overflow (I+VX>0xFFF), et à 0 si tel n'est pas le cas.
      if(cpu.I+cpu.V[b3])>0xFFF:
         cpu.V[0xF]=1
      else:
         cpu.V[0xF]=0;
      cpu.I+=cpu.V[b3]
   elif b4==31:
     #FX29 définit I à l'emplacement du caractère
     #stocké dans VX. Les caractères 0-F (en hexadécimal) sont représentés par une police 4x5.
      cpu.I=cpu.V[b3]*5
   elif b4==32:
     #FX33 stocke dans la mémoire le code décimal représentant VX (dans I, I+1, I+2).
      cpu.memoire[cpu.I]=int((cpu.V[b3]-cpu.V[b3]%100)/100)
      cpu.memoire[cpu.I+1]=int(((cpu.V[b3]-cpu.V[b3]%10)/10)%10)
      cpu.memoire[cpu.I+2]=cpu.V[b3]-cpu.memoire[cpu.I]*100-10*cpu.memoire[cpu.I+1]
      
   elif b4==33:
     #FX55 stocke V0 à VX en mémoire à partir de l'adresse I.
      for i in range(b3+1):
         cpu.memoire[cpu.I+i]=cpu.V[i]      
   elif b4==34:
     #FX65 remplit V0 à VX avec les valeurs de la mémoire à partir de l'adresse I.
      for i in range(b3+1):
         cpu.V[i] =cpu.memoire[cpu.I+i]        
   
   cpu.pc+=2 #on passe au prochain opcode


def dessinerEcran(b1,b2,b3):
   x=y=k=codage=j=decalage=0
   cpu.V[0xF]=0
   for k in range(b1):
       codage=cpu.memoire[cpu.I+k] #on récupère le codage de la ligne à dessiner
       y=(cpu.V[b2]+k)%L #on calcule l'ordonnée de la ligne à dessiner, on ne doit pas dépasser L
       decalage=7
       #print(bin(codage),k,y)
       for j in range(8):
         x=(cpu.V[b3]+j)%l #on calcule l'abscisse, on ne doit pas dépasser l
         #print(bin(codage),pixel[x][y].couleur,x,y)
         if((codage)&(0x1<<decalage))!=0: #on récupère le bit correspondant
           #si c'est blanc
           if(pixel[x][y].couleur==BLANC): #le pixel était blanc
              pixel[x][y].couleur=NOIR #on l'éteint
              cpu.V[0xF]=1 #il y a donc collusion
           else: #sinon
              pixel[x][y].couleur=BLANC #on l'allume
         decalage-=1

def chargerFont():
   cpu.memoire[0]=0xF0;cpu.memoire[1]=0x90;cpu.memoire[2]=0x90
   cpu.memoire[3]=0x90;cpu.memoire[4]=0xF0
   # O
   cpu.memoire[5]=0x20;cpu.memoire[6]=0x60;cpu.memoire[7]=0x20
   cpu.memoire[8]=0x20;cpu.memoire[9]=0x70
   # 1
   cpu.memoire[10]=0xF0;cpu.memoire[11]=0x10;cpu.memoire[12]=0xF0
   cpu.memoire[13]=0x80;cpu.memoire[14]=0xF0
   # 2
   cpu.memoire[15]=0xF0;cpu.memoire[16]=0x10;cpu.memoire[17]=0xF0
   cpu.memoire[18]=0x10;cpu.memoire[19]=0xF0
   # 3
   cpu.memoire[20]=0x90;cpu.memoire[21]=0x90;cpu.memoire[22]=0xF0
   cpu.memoire[23]=0x10;cpu.memoire[24]=0x10
   # 4
   cpu.memoire[25]=0xF0;cpu.memoire[26]=0x80;cpu.memoire[27]=0xF0
   cpu.memoire[28]=0x10;cpu.memoire[29]=0xF0
   # 5
   cpu.memoire[30]=0xF0;cpu.memoire[31]=0x80;cpu.memoire[32]=0xF0
   cpu.memoire[33]=0x90;cpu.memoire[34]=0xF0
   # 6
   cpu.memoire[35]=0xF0;cpu.memoire[36]=0x10;cpu.memoire[37]=0x20
   cpu.memoire[38]=0x40;cpu.memoire[39]=0x40
   # 7
   cpu.memoire[40]=0xF0;cpu.memoire[41]=0x90;cpu.memoire[42]=0xF0
   cpu.memoire[43]=0x90;cpu.memoire[44]=0xF0
   # 8
   cpu.memoire[45]=0xF0;cpu.memoire[46]=0x90;cpu.memoire[47]=0xF0
   cpu.memoire[48]=0x10;cpu.memoire[49]=0xF0
   # 9
   cpu.memoire[50]=0xF0;cpu.memoire[51]=0x90;cpu.memoire[52]=0xF0
   cpu.memoire[53]=0x90;cpu.memoire[54]=0x90
   # A
   cpu.memoire[55]=0xE0;cpu.memoire[56]=0x90;cpu.memoire[57]=0xE0
   cpu.memoire[58]=0x90;cpu.memoire[59]=0xE0
   # B
   cpu.memoire[60]=0xF0;cpu.memoire[61]=0x80;cpu.memoire[62]=0x80
   cpu.memoire[63]=0x80;cpu.memoire[64]=0xF0
   # C
   cpu.memoire[65]=0xE0;cpu.memoire[66]=0x90;cpu.memoire[67]=0x90
   cpu.memoire[68]=0x90;cpu.memoire[69]=0xE0
   # D
   cpu.memoire[70]=0xF0;cpu.memoire[71]=0x80;cpu.memoire[72]=0xF0
   cpu.memoire[73]=0x80;cpu.memoire[74]=0xF0
   # E
   cpu.memoire[75]=0xF0;cpu.memoire[76]=0x80;cpu.memoire[77]=0xF0
   cpu.memoire[78]=0x80;cpu.memoire[79]=0x80
   # F                                                                        

def chargerJeu(nomJeu):
   donnees=0
   with open(nomJeu,'rb')as fichier:
      donnees=fichier.read()
      adresse_index=ADRESSEDEBUT
      adress_arret=3743
      for valeur in donnees:
          cpu.memoire[adresse_index]=valeur
          #if adresse_index<=adress_arret:
          adresse_index+=1
          #else:
             #break
   if donnees!=0:
      return 1
   else:
      return 0
   
if __name__ == "__main__":   
    main()
