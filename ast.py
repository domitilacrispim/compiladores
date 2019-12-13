import csv
prod = open('producoes.csv', 'r')
n_term = open('n_terminais.csv', 'r')
anali = open('analises.csv', 'r')
producao=[]
dici={}
reader = csv.reader(prod)
for linha in reader:
 for c in linha:
  if(not(c in dici) and c!=""):
   dici[c]={}
 producao.append(linha)
flag=0
cabecalho=[]
reader = csv.reader(anali)	
for i in reader:
 if(flag==0):
  for c in i:
   cabecalho.append(c)
  flag=1
 else:
  aux=0
  for c in i:
   dici[i[0]][cabecalho[aux]]=c
   aux=aux+1
nao_t=[]
reader = csv.reader(n_term)
for i in reader:
 nao_t.append(i[0])
lexema=input().split()
pilha=["S"]
flag=0
prox=lexema[flag]
while(len(pilha)>0):
 x=pilha[len(pilha)-1]
 print(pilha) 
 if( x not in nao_t):
  if( x == prox ):
   pilha.pop(len(pilha)-1)
   flag=flag+1
   prox=lexema[flag]
  else:
   print("ERRO1")
   break
 else:
  if(dici[x][prox]==""):
   print("ERRO2")
   break 
  else:
   pilha.pop(len(pilha)-1) 
   for c in reversed(producao[int(dici[x][prox])-1]):
    if(c!=""):
     pilha.append(c)
   # print(producao[int(dici[x][prox])-1])
   #to do senão // Tab[X, proxToken] = X → Y1 Y2 ... Yn
if (prox!="$") :
 print ("ERRO")
else:
 print("aceita")
 
  
