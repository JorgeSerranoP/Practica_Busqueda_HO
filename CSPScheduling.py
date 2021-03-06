from constraint import *

problem = Problem()

# Creamos los satelites disponibles, dividiendo los que tienen más de una franja horaria
satelites = ['SAT1_F1', 'SAT2_F1', 'SAT3_F1',
             'SAT3_F2', 'SAT4_F1', 'SAT5_F1', 'SAT6_F1', 'SAT6_F2']

# Creamos las antenas disponibles
antenas = ['ANT1', 'ANT2', 'ANT3', 'ANT4', 'ANT5', 'ANT6',
           'ANT7', 'ANT8', 'ANT9', 'ANT10', 'ANT11', 'ANT12']

# Satelites cuya franja es antes de las 12
satelitesAntes12 = [satelites[0], satelites[1],
                    satelites[2], satelites[5], satelites[6]]

# Satelites cuya franja es despues de las 12
satelitesDespues12 = [satelites[3], satelites[4], satelites[7]]

# Añadimos a cada satelite las antenas visibles según la tabla
problem.addVariable(satelites[0], antenas[:4])
problem.addVariable(satelites[1], antenas[:3])
problem.addVariable(satelites[2], (antenas[3], antenas[5]))
problem.addVariable(satelites[3], (antenas[6], antenas[8], antenas[9]))
problem.addVariable(satelites[4], (antenas[7], antenas[10], antenas[11]))
problem.addVariable(satelites[5], (antenas[0], antenas[6], antenas[11]))
problem.addVariable(satelites[6], (antenas[6], antenas[8]))
problem.addVariable(satelites[7], antenas[2:5])

# R2: SAT1 y SAT2 misma antena
problem.addConstraint(AllEqualConstraint(), (satelites[:2]))

# R3: SAT2, SAT4 y SAT5 antenas diferentes
problem.addConstraint(AllDifferentConstraint(),
                      (satelites[1], satelites[4], satelites[5]))


def Restriccion4(a, b):
    if a == 'ANT12' and b == 'ANT11':
        return False
    return True


# R4: Si SAT5 se comunica con ANT12, SAT4 no se puede comunicar con ANT11
problem.addConstraint(Restriccion4, (satelites[5], satelites[4]))


def Restriccion5(a, b):
    if(a == 'ANT7' and b == 'ANT12') or (a == 'ANT12' and b == 'ANT7'):
        return False
    return True


# R5: Si en una solución se asignan las antenas ANT7 y ANT12,
# se deben asignar ambas a franjas horarias que comiencen antes de las
# 12:00 o a franjas horarias que comiencen después de las 12:00
for i in range(len(satelitesAntes12)):
    for j in range(len(satelitesDespues12)):
        problem.addConstraint(
            Restriccion5, (satelitesAntes12[i], satelitesDespues12[j]))


# Obtenemos todas las soluciones posibles
solutions = problem.getSolutions()
print(len(solutions))
