import sys	
import csv
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
pos=0
arquivo=arq.read()
atual=arquivo[pos]
while(True):
  if(atual==" " or atual=="\n" or atual=="EOF"):
   atual="branco"
#  print(estado, atual)
  estado=int(dici[atual][estado])
  pos=pos+1
  if(estado==-1):
   print("Error na posicao", pos)
   sys.exit(0)
  if(int(dici["isFinal"][estado])==1):
   print(dici["value"][estado])
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
   
