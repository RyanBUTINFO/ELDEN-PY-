import pygame
import random
import math
import os

pygame.init()
LARGEUR, HAUTEUR = 1024, 576
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("ELDEN PY: BOSS FINAL (Version Grand Ecran)")
horloge = pygame.time.Clock()

BOSS_REGARDE_DROITE = True

pygame.mixer.init()

NOIR = (5, 5, 8)
FOND_HAUT = (20, 10, 25)
FOND_BAS = (5, 5, 10)
ROUGE_SANG = (160, 10, 10)
OR = (200, 150, 50)
ARGENT = (150, 155, 160)
VERT_ENDURANCE = (40, 180, 80)
FOND_ENDURANCE = (20, 60, 20)
COULEUR_INCANTATION = (255, 140, 0)

# --- CORRECTION CHEMIN ---
chemin_base = os.path.dirname(os.path.abspath(__file__))

MUSIC_MENU = os.path.join(chemin_base, "Firelink Shrine - Dark Souls Soundtrack 03.mp3")
MUSIC_PHASE1 = os.path.join(chemin_base, "Taurus Demon - Dark Souls Soundtrack 04.mp3")
MUSIC_PHASE2 = os.path.join(chemin_base, "Bell Gargoyles - Dark Souls Soundtrack 05.mp3")

def jouer_musique(chemin, volume):
    if os.path.exists(chemin):
        try:
            pygame.mixer.music.load(chemin)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"Erreur musique: {e}")

def obtenir_police(taille):
    chemin_police = os.path.join(chemin_base, "souls_font.ttf")
    if os.path.exists(chemin_police):
        return pygame.font.Font(chemin_police, taille)
    else:
        return pygame.font.SysFont("serif", taille, bold=True)

def charger_et_redimensionner(chemin, largeur, hauteur, est_feuille=False):
    if not os.path.exists(chemin):
        s = pygame.Surface((largeur, hauteur))
        s.fill((255, 0, 255))
        return s
    try:
        img = pygame.image.load(chemin).convert_alpha()
        if est_feuille:
            h = img.get_height()
            img = img.subsurface((0, 0, h, h))
        return pygame.transform.scale(img, (largeur, hauteur))
    except Exception as e:
        print(f"ERREUR CHARGEMENT: {e}")
        s = pygame.Surface((largeur, hauteur))
        s.fill((255, 0, 255))
        return s

chemin_boutons = os.path.join(chemin_base, "buttons") 
chemin_boss_base = os.path.join(chemin_base, "boss_base") 
chemin_boss_attaque = os.path.join(chemin_base, "boss")
chemin_boss_final = os.path.join(chemin_base, "finalboss")
chemin_frames_menu = os.path.join(chemin_base, "frames")
chemin_valk = os.path.join(chemin_base, "VALK") 
chemin_chev = os.path.join(chemin_base, "CHEVALIER")
chemin_sang = os.path.join(chemin_base, "blood")
chemin_technique = os.path.join(chemin_base, "technique")
chemin_disciple = os.path.join(chemin_base, "disciple")

IMG_CHEVALIER_DEFAUT = charger_et_redimensionner(os.path.join(chemin_base, "chevalier.png"), 45, 65)
IMG_VALKYRIE_DEFAUT = charger_et_redimensionner(os.path.join(chemin_base, "valk.png"), 45, 65)

IMG_FEU = charger_et_redimensionner(os.path.join(chemin_base, "fireball sheet.png"), 100, 75, est_feuille=True)

IMG_EPEE_BRUTE = charger_et_redimensionner(os.path.join(chemin_base, "sword.png"), 25, 80)
IMG_EPEE = pygame.transform.rotate(IMG_EPEE_BRUTE, -90)

IMG_UI_PV = charger_et_redimensionner(os.path.join(chemin_boutons, "buttons_pv.png"), 200, 20)
IMG_UI_ENDURANCE = charger_et_redimensionner(os.path.join(chemin_boutons, "buttons_stamina.png"), 150, 8)
IMG_UI_BOSS = charger_et_redimensionner(os.path.join(chemin_boutons, "buttons_boss.png"), 600, 15)

IMAGES_BOSS_BASE = []
for i in range(1, 9):
    chemin_long = os.path.join(chemin_boss_base, f"boss_base{i}.png")
    chemin_court = os.path.join(chemin_boss_base, f"{i}.png")
    if os.path.exists(chemin_long):
        img = charger_et_redimensionner(chemin_long, 120, 150)
    else:
        img = charger_et_redimensionner(chemin_court, 120, 150)
    IMAGES_BOSS_BASE.append(img)

IMAGES_BOSS_ATTAQUE = []
for i in range(1, 10): 
    nom_fichier = f"boss_lvl{i}.png"
    chemin = os.path.join(chemin_boss_attaque, nom_fichier)
    img = charger_et_redimensionner(chemin, 120, 150)
    IMAGES_BOSS_ATTAQUE.append(img)

IMAGES_BOSS_FINAL = []
for i in range(1, 9):
    nom_fichier = f"finalboss_base{i}.png"
    chemin = os.path.join(chemin_boss_final, nom_fichier)
    img = charger_et_redimensionner(chemin, 120, 150)
    IMAGES_BOSS_FINAL.append(img)

IMAGES_FOND_MENU = []
for i in range(1, 13): 
    nom_fichier = f"Frame {i}.png" 
    chemin = os.path.join(chemin_frames_menu, nom_fichier)
    if not os.path.exists(chemin):
        nom_sans_espace = f"Frame{i}.png"
        chemin = os.path.join(chemin_frames_menu, nom_sans_espace)
    img = charger_et_redimensionner(chemin, LARGEUR, HAUTEUR) 
    IMAGES_FOND_MENU.append(img)

IMGS_VALKYRIE = {}
if os.path.exists(chemin_valk):
    for i in range(1, 8):
        IMGS_VALKYRIE[i] = charger_et_redimensionner(os.path.join(chemin_valk, f"valk{i}.png"), 45, 65)

IMGS_CHEVALIER = {}
if os.path.exists(chemin_chev):
    for i in range(1, 8):
        IMGS_CHEVALIER[i] = charger_et_redimensionner(os.path.join(chemin_chev, f"chevalier{i}.png"), 45, 65)

IMG_MENU_CHEVALIER = IMGS_CHEVALIER.get(1, IMG_CHEVALIER_DEFAUT)
IMG_MENU_VALKYRIE = IMGS_VALKYRIE.get(1, IMG_VALKYRIE_DEFAUT)

IMAGES_SANG = []
for i in range(1, 16):
    img = charger_et_redimensionner(os.path.join(chemin_sang, f"blood_lvl{i}.png"), 100, 100) 
    IMAGES_SANG.append(img)

IMAGES_TECHNIQUE = []
for i in range(1, 19):
    nom_fichier = f"technique_lvl{i}.png"
    chemin = os.path.join(chemin_technique, nom_fichier)
    img = charger_et_redimensionner(chemin, 100, 130) 
    IMAGES_TECHNIQUE.append(img)

IMAGES_DISCIPLE = []
for i in range(1, 12):
    nom_fichier = f"disciple_lvl{i}.png"
    chemin = os.path.join(chemin_disciple, nom_fichier)
    img = charger_et_redimensionner(chemin, 100, 120)
    IMAGES_DISCIPLE.append(img)

class Disciple:
    def __init__(self, boss):
        self.boss = boss
        self.index = 0
        self.etat = "inactif"
        self.x = 0
        self.y = 0
        self.cible_x = 0
        self.sol_y = 0

    def activer(self, cible_x, sol_y):
        self.etat = "apparition"
        self.index = 0
        self.cible_x = cible_x
        self.sol_y = sol_y
        self.x = self.boss.rect.centerx - 80 
        self.y = self.boss.rect.y - 20

    def mettre_a_jour(self):
        monstre = None
        vitesse = 0.4

        if self.etat == "inactif":
            return None

        if self.etat == "apparition":
            self.index += vitesse
            if self.index >= 10:
                self.index = 10
                monstre = MonstreSol(self.cible_x, self.sol_y)
                self.etat = "disparition"

        elif self.etat == "disparition":
            self.index -= vitesse
            if self.index <= 0:
                self.index = 0
                self.etat = "inactif"

        return monstre

    def dessiner(self, surface):
        if self.etat != "inactif":
            idx = int(self.index)
            if idx >= len(IMAGES_DISCIPLE): idx = len(IMAGES_DISCIPLE) - 1
            img = IMAGES_DISCIPLE[idx]
            
            if not self.boss.regarde_gauche:
                img = pygame.transform.flip(img, True, False)
            surface.blit(img, (self.x, self.y))

class MonstreSol:
    def __init__(self, x, y_sol):
        self.rect = pygame.Rect(x - 50, y_sol - 130, 100, 130)
        self.index_image = 0
        self.fini = False
        self.a_touche = False

    def mettre_a_jour(self):
        self.index_image += 0.4 
        if self.index_image >= len(IMAGES_TECHNIQUE):
            self.fini = True

    def dessiner(self, surface):
        if not self.fini:
            img = IMAGES_TECHNIQUE[int(self.index_image)]
            surface.blit(img, (self.rect.x, self.rect.y))

    def obtenir_hitbox(self):
        if 6 < self.index_image < 14 and not self.a_touche:
            return pygame.Rect(self.rect.x + 20, self.rect.y + 20, 60, 80)
        return None

class EffetSang:
    def __init__(self, x, y):
        self.x = x + random.randint(-20, 20)
        self.y = y + random.randint(-20, 20)
        self.index_image = 0
        self.fini = False

    def mettre_a_jour(self):
        self.index_image += 0.5 
        if self.index_image >= len(IMAGES_SANG):
            self.fini = True

    def dessiner(self, surface):
        if not self.fini:
            surface.blit(IMAGES_SANG[int(self.index_image)], (self.x - 50, self.y - 50))

class Particule:
    def __init__(self, x, y, type_p):
        self.x = x
        self.y = y
        self.type = type_p
        self.vie = random.randint(20, 50)
        self.vie_max = self.vie
        if type_p == "sang":
            self.vx = random.uniform(-4, 4)
            self.vy = random.uniform(-5, -2)
            self.couleur = ROUGE_SANG
            self.taille = random.randint(2, 4)
            self.gravite = 0.4
        elif type_p == "cendre":
            self.vx = random.uniform(-1, 1)
            self.vy = random.uniform(0.5, 1.5)
            self.couleur = (100, 100, 110)
            self.taille = random.randint(1, 2)
            self.gravite = 0

    def mettre_a_jour(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravite
        self.vie -= 1

    def dessiner(self, surface):
        if self.vie > 0:
            alpha = int(255 * (self.vie / self.vie_max))
            s = pygame.Surface((self.taille, self.taille), pygame.SRCALPHA)
            s.fill((*self.couleur, alpha))
            surface.blit(s, (self.x, self.y))

class BouleDeFeu:
    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(x, y, 100, 75)
        self.vitesse = 8 * direction 
        self.image = IMG_FEU
        if direction == 1:
            self.image = pygame.transform.flip(IMG_FEU, True, False)
        self.vie = 120

    def mettre_a_jour(self):
        self.rect.x += self.vitesse
        self.vie -= 1

    def dessiner(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class Joueur:
    def __init__(self, genre, difficulte):
        self.largeur, self.hauteur = 45, 65
        self.rect = pygame.Rect(100, 415, self.largeur, self.hauteur)
        self.genre = genre
        self.regarde_droite = True
        self.chrono_anim = 0
        self.index_image = 0
        self.recul_x = 0
        
        if self.genre == "homme":
            if 1 in IMGS_CHEVALIER:
                self.img_victoire = IMGS_CHEVALIER[1]
                self.imgs_gauche = [IMGS_CHEVALIER[2], IMGS_CHEVALIER[3], IMGS_CHEVALIER[4]]
                self.imgs_droite = [IMGS_CHEVALIER[5], IMGS_CHEVALIER[6], IMGS_CHEVALIER[7]]
                self.utiliser_anim = True
            else:
                self.image_originale = IMG_CHEVALIER_DEFAUT
                self.utiliser_anim = False
        else:
            if 1 in IMGS_VALKYRIE:
                self.img_victoire = IMGS_VALKYRIE[1]
                self.imgs_gauche = [IMGS_VALKYRIE[2], IMGS_VALKYRIE[3], IMGS_VALKYRIE[4]]
                self.imgs_droite = [IMGS_VALKYRIE[5], IMGS_VALKYRIE[6], IMGS_VALKYRIE[7]]
                self.utiliser_anim = True
            else:
                self.image_originale = IMG_VALKYRIE_DEFAUT
                self.utiliser_anim = False
        
        if difficulte == "noob":
            self.pv_max = 200
            self.mult_degats = 1.5
            self.regen_endurance = 0.8
        elif difficulte == "pro":
            self.pv_max = 50
            self.mult_degats = 0.8
            self.regen_endurance = 0.4
        else:
            self.pv_max = 100
            self.mult_degats = 1.0
            self.regen_endurance = 0.6
            
        self.pv = self.pv_max
        self.endurance = 100
        self.endurance_max = 100
        self.vitesse = 5
        self.en_dash = False
        self.chrono_dash = 0
        self.invincible = 0
        self.z = 0
        self.vel_z = 0
        self.gravite = 0.8
        self.en_saut = False
        self.en_mouvement = False
        
        self.attaque_en_cours = False
        self.duree_attaque = 12 
        self.chrono_attaque = 0
        self.delai_attaque = 0  

    def deplacer(self, touches):
        if self.delai_attaque > 0:
            self.delai_attaque -= 1
        
        if not self.en_dash and not self.attaque_en_cours and not self.en_saut:
            if self.endurance < 100:
                self.endurance += self.regen_endurance

        if touches[pygame.K_SPACE] and not self.en_saut and self.endurance > 10:
            self.en_saut = True
            self.vel_z = 15
            self.endurance -= 10
        
        if self.en_saut:
            self.z += self.vel_z
            self.vel_z -= self.gravite
            if self.z <= 0:
                self.z = 0
                self.vel_z = 0
                self.en_saut = False

        if touches[pygame.K_LSHIFT] and self.endurance > 25 and self.chrono_dash == 0:
            self.en_dash = True
            self.chrono_dash = 20
            self.invincible = 25
            self.endurance -= 25
            self.vitesse = 12 

        if self.en_dash:
            self.chrono_dash -= 1
            if self.chrono_dash <= 0:
                self.en_dash = False
                self.vitesse = 5
        else:
            self.vitesse = 5

        dx = 0
        self.en_mouvement = False
        if not self.en_dash:
            if touches[pygame.K_q] or touches[pygame.K_LEFT]:
                dx = -self.vitesse
                self.regarde_droite = False
                self.en_mouvement = True
            if touches[pygame.K_d] or touches[pygame.K_RIGHT]:
                dx = self.vitesse
                self.regarde_droite = True
                self.en_mouvement = True
        else:
            dx = self.vitesse if self.regarde_droite else -self.vitesse

        dx += self.recul_x
        if self.recul_x > 0: self.recul_x -= 1
        elif self.recul_x < 0: self.recul_x += 1
        
        if touches[pygame.K_e] and self.endurance > 20 and not self.attaque_en_cours and self.delai_attaque == 0 and not self.en_dash:
            self.attaque_en_cours = True
            self.chrono_attaque = self.duree_attaque
            self.delai_attaque = 45
            self.endurance -= 20

        if self.attaque_en_cours:
            self.chrono_attaque -= 1
            if self.chrono_attaque <= 0:
                self.attaque_en_cours = False

        if self.invincible > 0:
            self.invincible -= 1
        
        self.rect.x += dx
        self.rect.x = max(0, min(LARGEUR - self.largeur, self.rect.x)) 

    def dessiner(self, surface, boss_vaincu):
        if self.invincible > 0 and self.invincible % 4 == 0:
            return
        
        largeur_ombre = self.largeur - int(self.z / 2)
        if largeur_ombre > 5:
            pygame.draw.ellipse(surface, (0,0,0,80), (self.rect.centerx - largeur_ombre//2, self.rect.bottom - 5, largeur_ombre, 6))

        image_a_dessiner = None
        if self.utiliser_anim:
            if boss_vaincu:
                image_a_dessiner = self.img_victoire
            else:
                self.chrono_anim += 1
                if self.chrono_anim > 5:
                    self.index_image += 1
                    self.chrono_anim = 0
                
                if self.regarde_droite:
                    frames = self.imgs_droite
                    idx = self.index_image % len(frames)
                    image_a_dessiner = frames[idx]
                else:
                    frames = self.imgs_gauche
                    idx = self.index_image % len(frames)
                    image_a_dessiner = frames[idx]
        else:
            image_a_dessiner = self.image_originale
            if self.regarde_droite and self.genre == "homme":
                image_a_dessiner = pygame.transform.flip(image_a_dessiner, True, False)
            elif self.regarde_droite:
                image_a_dessiner = pygame.transform.flip(image_a_dessiner, True, False)

        surface.blit(image_a_dessiner, (self.rect.x, self.rect.y - self.z))
            
        if self.attaque_en_cours:
            cy = self.rect.centery - self.z
            if self.regarde_droite:
                surface.blit(IMG_EPEE, (self.rect.right - 20, cy - 10))
            else:
                epee_retournee = pygame.transform.flip(IMG_EPEE, True, False)
                surface.blit(epee_retournee, (self.rect.left - 60, cy - 10))

    def obtenir_hitbox(self):
        if self.attaque_en_cours and 0 < self.chrono_attaque < 12:
            if self.regarde_droite:
                return pygame.Rect(self.rect.right, self.rect.y, 60, 60)
            else:
                return pygame.Rect(self.rect.left - 60, self.rect.y, 60, 60)
        return None

class Boss:
    def __init__(self, difficulte):
        self.largeur, self.hauteur = 120, 150
        self.rect = pygame.Rect(600, 330, self.largeur, self.hauteur)
        
        self.frames_base = IMAGES_BOSS_BASE
        self.frames_attaque = IMAGES_BOSS_ATTAQUE
        self.frames_final = IMAGES_BOSS_FINAL
        
        self.index_image = 0
        self.chrono_anim = 0
        self.vitesse_anim = 5       
        
        if difficulte == "noob":
            self.pv_max = 400
            self.freq_tir = 180
        elif difficulte == "pro":
            self.pv_max = 1200
            self.freq_tir = 80
        else:
            self.pv_max = 800
            self.freq_tir = 120

        self.pv = self.pv_max
        self.phase = 1 
        self.etat = "repos"
        self.recuperation = 0
        self.chrono_tir = 0
        self.chrono_flash = 0
        self.regarde_gauche = True
        self.chrono_incantation = 0
        self.projectiles = []
        self.a_tire = False
        
        self.chrono_resurrection = 0
        self.delai_technique = 200
        
        self.chrono_prepa_technique = 0
        
        self.disciple = Disciple(self)

    def lancer_transition_phase2(self):
        self.etat = "resurrection"
        self.chrono_resurrection = 180 
        self.pv = 0

    def mettre_a_jour_animation(self):
        self.chrono_anim += 1
        vitesse = 4 if self.etat == "incantation" else 5
        if self.chrono_anim >= vitesse:
            self.chrono_anim = 0
            self.index_image += 1
            
            if self.etat == "incantation":
                frames = self.frames_final if self.phase == 2 else self.frames_attaque
                if self.phase == 2: 
                     self.index_image = self.index_image % len(frames)
                else:
                    if self.index_image >= len(frames):
                        self.etat = "repos"
                        self.index_image = 0
                        self.a_tire = False
                        
            elif self.etat == "attaque":
                # Utiliser frames_attaque pour l'attaque ou frames_final si Phase 2
                frames = self.frames_final if self.phase == 2 else self.frames_attaque
                if self.index_image >= len(frames):
                    self.etat = "repos"
                    self.index_image = 0
                    
            else:
                set_actuel = self.frames_final if self.phase == 2 else self.frames_base
                self.index_image = self.index_image % len(set_actuel)

    def mettre_a_jour(self, joueur):
        corps_a_corps = False
        nouveau_monstre = None
        
        # Le disciple vit sa vie indépendamment du Boss en phase 2
        if self.phase == 2:
            nouveau_monstre = self.disciple.mettre_a_jour()
            self.delai_technique -= 1
            if self.delai_technique <= 0:
                self.disciple.activer(joueur.rect.centerx, joueur.rect.bottom)
                self.delai_technique = 250

        if self.etat == "resurrection":
            self.chrono_resurrection -= 1
            if self.chrono_resurrection <= 0:
                self.phase = 2
                self.pv = self.pv_max
                self.etat = "repos"
                self.freq_tir = max(30, self.freq_tir - 30) 
            return corps_a_corps, nouveau_monstre

        self.mettre_a_jour_animation()
        centre_soi = self.rect.centerx
        dist = abs(centre_soi - joueur.rect.centerx)
        self.regarde_gauche = centre_soi > joueur.rect.centerx

        if self.recuperation > 0: self.recuperation -= 1
        if self.chrono_flash > 0: self.chrono_flash -= 1
        
        # Le Boss fait ses actions s'il n'est pas déjà occupé
        if self.etat in ["repos", "poursuite"]:
            self.chrono_tir += 1
            if self.chrono_tir > self.freq_tir and dist > 150:
                self.chrono_tir = 0
                self.etat = "incantation"
                self.index_image = 0
                self.chrono_anim = 0
                self.a_tire = False
                if self.phase == 2: self.chrono_incantation = 40 
                return corps_a_corps, nouveau_monstre

            if dist < 100 and self.recuperation == 0:
                self.etat = "attaque"
                self.index_image = 0
                self.recuperation = 100
                corps_a_corps = True
                return corps_a_corps, nouveau_monstre
            elif dist > 80:
                self.etat = "poursuite"
                pas = 2
                if self.regarde_gauche:
                    self.rect.x -= pas
                else:
                    self.rect.x += pas
            else:
                self.etat = "repos"

        if self.etat == "incantation":
            if self.phase == 1:
                if self.index_image == 4 and not self.a_tire:
                    direction = -1 if self.regarde_gauche else 1
                    self.projectiles.append(BouleDeFeu(self.rect.centerx, self.rect.centery, direction))
                    self.a_tire = True
            else:
                self.chrono_incantation -= 1
                if self.chrono_incantation == 20: 
                     direction = -1 if self.regarde_gauche else 1
                     self.projectiles.append(BouleDeFeu(self.rect.centerx, self.rect.centery, direction))
                if self.chrono_incantation <= 0: self.etat = "repos"
        
        return corps_a_corps, nouveau_monstre

    def mettre_a_jour_projectiles(self):
        for p in self.projectiles:
            p.mettre_a_jour()
        self.projectiles = [p for p in self.projectiles if p.vie > 0]

    def dessiner(self, surface):
        if self.phase == 2:
            self.disciple.dessiner(surface)
            frames = self.frames_final
        else:
            if self.etat == "incantation" or self.etat == "attaque":
                frames = self.frames_attaque
            else:
                frames = self.frames_base
            
        if self.index_image >= len(frames):
            self.index_image = 0
        img_courante = frames[self.index_image]
        
        doit_retourner = self.regarde_gauche if BOSS_REGARDE_DROITE else not self.regarde_gauche
        img = pygame.transform.flip(img_courante, True, False) if doit_retourner else img_courante
        
        offset_x = random.randint(-2, 2) if self.etat == "incantation" else 0
        if self.etat == "resurrection":
            offset_x = random.randint(-5, 5) 
            
        surface.blit(img, (self.rect.x + offset_x, self.rect.y))
        for p in self.projectiles:
            p.dessiner(surface)

def dessiner_fond(surface):
    for y in range(HAUTEUR):
        ratio = y / HAUTEUR
        r = int(FOND_HAUT[0] * (1-ratio) + FOND_BAS[0] * ratio)
        g = int(FOND_HAUT[1] * (1-ratio) + FOND_BAS[1] * ratio)
        b = int(FOND_HAUT[2] * (1-ratio) + FOND_BAS[2] * ratio)
        pygame.draw.line(surface, (r,g,b), (0,y), (LARGEUR,y))
    pygame.draw.rect(surface, (15, 15, 20), (0, 480, LARGEUR, 96)) 

def dessiner_item_menu(surface, texte, x_centre, y_depart, img):
    police = obtenir_police(25) 
    rendu = police.render(texte, True, ARGENT)
    surface.blit(rendu, (x_centre - rendu.get_width()//2, y_depart))
    surface.blit(img, (x_centre - img.get_width()//2, y_depart + 50))

def dessiner_texte_centre(surface, texte, y, taille, couleur): 
    police = obtenir_police(taille) 
    rendu = police.render(texte, True, couleur)
    surface.blit(rendu, (LARGEUR//2 - rendu.get_width()//2, y))

def dessiner_ecran_touches(surface, volume):
    dessiner_texte_centre(surface, "COMMANDES", 50, 60, OR)
    dessiner_texte_centre(surface, "DEPLACEMENT : Q / D  ou  FLECHES", 150, 30, ARGENT)
    dessiner_texte_centre(surface, "SAUT : ESPACE", 200, 30, ARGENT)
    dessiner_texte_centre(surface, "ATTAQUE : E", 250, 30, ARGENT)
    dessiner_texte_centre(surface, "DASH (ESQUIVE) : SHIFT GAUCHE", 300, 30, ARGENT)
    
    dessiner_texte_centre(surface, "VOLUME : + / -", 350, 30, ARGENT)
    dessiner_texte_centre(surface, "COUPER SON : M", 390, 30, ARGENT)
    
    largeur_barre = 200
    remplissage = int(largeur_barre * volume)
    pygame.draw.rect(surface, (50, 50, 50), (LARGEUR//2 - 100, 430, largeur_barre, 20))
    pygame.draw.rect(surface, OR, (LARGEUR//2 - 100, 430, remplissage, 20))
    pygame.draw.rect(surface, ARGENT, (LARGEUR//2 - 100, 430, largeur_barre, 20), 2)
    
    dessiner_texte_centre(surface, "RETOUR : ENTREE", 500, 25, ROUGE_SANG)

def dessiner_hud(surface, joueur, boss):
    ratio_pv = joueur.pv / joueur.pv_max
    largeur_pv = max(0, int(200 * ratio_pv))
    pygame.draw.rect(surface, (50, 0, 0), (20, 20, 200, 20))
    if largeur_pv > 0:
        surface.blit(IMG_UI_PV, (20, 20), area=pygame.Rect(0, 0, largeur_pv, 20))
    pygame.draw.rect(surface, OR, (20, 20, 200, 20), 2)
    
    ratio_endurance = joueur.endurance / 100
    largeur_endurance = max(0, int(150 * ratio_endurance))
    pygame.draw.rect(surface, (20, 50, 20), (20, 45, 150, 8))
    if largeur_endurance > 0:
        surface.blit(IMG_UI_ENDURANCE, (20, 45), area=pygame.Rect(0, 0, largeur_endurance, 8))
    
    if boss.pv > 0 or boss.etat == "resurrection":
        ratio_boss = boss.pv / boss.pv_max
        largeur_boss = max(0, int(600 * ratio_boss))
        rect_x = LARGEUR//2 - 300
        rect_y = HAUTEUR - 40
        pygame.draw.rect(surface, (30, 0, 0), (rect_x, rect_y, 600, 15))
        if largeur_boss > 0:
            surface.blit(IMG_UI_BOSS, (rect_x, rect_y), area=pygame.Rect(0, 0, largeur_boss, 15))
        pygame.draw.rect(surface, OR, (rect_x, rect_y, 600, 15), 2)
        
        nom = "SORCIER DU FLEAU" if boss.phase == 1 else "ARCHIMAGE DU NEANT"
        couleur = ARGENT if boss.phase == 1 else ROUGE_SANG
        police = obtenir_police(18)
        surface.blit(police.render(nom, True, couleur), (rect_x + 5, rect_y - 22))

def dessiner_ecran_titre(surface):
    police_grande = obtenir_police(80)
    police_petite = obtenir_police(25)
    ombre_titre = police_grande.render("ELDEN PY", True, NOIR)
    surface.blit(ombre_titre, (LARGEUR//2 - ombre_titre.get_width()//2 + 3, 100 + 3))
    titre = police_grande.render("ELDEN PY", True, OR)
    surface.blit(titre, (LARGEUR//2 - titre.get_width()//2, 100))
    if pygame.time.get_ticks() % 1000 < 500:
        msg = police_petite.render("- Appuyez sur Entree -", True, ARGENT)
        surface.blit(msg, (LARGEUR//2 - msg.get_width()//2, 300))

def main():
    etat = "INTRODUCTION"
    volume_general = 0.5
    derrnier_volume = 0.5
    jouer_musique(MUSIC_MENU, volume_general)
    genre_choisi = "homme"
    difficulte_choisie = "normal"
    joueur = None
    boss = None
    particules = []
    effets_sang = []
    attaques_sol = []
    secousse = 0
    jeu_fini = False
    victoire = False
    
    index_menu = 0
    chrono_menu = 0

    en_cours = True
    while en_cours:
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                en_cours = False
            
            if etat == "INTRODUCTION":
                if evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_RETURN:
                    etat = "MENU_GENRE"

            elif etat == "MENU_GENRE":
                if evenement.type == pygame.KEYDOWN:
                    if evenement.key == pygame.K_1:
                        genre_choisi = "homme"
                        etat = "MENU_DIFFICULTE"
                    elif evenement.key == pygame.K_2:
                        genre_choisi = "femme"
                        etat = "MENU_DIFFICULTE"
                    elif evenement.key == pygame.K_3:
                        etat = "MENU_TOUCHES"

            elif etat == "MENU_TOUCHES":
                if evenement.type == pygame.KEYDOWN:
                    if evenement.key == pygame.K_RETURN or evenement.key == pygame.K_ESCAPE:
                        etat = "MENU_GENRE"
                    elif evenement.key == pygame.K_PLUS or evenement.key == pygame.K_KP_PLUS or evenement.key == pygame.K_EQUALS:
                        volume_general = min(1.0, volume_general + 0.1)
                        pygame.mixer.music.set_volume(volume_general)
                    elif evenement.key == pygame.K_MINUS or evenement.key == pygame.K_KP_MINUS or evenement.key == pygame.K_6:
                        volume_general = max(0.0, volume_general - 0.1)
                        pygame.mixer.music.set_volume(volume_general)
                    elif evenement.key == pygame.K_m:
                        if volume_general > 0:
                            derrnier_volume = volume_general
                            volume_general = 0
                        else:
                            volume_general = derrnier_volume
                        pygame.mixer.music.set_volume(volume_general)

            elif etat == "MENU_DIFFICULTE":
                if evenement.type == pygame.KEYDOWN:
                    if evenement.key == pygame.K_ESCAPE:
                        etat = "MENU_GENRE"
                    elif evenement.key == pygame.K_1: difficulte_choisie = "noob"
                    elif evenement.key == pygame.K_2: difficulte_choisie = "normal"
                    elif evenement.key == pygame.K_3: difficulte_choisie = "pro"
                    if evenement.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                        joueur = Joueur(genre_choisi, difficulte_choisie)
                        boss = Boss(difficulte_choisie)
                        etat = "JEU"
                        jouer_musique(MUSIC_PHASE1, volume_general)
            elif etat == "JEU":
                if (jeu_fini or victoire) and evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_RETURN:
                    etat = "INTRODUCTION"
                    joueur = None
                    boss = None
                    particules = []
                    effets_sang = []
                    attaques_sol = []
                    secousse = 0
                    jeu_fini = False
                    victoire = False
                    jouer_musique(MUSIC_MENU, volume_general)

        ecran.fill(NOIR)

        if etat == "INTRODUCTION":
            if IMAGES_FOND_MENU:
                chrono_menu += 1
                if chrono_menu > 5:
                    index_menu = (index_menu + 1) % len(IMAGES_FOND_MENU)
                    chrono_menu = 0
                ecran.blit(IMAGES_FOND_MENU[index_menu], (0,0))
            else:
                dessiner_fond(ecran)
            dessiner_ecran_titre(ecran)

        elif etat == "MENU_GENRE":
            dessiner_fond(ecran)
            dessiner_texte_centre(ecran, "CHOISIS TON DESTIN", 80, 50, OR)
            dessiner_item_menu(ecran, "[1] CHEVALIER", 250, 180, IMG_MENU_CHEVALIER)
            dessiner_item_menu(ecran, "[2] VALKYRIE", 700, 180, IMG_MENU_VALKYRIE)
            dessiner_texte_centre(ecran, "[3] COMMANDES", 450, 25, ARGENT)

        elif etat == "MENU_TOUCHES":
            dessiner_fond(ecran)
            dessiner_ecran_touches(ecran, volume_general)
            
        elif etat == "MENU_DIFFICULTE":
            dessiner_fond(ecran)
            dessiner_texte_centre(ecran, "DIFFICULTE", 80, 50, ROUGE_SANG)
            dessiner_texte_centre(ecran, "[1] ECUYER (Facile)", 200, 30, VERT_ENDURANCE)
            dessiner_texte_centre(ecran, "[2] CHEVALIER (Normal)", 250, 30, ARGENT)
            dessiner_texte_centre(ecran, "[3] LEGENDE (Difficile)", 300, 30, ROUGE_SANG)
            dessiner_texte_centre(ecran, "ECHAP : RETOUR", 500, 25, ROUGE_SANG)

        elif etat == "JEU":
            surface_jeu = pygame.Surface((LARGEUR, HAUTEUR))
            dessiner_fond(surface_jeu)
            
            if not jeu_fini and not victoire:
                touches = pygame.key.get_pressed()
                joueur.deplacer(touches)
                
                boss_corps_a_corps, nouveau_piege = boss.mettre_a_jour(joueur)
                
                if nouveau_piege:
                    attaques_sol.append(nouveau_piege)
                    
                boss.mettre_a_jour_projectiles()
                
                if boss.etat == "resurrection":
                    secousse = 5

                for p in boss.projectiles:
                    if p.rect.colliderect(joueur.rect):
                        if joueur.invincible == 0 and joueur.z < 30:
                            joueur.pv -= 20
                            joueur.invincible = 30
                            secousse = 8
                            p.vie = 0
                            for _ in range(8):
                                particules.append(Particule(joueur.rect.centerx, joueur.rect.centery, "sang"))
                            if joueur.rect.centerx < boss.rect.centerx:
                                joueur.recul_x = -15
                            else:
                                joueur.recul_x = 15

                for g in attaques_sol:
                    hit = g.obtenir_hitbox()
                    if hit and hit.colliderect(joueur.rect):
                        if joueur.invincible == 0:
                            joueur.pv -= 30
                            joueur.invincible = 40
                            secousse = 10
                            g.a_touche = True
                            for _ in range(10):
                                particules.append(Particule(joueur.rect.centerx, joueur.rect.centery, "sang"))
                            joueur.vel_z = 10
                            joueur.en_saut = True

                if boss_corps_a_corps:
                    hitbox = pygame.Rect(boss.rect.x - 60, boss.rect.y, 200, 100)
                    if hitbox.colliderect(joueur.rect) and joueur.invincible == 0:
                        joueur.pv -= 20
                        joueur.invincible = 40
                        secousse = 10
                        for _ in range(10):
                            particules.append(Particule(joueur.rect.centerx, joueur.rect.centery, "sang"))
                        if joueur.rect.centerx < boss.rect.centerx:
                            joueur.recul_x = -15
                        else:
                            joueur.recul_x = 15

                hbox = joueur.obtenir_hitbox()
                if hbox and hbox.colliderect(boss.rect) and boss.etat != "resurrection":
                    boss.pv -= 10 * joueur.mult_degats
                    boss.chrono_flash = 5
                    boss.rect.x += 5 if joueur.regarde_droite else -5
                    effets_sang.append(EffetSang(boss.rect.centerx, boss.rect.centery))

                if joueur.pv <= 0:
                    jeu_fini = True
                
                if boss.pv <= 0:
                    if boss.phase == 1 and boss.etat != "resurrection":
                        boss.lancer_transition_phase2()
                        jouer_musique(MUSIC_PHASE2, volume_general)
                    elif boss.phase == 2:
                        victoire = True

                if random.random() < 0.1:
                    particules.append(Particule(random.randint(0, LARGEUR), 0, "cendre"))

            decale = random.randint(-secousse, secousse) if secousse > 0 else 0
            if secousse > 0:
                secousse -= 1
            
            for p in particules:
                p.mettre_a_jour()
                p.dessiner(surface_jeu)
            
            for g in attaques_sol:
                g.mettre_a_jour()
                g.dessiner(surface_jeu)
            attaques_sol = [g for g in attaques_sol if not g.fini]

            for b in effets_sang:
                b.mettre_a_jour()
                b.dessiner(surface_jeu)
            effets_sang = [b for b in effets_sang if not b.fini]

            boss.dessiner(surface_jeu)
            joueur.dessiner(surface_jeu, victoire)
            dessiner_hud(surface_jeu, joueur, boss)
            
            if jeu_fini:
                dessiner_texte_centre(surface_jeu, "VOUS ETES MORT (ENTREE)", 200, 60, ROUGE_SANG)
            if victoire:
                dessiner_texte_centre(surface_jeu, "ARCHIMAGE DU NEANT ABATTU (ENTREE)", 200, 45, OR)

            ecran.blit(surface_jeu, (decale, decale))

        pygame.display.flip()
        horloge.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()