import tkinter as tk

# Configurações da Janela
LARGURA = 800
ALTURA = 500
VELOCIDADE_RAQUETE = 20
LARGURA_RAQUETE = 15
ALTURA_RAQUETE = 90
TAMANHO_BOLA = 15

class JogoPingPong:
    def __init__(self, root):
        self.root = root
        self.root.title("Ping Pong em Python")
        self.root.resizable(False, False)

        # Canvas (Tela de jogo)
        self.canvas = tk.Canvas(root, width=LARGURA, height=ALTURA, bg="black")
        self.canvas.pack()

        # Placar
        self.pontos_j1 = 0
        self.pontos_j2 = 0
        self.texto_placar = self.canvas.create_text(
            LARGURA // 2, 30, text="0   |   0", fill="white", font=("Arial", 30, "bold")
        )

        # Linha central
        self.canvas.create_line(LARGURA // 2, 0, LARGURA // 2, ALTURA, fill="white", dash=(5, 5))

        # Raquetes
        self.raq_j1 = self.canvas.create_rectangle(
            20, ALTURA//2 - ALTURA_RAQUETE//2, 
            20 + LARGURA_RAQUETE, ALTURA//2 + ALTURA_RAQUETE//2, 
            fill="white"
        )
        self.raq_j2 = self.canvas.create_rectangle(
            LARGURA - 20 - LARGURA_RAQUETE, ALTURA//2 - ALTURA_RAQUETE//2, 
            LARGURA - 20, ALTURA//2 + ALTURA_RAQUETE//2, 
            fill="white"
        )

        # Bola
        self.bola = self.canvas.create_oval(
            LARGURA//2 - TAMANHO_BOLA//2, ALTURA//2 - TAMANHO_BOLA//2,
            LARGURA//2 + TAMANHO_BOLA//2, ALTURA//2 + TAMANHO_BOLA//2,
            fill="white"
        )

        # Velocidades iniciais da bola
        self.vel_bola_x = 5
        self.vel_bola_y = 5

        # Mapeamento de teclas pressionadas
        self.teclas = {}
        self.root.bind("<KeyPress>", self.tecla_pressionada)
        self.root.bind("<KeyRelease>", self.tecla_solta)

        # Iniciar o loop do jogo
        self.atualizar_jogo()

    def tecla_pressionada(self, event):
        self.teclas[event.keysym.lower()] = True

    def tecla_solta(self, event):
        self.teclas[event.keysym.lower()] = False

    def mover_raquetes(self):
        # Raquete Jogador 1 (W / S)
        pos_j1 = self.canvas.coords(self.raq_j1)
        if self.teclas.get("w") and pos_j1[1] > 0:
            self.canvas.move(self.raq_j1, 0, -VELOCIDADE_RAQUETE)
        if self.teclas.get("s") and pos_j1[3] < ALTURA:
            self.canvas.move(self.raq_j1, 0, VELOCIDADE_RAQUETE)

        # Raquete Jogador 2 (Setas Cima / Baixo)
        pos_j2 = self.canvas.coords(self.raq_j2)
        if self.teclas.get("up") and pos_j2[1] > 0:
            self.canvas.move(self.raq_j2, 0, -VELOCIDADE_RAQUETE)
        if self.teclas.get("down") and pos_j2[3] < ALTURA:
            self.canvas.move(self.raq_j2, 0, VELOCIDADE_RAQUETE)

    def mover_bola(self):
        self.canvas.move(self.bola, self.vel_bola_x, self.vel_bola_y)
        pos_bola = self.canvas.coords(self.bola)

        # Colisão com o topo ou fundo
        if pos_bola[1] <= 0 or pos_bola[3] >= ALTURA:
            self.vel_bola_y *= -1

        # Colisão com as raquetes
        pos_j1 = self.canvas.coords(self.raq_j1)
        pos_j2 = self.canvas.coords(self.raq_j2)

        # Rebater na Raquete 1
        if pos_bola[0] <= pos_j1[2] and pos_j1[1] <= pos_bola[3] and pos_j1[3] >= pos_bola[1]:
            self.vel_bola_x = abs(self.vel_bola_x)  # Vai para a direita

        # Rebater na Raquete 2
        if pos_bola[2] >= pos_j2[0] and pos_j2[1] <= pos_bola[3] and pos_j2[3] >= pos_bola[1]:
            self.vel_bola_x = -abs(self.vel_bola_x) # Vai para a esquerda

        # Pontuação (quando passa das bordas laterais)
        if pos_bola[0] <= 0:
            self.pontos_j2 += 1
            self.resetar_bola()
        elif pos_bola[2] >= LARGURA:
            self.pontos_j1 += 1
            self.resetar_bola()

    def resetar_bola(self):
        # Atualiza placar
        self.canvas.itemconfig(self.texto_placar, text=f"{self.pontos_j1}   |   {self.pontos_j2}")
        
        # Reposiciona a bola no centro
        self.canvas.coords(
            self.bola,
            LARGURA//2 - TAMANHO_BOLA//2, ALTURA//2 - TAMANHO_BOLA//2,
            LARGURA//2 + TAMANHO_BOLA//2, ALTURA//2 + TAMANHO_BOLA//2
        )
        # Inverte a direção do saque
        self.vel_bola_x *= -1

    def atualizar_jogo(self):
        self.mover_raquetes()
        self.mover_bola()
        # Atualiza o jogo a cada 16ms (~60 FPS)
        self.root.after(16, self.atualizar_jogo)

# Executar o jogo
if __name__ == "__main__":
    root = tk.Tk()
    jogo = JogoPingPong(root)
    root.mainloop()