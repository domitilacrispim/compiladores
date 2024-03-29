import csv
import sys
global tabela_simbol
global nao_t
tabela_simbol=[]
global max_n
global col, lin
col=0
lin=0
max_n=0
def lexico(pos):
 global lin, col, tabela_simbol
 comp = open('compiladores.csv', 'r')
 dici = {}
 reader = csv.reader(comp)
 flag = 0
 f_inicio = 0
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
 estado=0
 arquivo=arq.read()
 inicial=0
 atual=arquivo[pos]
 while(True):
   if(atual=="\n"):
    lin=lin+1
    col=0
   if(atual==" " or atual=="\n" or atual=="EOF"):
    atual="branco"
   elif(f_inicio==0):
    f_inicio=1
    inicial=pos
  # print(estado, atual)
   if(atual==","):
    atual="vir"
   try:
    estado=int(dici[atual][estado])
   except:
    print("O simbolo nao faz parte da gramatica linha:", lin, "coluna:", col )
    return "$", -1, -1
   pos=pos+1
   col=col+1
   if(estado==-1):
    print("Error na posicao", pos)
    sys.exit(0)
   if(int(dici["isFinal"][estado])==1):
    if(dici["value"][estado]==">" or dici["value"][estado]==">=" or dici["value"][estado]=="<" or dici["value"][estado]=="<>" or dici["value"][estado]=="==" or dici["value"][estado]=="<="):
     if(int(dici["goBack"][estado])==1):
       pos=pos-1
       col=col-1
     return "relacional",pos, dici["value"][estado]
    elif(dici["value"][estado]=="+"  or dici["value"][estado]=="/" or dici["value"][estado]=="*" or dici["value"][estado]=="-"):
     if(int(dici["goBack"][estado])==1):
      pos=pos-1
      col=col-1
     return "aritmetico",pos, dici["value"][estado]
    elif(dici["value"][estado]=="="):  
     if(int(dici["goBack"][estado])==1):
      pos=pos-1
      col=col-1
     return "atribuicao",pos, dici["value"][estado]
    elif(dici["value"][estado]=="vir"):  
     if(int(dici["goBack"][estado])==1):
      pos=pos-1
      col=col-1
     return "vir",pos, dici["value"][estado]
    elif(dici["value"][estado]=="id"):  
     if(int(dici["goBack"][estado])==1):
      pos=pos-1
      col=col-1
     if(arquivo[inicial:pos] not in tabela_simbol):
      tabela_simbol.append(arquivo[inicial:pos])
     return "id",pos, tabela_simbol.index(arquivo[inicial:pos])
    else:
      if(int(dici["goBack"][estado])==1):
       pos=pos-1
       col=col-1
      return dici["value"][estado], pos ,dici["value"][estado]
   if(pos==len(arquivo)):
    break  
   atual=arquivo[pos]
 atual="branco"
 estado=int(dici[atual][estado])
 pos=pos+1
 col=col-1
 if(estado==-1):
    print("Error na posicao", pos)
 if(int(dici["isFinal"][estado])==1):
    print(dici["value"][estado])
 return "$",-1, -1
 

class No:
    def __init__(self, valor, n):
        self.valor = valor
        self.filhos = []
        self.processado = False
        self.nivel=n

    def processador(self, valor):
        if(not(self.processado) and self.valor == valor):
            self.processado = True
        else:
            for filho in self.filhos:
                filho.processador(valor)

    def addFilho(self, valor, pai):
        global max_n
        if(pai == self.valor and not(self.processado)):
            self.filhos.append(No(valor, self.nivel+1))
            if(self.nivel+1>max_n):
             max_n=self.nivel+1
            return 1
        if(len(self.filhos) == 0):
            return 0
        for filho in self.filhos:
            if(filho.addFilho(valor, pai) == 1):
                return 1

    def percorre(self, n):
        global nao_t
        flagui = 0
        if(self.nivel>n):
         return 0
        if(self.nivel==n and self.valor in nao_t):
         print("<", end="")
         for filho in reversed(self.filhos):
             print(filho.valor, " " , end="")
         print("> ", end="")
        if(self.nivel<n):
         for filho in reversed(self.filhos):
             filho.percorre(n)

         

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
# carrega nao terminais
nao_t = []
reader = csv.reader(n_term)
for i in reader:
    nao_t.append(i[0])

# lexema = input().split()  # ler codigo

pilha = ["S"]
raiz = No("S",0)
flag = 0
flag_proc = 0
prox, pos, valorz = lexico(0)
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
            prox, pos, valorz = lexico(pos)  # chamar lexico
          #  print(prox)
            if(prox=="$"):
           #  print(prox)
             break
        else:
           # print(prox, x)
            print(x, " esperado, token recebido ", prox, "linha:", lin, "coluna:", col)
            break
    else:
        print(x, prox)
        if(dici[x][prox] == ""):
            print(prox, " nao esperado", "linha:", lin, "coluna:", col)
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

if (prox != "$" or len(pilha)!=0):
    print("ERRO")	
else:
    print("\nCadeia Aceita!!")
    print('\nArvore:')
    print("<",raiz.valor,">")
    for i in range(max_n):
     raiz.percorre(i)
     print("")
    print(tabela_simbol)

