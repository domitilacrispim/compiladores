import csv
ficheiro = open('compiladores.csv', 'r')
reader = csv.reader(ficheiro)
tabela=[]
for linha in reader:
    tabela.append(linha)
programa=input()
estado=0
for c in programa:
 print(c)
 for i in range(len(tabela[0])):
  if (c==tabela[0][i]):
   aux=i
   break
  if ( i>24):
   if(c>'0' and c<='9'):
    aux=24
    break
   if(c>='A' and c<='Z'):
    aux=25
    break
   if(c>='a' and c<='z'):
    aux=25
    break
   if(c=='_'):
    aux=25
    break
   else:
    aux=26
 if(aux==26):
  print(tabela[estado][26])
  estado=0
  continue
 for j in range(1,len(tabela)):
  if(tabela[j][0]==str(estado)):
   aux2=j
   break
 if(tabela[j][aux]=="erro"):
  print ("erro")
  break
 else:
  estado=int(tabela[j][aux])
