# Garzon Dominguez Gerardo Ismael, Compiladores 3CV18

import sys
import automaton

# para comprobar que los argumentos recibidos desde la cli sean correctos
def set_program(args):
	if len(args) > 1:
		return args[1]
	else:
		sys.exit('uso: python3 <main.py> <ruta automata .txt>')

# ejecuta el programa creando el objeto automata si se dan los argumentos necesarios
# si los argumentos estan mal, el programa termina
def main():

	i = set_program(sys.argv)
	aut = automaton.Automata(i, ',')
	print('"exit" para salir del programa, o introduzca cadenas')

	aut.help()
	while 1:
		input_str = input('>> ')
		if(input_str == 'exit'):
			break
		else:
			aut.show_all_paths(input_str)

if __name__ == "__main__":
	main()

