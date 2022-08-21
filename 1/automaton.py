# Garzon Dominguez Gerardo Ismael, Compiladores 3CV18

epsilon = 'E'

class Automata:
	#5-tupla de automata
	__states__ : set
	__alphabet__ : set
	__delta_map__ : dict
	__initial_state__ : str
	__accepting_states__ : set

	# Detalles de implementacion. errset contiene los simbolos de la
	# cadena que no estan en el alfabeto del automata, pathstack va guardando
	# el camino que actualmente el automata recorre
	# memo_accepted guarda soluciones para no realizar doble procesamiento
	# aun falta algun metodo para limpiar memo_accepted
	# index guarda el ultimo indice valido de la cadena
	__memo_accepted__ : dict
	__errset__ : set
	__pathstack__ : list
	__last_valid_state__ : str
	__index__ : int

	def help(self):
		print(
	"""
	Automatas.
	Ayuda a comprobar si una cadena pertenece al lenguaje descrito por el automata
	"""
		)

	#Para quitar las nuevas lineas al construir un automata desde archivo
	def __strip_nlines__(self, list_of_lines):
		newlist = []
		for i in list_of_lines:
			newlist.append(i.strip('\n'))
		return newlist

	#resetea el ultimo camino y el stack de errores.
	#Esto sucede cada que el automata recibe una nueva cadena a validar
	def __reset_stacks__(self):
		self.__errset__ = None
		self.__pathstack__ = None

	#inicializa automata con los 5 elementos de la 5-tupla que describen al automata.
	def __init_with_5_tuple__(self, states : set, alphabet : set, Delta, initial_state,
	accepting_states):
		self.__states__ = states
		self.__alphabet__ = alphabet
		self.__delta_map__ = Delta
		self.__initial_state__ = initial_state
		self.__accepting_states__ = accepting_states
		self.__memo_accepted__ = {}
		self.__reset_stacks__()

	#inicializa el automata con informacion de un archivo .txt.
	#se hacen algunas comprobaciones sobre la definicion del archivo
	# si se encuentran errores en el archivo, no se garantiza que al automata funcione
	# los errores se imprimiran en pantalla si es que se detectan
	def init_from_file(self, filepath, delim):
		try:
			fp = open(filepath, 'r')
		except:
			print('No se puede abrir el archivo {}'.format(filepath))
			return
		
		with fp as rd:
			lines = fp.readlines()
		lines = self.__strip_nlines__(lines)

		states = set(lines[0].split(delim))
		alphabet = set(lines[1].split(delim))
		initial_state = lines[2].split(delim)[0]

		if initial_state not in states:
			print('Error estado inicial {} no se definio en los estados'.format(initial_state))
			return
			
		accepting_states = set(lines[3].split(delim))

		delta_map = {}
		for i in lines[4:]:
			sepln = i.split(delim)
			key = ()
			if sepln[0] in states:
				key = (sepln[0])
			else:
				print('Error, "{}" no se definio en los estados'.format(sepln[0]))
				continue
			if sepln[1] in alphabet or sepln[1] == epsilon:
				key = (sepln[0], sepln[1])
			else:
				print('Error, "{}" no se definio en el alfabeto'.format(sepln[1]))
				continue

			if key in delta_map:
				val = delta_map[key]
			else:
				val = []

			if sepln[2] not in val and sepln[2] in states:
				val.append(sepln[2])
			else:
				print('Error, "{}" no se definio en los estados'.format(sepln[2]))
				continue
			delta_map[key] = val

		self.__init__(states, alphabet, delta_map, initial_state, accepting_states)

	#busca que metodo usar para inicializar el objeto automata
	def __init__(self, *args):
		if(len(args) == 5):
			return self.__init_with_5_tuple__(*args)
		elif(len(args) == 2):
			return self.init_from_file(*args)

	#informa si una cadena pertenece o no al lenguaje descrito por el automata
	def __inform_status__(self, sequence):
		if sequence in self.__memo_accepted__:
			print('Cadena "{}" es valida'.format(sequence))
			print('Info:', *self.__memo_accepted__[sequence])
		else:
			print('Cadena "{}" es invalida para el automata'.format(sequence))

	#funcion de utilidad para agregar soluciones asociadas a una cadena usando un dict
	def __add_solution__(self, sequence):
		if sequence in self.__memo_accepted__:
			a = self.__memo_accepted__[sequence]
		else:
			a = self.__memo_accepted__[sequence] = []
		a.append(self.__pathstack__.copy())


	# agregara elementos al pathstack del automata (camino de validacion)
	# agregara los simbolos invalidos al errset del automata
	def __ctrl_path__(self, sequence, pos, i, empty_flag):
		if i != None:
			self.__pathstack__.append(i)

		if pos < len(sequence) and sequence[pos] in self.__alphabet__:
			self.__last_valid_state__ = i
			self.__index__ = pos
		elif pos == len(sequence) and sequence[self.__index__] in self.__alphabet__:
			self.__last_valid_state__ = i
		elif pos < len(sequence) and sequence[pos] not in self.__alphabet__:
			self.__errset__.add(sequence[pos])

		if pos == len(sequence) and empty_flag == True:
			if self.__last_valid_state__ in self.__accepting_states__:
				self.__add_solution__(sequence)
		elif pos == len(sequence)-1 and empty_flag == False:
			if self.__last_valid_state__ in self.__accepting_states__:
				self.__add_solution__(sequence)			

	# funcion de transiciones como 'funcion' en vez de solo ser un dict
	# aun asi hace uso del dict delta_map del automata
	def __Delta__(self, key):
		if key not in self.__delta_map__:
			return [None]
		else:
			return self.__delta_map__[key]

	# atraviesa caminos recursivamente, se cubren 3 casos distintos
	# tambien genera caminos con transiciones vacias
	def __traverse_path__(self, curr_state, sequence, pos):
		if pos < len(sequence) and sequence[pos] in self.__alphabet__:

			key = (curr_state, epsilon)
			m = self.__Delta__(key)
			if m != [None]:
				for i in m:
					self.__ctrl_path__(sequence, pos, i, True)
					self.__traverse_path__(i, sequence, pos)
					self.__pathstack__.pop()

			key = (curr_state, sequence[pos])
			if key in self.__delta_map__:
				for i in self.__Delta__(key):						
					self.__ctrl_path__(sequence, pos, i, False)
					self.__traverse_path__(i, sequence, pos+1)
					self.__pathstack__.pop()

		elif pos < len(sequence) and sequence[pos] not in self.__alphabet__:
			self.__ctrl_path__(sequence, pos, None, False)
			self.__traverse_path__(curr_state, sequence, pos+1)
		else:
			key = (curr_state, epsilon)
			if key in self.__delta_map__:
				for i in self.__Delta__(key):
					self.__ctrl_path__(sequence, pos, i, True)
					self.__traverse_path__(i, sequence, len(sequence))
					self.__pathstack__.pop()


	# completa la informacion para imprimir a la pantalla sobre el estatus
	# de la cadena que se le dio al automata para procesar
	def __additional_info__(self, sequence):
		if sequence in self.__memo_accepted__:
			if self.__errset__:
				errstatus = 'Simbolos no permitidos: {}'.format(self.__errset__)
			else:
				errstatus = 'Sin errores encontrados'
			a = self.__memo_accepted__[sequence]
			info = (a, errstatus)
			self.__memo_accepted__[sequence] = info

	# inicializa algunas variables "privadas" al objeto necesarias para procesar las cadenas
	def __initialize_processing__(self):
		self.__pathstack__ = []
		self.__errset__ = set([])
		self.__last_valid_state__ = self.__initial_state__
		self.__pathstack__.append(self.__initial_state__)
		self.__index__ = 0

	#muestra la validacion o no de una cadena que se le da al automata.
	def show_all_paths(self, sequence):
		if sequence not in self.__memo_accepted__:
			self.__initialize_processing__()

			self.__traverse_path__(self.__initial_state__, sequence, 0)
			self.__additional_info__(sequence)	

			self.__reset_stacks__()

		self.__inform_status__(sequence)
