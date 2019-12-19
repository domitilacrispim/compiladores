import csv
import sys
def lexico(pos):
 
 comp = open('compiladores.csv', 'r')
 dici = {}
 reader = csv.reader(comp)
 flag = 0
 # carrega informações da tabela de produção
 cabecalho=[]
 for linha in reader:
     for c in linha:
        dici[c] = {}
        cabecalho.append(c)
     break   	
 for linha in reader:
   for c in range(len(linha)): 
     dici[cabecalho[c]][flag]=linha[c]
   flag=flag+1 
 #print(dici["e"][0])
 arq = open("programa", "r")
 col=0
 lin=0
 estado=0
 arquivo=arq.read()
 atual=arquivo[pos]
 while(True):
   if(atual==" " or atual=="\n" or atual=="EOF"):
    atual="branco"
  # print(estado, atual)
   estado=int(dici[atual][estado])
   pos=pos+1
   if(estado==-1):
    print("Error na posicao", pos)
    sys.exit(0)
   if(int(dici["isFinal"][estado])==1):
    if(dici["value"][estado]==">" or dici["value"][estado]==">=" or dici["value"][estado]=="<" or dici["value"][estado]=="<>" or dici["value"][estado]=="==" or dici["value"][estado]=="<="):
     if(int(dici["goBack"][estado])==1):
       pos=pos-1
     return "relacional",pos
    elif(dici["value"][estado]=="+"  or dici["value"][estado]=="/" or dici["value"][estado]=="*" or dici["value"][estado]=="-"):
     if(int(dici["goBack"][estado])==1):
      pos=pos-1
     return "aritmetico",pos
    elif(dici["value"][estado]=="="):  
     if(int(dici["goBack"][estado])==1):
      pos=pos-1
     return "atribuicao",pos
    else:
      if(int(dici["goBack"][estado])==1):
       pos=pos-1
      return dici["value"][estado], pos
    if(int(dici["goBack"][estado])==1):
     pos=pos-1
    estado=0
   if(pos==len(arquivo)):
    break  
   atual=arquivo[pos]
 atual="branco"
 estado=int(dici[atual][estado])
 pos=pos+1
 if(estado==-1):
    print("Error na posicao", pos)
 if(int(dici["isFinal"][estado])==1):
    print(dici["value"][estado])
 return "$",-1
 

class No:
    def __init__(self, valor):
        self.valor = valor
        self.filhos = []
        self.processado = False

    def processador(self, valor):
        if(not(self.processado) and self.valor == valor):
            self.processado = True
        else:
            for filho in self.filhos:
                filho.processador(valor)

    def addFilho(self, valor, pai):
        if(pai == self.valor and not(self.processado)):
            self.filhos.append(No(valor))
            return 1
        if(len(self.filhos) == 0):
            return 0
        for filho in self.filhos:
            if(filho.addFilho(valor, pai) == 1):
                return 1

    def percorre(self):
        flagui = 0
        if(len(self.filhos) != 0):
            print("")
        for filho in self.filhos:
            if(flagui == 0):
                print("<", end="")
                flagui = 1
            print(filho.valor, " ", end="")
        if(flagui == 1):
            print(">", end="")
        for filho in self.filhos:
            filho.percorre()


prod = open('producoes.csv', 'r')
n_term = open('n_terminais.csv', 'r')
anali = open('analise.csv', 'r')
producao = []
dici = {}
reader = csv.reader(prod)

# carrega informações da tabela de produção
for linha in reader:
    for c in linha:
        if(not(c in dici) and c != ""):
            dici[c] = {}
    producao.append(linha)

flag = 0
cabecalho = []
reader = csv.reader(anali)

for i in reader:
    if(flag == 0):
        # carrega tokens (terminais)
        for c in i:
            cabecalho.append(c)
        flag = 1
    else:
        aux = 0
        # carrega tabela de analise preditiva
        for c in i:
            dici[i[0]][cabecalho[aux]] = c
            aux = aux+1
print(dici["inicio"])     
# carrega nao terminais
nao_t = []
reader = csv.reader(n_term)
for i in reader:
    nao_t.append(i[0])

# lexema = input().split()  # ler codigo

pilha = ["S"]
raiz = No("S")
flag = 0
flag_proc = 0
prox, pos = lexico(0)
print(prox)
# print(prox)
while(len(pilha) > 0):
    flag_proc = 0
    x = pilha[len(pilha)-1]
    print(pilha)
    # print(prox)
    if(x not in nao_t):
        if(x == prox):
            pilha.pop(len(pilha)-1)
            # flag = flag+1
            prox, pos = lexico(pos)  # chamar lexico
          #  print(prox)
            if(prox=="$"):
           #  print(prox)
             break
        else:
            print(prox, x)
            print("ERRO1")
            break
    else:
        if(dici[x][prox] == ""):
            print(x, prox)
            print("ERRO2")
            break
        else:
            pai = pilha[len(pilha)-1]
            pilha.pop(len(pilha)-1)
            flag_proc = 1
            for c in reversed(producao[int(dici[x][prox])-1]):
                if(c != ""):
                    raiz.addFilho(c, pai)
                    pilha.append(c)
            if(flag_proc == 1):
                raiz.processador(pai)

if (prox != "$"):
    print("ERRO")	
else:
    print("\nCadeia Aceita!!")
    print('\nArvore:')
    print(raiz.valor, end="")
    raiz.percorre()


