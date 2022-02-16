from pyswip import Prolog

prolog = Prolog()
prolog.consult('bdknowledge.pl')

reglas = []
antec = []
consec = []

#Para que sea una regla valida la cadena debe cumplir lo siguiente:
#1: Debe contener la subcadena "entonces" y cadena o caracter antes y despues de este
#2: No puede contener el conector "o" despues del entonces (Se considera una regla no determinista)
def isregla(cadena):
    begin = cadena.lower().find('entonces')
    end = cadena.lower().find('entonces') + len('entonces') - 1
    
    if 'entonces' in cadena.lower() and begin > 1 and end < len(cadena) - 2:
        if ' o ' in cadena.split(' entonces ')[1]:
            return -2
        return 1
    return -1

def clean_rule(x):
    cadena = x.lower()
    elem = ['.', ',', ';', ':', '-', 'si ']
    antecedentes = []
    consecuentes = []
    
    #Limpiando caracteres no deseables de la cadena
    for c in  elem:
        cadena = cadena.replace(c, '')
        
    #Dividir la cadena en 2. Separar el antecedente y el consecuente 
    list_aux = cadena.split(' entonces ')
    
    #Analizando y dividiendo la cadena de tal manera que sea una clausula de Horn
    #Separar el antecendente por el conector "o". Ejem: Si A \/ B --> C 
    if list_aux[0].count(' o ') > 0:
        antecedentes = list_aux[0].split(' o ')
    
    #Separar el consecuentes por el conector "y". Ejem: Si A --> B /\ C   
    if list_aux[1].count(' y ') > 0:
        consecuentes = list_aux[1].split(' y ')

    #Si los dos ultimos if no se ejecutaron entonces la regla ya es una clausula de Horn. Ejem: Si A /\ B --> C
    #Separa el antecedente por el conector "y" (si hay).
    if len(antecedentes) == 0:
        antecedentes = list_aux[0].split(' y ')
        
    if len(consecuentes) == 0:
        consecuentes.append(list_aux[1])

    #Creo un lista de reglas (una lista de listas): [[regla1], [regla2], ..., [reglaN]]
    #Una regla: ['consecuente', 'antecedente1', 'antecedente2', ..., 'antecedenteN'].
    #El consecuente va en la poscion 0 y en las demas posiciones van los antecedentes
    for value_i in consecuentes:
        reglas.append([value_i])
        for value_j in antecedentes:
            reglas[len(reglas) - 1] += value_j.split(' y ')
            
#Este metodo escribe en un archivo prolog los hechos y las reglas previamente procesadas   
def save_knowloge(facts):
    with open('bdknowledge.pl', mode='r+') as f:
        f.readlines()
        f.write('\n')
        
        #Escribo los hechos en el archivo "bdknowledge.pl".
        #Ejem: "soy profesor" se escribira "soy_profesor."
        for i in facts:
            f.write(antec[int(i) - 1].replace(' ', '_')+'.'+'\n')
        
        #Escribo las reglas
        #Ejem: Si soy profesor entonces imparto clases. [['imparto clases', 'soy profesor']]
        #Se escribira "imparto_clases :- soy_profesor." Si hay mas antecedentes van separadas por coma (Clausula de Horn)
        f.write('\n')
        for regla in reglas:
            for index, value in enumerate(regla):
                if index == 0:
                    #Escribo el consecuente
                    f.write(value.replace(' ', '_')+' :- ')
                    continue
                
                elif index == len(regla) - 1:
                    #Escribo el ultimo antecedente
                    f.write(value.replace(' ', '_')+'.'+'\n')
                
                else:
                    #Escribo los antecedentes intermedio.
                    #Como estamos usando clausula de Horn van separadas por coma ","
                    f.write(value.replace(' ', '_')+', ')
                    
                           
print('Ejemplo de reglas: Si A entonces B / Si A y B entonces C / ...\nSiendo A, B y C cualquier palabra\n')
print('Escriba las reglas/preposiciones:')

# COMENZA AQUI -----------------------------------------------------------------------------------------------

#Pedir que el usuario entre las reglas que necesite
count = 1
while True:
    print('(Enter): Para insertar mas reglas')
    print('(1): Continuar con los hechos')
    
    cadena = input(f'Regla({count}): ')
    print('---'*12)
    if cadena == '':
        continue
    if cadena == '1':
        break

    if isregla(cadena) == 1:
        clean_rule(cadena)
        count += 1
    elif isregla(cadena) == -1:
        print(f'"{cadena}" NO ES UNA REGLA.\n')
    else:
        print('ESTA REGLA NO ES DETERMINISTA.'+'\n')

#Despues de tener todas las reglas, separar los antecedentes y los consecuentes de la lista de reglas
#Nos servira para preguntar al usuario los hechos y lo que necesita saber    
for regla in reglas:
    for index, value in enumerate(regla):
        if index == 0 and value not in consec:
            consec.append(value)
            continue
        if index > 0 and value not in antec:
            antec.append(value)

print('Selecciona los hechos separados por coma y sin espacios:')
print('---'*12)
#Obtengo los hechos de los antecedentes
for index, value in enumerate(antec):
    print(f'Hecho({index + 1}): {value}')
    
#Pedimos que el usuario selecione los hechos 
print()
while True:
    selected = input('Hechos: ')
    
    notnum = ''
    for h in selected.split(','):
        if h.isnumeric() == False:
            notnum = h
            
    if notnum != '':
        print(f'Revisa tu seleccion: "{notnum}" no es una opcion valida\n')
        continue
      
    if len(selected.split(',')) <= len(antec):
        for h in selected.split(','):
            if int(h) > 0 and int(h) <= len(antec) and selected.count(h) == 1:
                #Guardar los hechos y reglas en el archivo prolog
                save_knowloge(selected.split(','))
                break
            else:
                print('Revisa tu seleccion: hechos repetidos o no existente\n')
                continue
    else:
        print('Has selecionado mas hechos de los que tienes disponible\n')
        continue
    
    break

print('\n'+'---'*12)
print('Que desea saber ?')
print('---'*12)
for index, value in enumerate(consec):
    print(f'Pregunta({index + 1}): {value} ?')

while True:
    questions = input('\nOpcion: ')
    
    notnum = ''
    for q in questions.split(','):
        if q.isnumeric() == False:
            notnum = q
            break
            
    if notnum != '':
        print(f'Revisa tu seleccion: "{notnum}" no es una opcion valida\n')
        continue
    
    if len(questions.split(',')) <= len(consec):
        for q in questions.split(','):
            if int(q) > 0 and int(q) <= len(consec) and questions.count(q) == 1:
                
                result = bool(list(prolog.query(consec[int(questions) - 1].replace(' ', '_'))))
                ans = 'Sí' if result else 'No'
                print(f'\n{consec[int(questions) - 1]} ?\n{ans}')
                break
            else:
                print('Revisa tu seleccion: Preguntas repetidas, no existente, o no numerico\n')
            continue 
    else:
        print('Has selecionado mas Preguntas de los que tienes disponible\n')
        continue
    
    break
           
