# Garzon Dominguez Gerardo Ismael, Compiladores 3CV18

import sys
import dfagen

# checa si se tiene un segundo argumento despues del nombre del programa
# se espera que este sea una ruta hacia una definicion de automata .txt
def set_program(args):
	if len(args) > 1:
		return args[1]
	else:
		sys.exit('uso: python3 <main.py> <ruta automata .txt>')

# hace uso del constructor de la clase dfagen
def main():
	gen = dfagen.dfagen(set_program(sys.argv))

if __name__ == '__main__':
	main()
