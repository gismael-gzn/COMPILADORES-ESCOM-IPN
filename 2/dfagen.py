# Garzon Dominguez Gerardo Ismael, Compiladores 3CV18

import os
import sys
import automaton

class dfagen:
	NFA : automaton.Automata
	__initial_state__ : frozenset
	__finite_map__ : dict
	__sets_as_state__:dict
	__stateno__:int

	# agrega un conjunto de estados a un diccionario que los mapea a numeros
	# un conjunto mapeado a un numero es un estado del nuevo AFD
	def __add_set__(self, state: frozenset):
		if state not in self.__sets_as_state__:
			self.__sets_as_state__[state] = self.__stateno__
			self.__stateno__ += 1

	# genera la cadena que describe el automata con el formato dado
	def __format__(self):
		comma = ','
		s = ''

		for i in self.__sets_as_state__:
			s += str(self.__sets_as_state__[i]) + comma
		s = s[0:s.__len__()-1]
		s += os.linesep

		for a in self.NFA._alphabet_:
			s += a + comma
		s = s[0:s.__len__()-1]
		s += os.linesep

		s += str(self.__sets_as_state__[self.__initial_state__])
		s += os.linesep

		for fs in self.NFA._accepting_states_:
			for i in self.__sets_as_state__:
				if fs in i:
					s += str(self.__sets_as_state__[i]) + comma
					# print(i, self.__sets_as_state__[i])
		s = s[0:s.__len__()-1]
		s += os.linesep

		for i in self.__finite_map__:
			for j in i:
				s += str(j) + comma
			s += str(self.__finite_map__[i]) + os.linesep
		return s


	# inicializador del objeto, por ahora se crea el AFD y se imprime con formato
	def __init__(self, filepath:str):
		self.NFA = automaton.Automata(filepath, ',')
		self.__finite_map__ = {}
		self.__sets_as_state__ = {}
		self.__stateno__ = 0
		self.__initial_state__ = frozenset(
			self.__ECLOSE__({self.NFA._initial_state_})
		)

		self.DFA_from_DFN(self.__initial_state__)

		print(self.__format__())

	# algoritmo recursivo para obtener los pares (estado, simbolo) del AFD
	# esta informacion ayuda a __format__ a generar la cadena de salida
	def DFA_from_DFN(self, states:set):
		for a in self.NFA._alphabet_:
			r = self.__ECLOSE__( self.__MOVE__(states, a) )
			fr = frozenset(r)
			fs = frozenset(states)

			self.__add_set__(fs)
			self.__add_set__(fr)

			# print(states, self.__sets_as_state__[fs], r, self.__sets_as_state__[fr], a)
			k = (self.__sets_as_state__[fs], a)
			if k not in self.__finite_map__:
				self.__finite_map__[k] = self.__sets_as_state__[fr]
				self.DFA_from_DFN(r)

			# if r not in self.__new_states__:
			# 	self.__new_states__.append(r)
			# 	print(states, self.__sets_as_state__[fs], r, self.__sets_as_state__[fr], a)
			# 	self.DFA_from_DFN(r)

	# computa la cerradura e de un estado state de manera recursiva
	# hace uso de la funcion delta del AFN.
	# los resultados van en Eset
	def __ECLOSE_R__(self, Eset:set, state):
		key = (state, automaton.epsilon)
		S = self.NFA.Delta(key)
		if S[0] != None:
			for s in S:
				self.__ECLOSE_R__(Eset, s)
			Eset.update(S)

	# regresa el conjunto de estados que tiene transicion epsilon para cada
	# estado dentro de states
	def __ECLOSE__(self, states:set):
		E = set()
		E.update(states)

		for e in states:
			self.__ECLOSE_R__(E, e)
			
		return E


	# implementacion la funcion move
	# simplemente se consulta para cada estado en states con el simbolo symbol
	# regresa el conjunto de estados a los que se puede llegar desde cada
	# estado en states con symbol
	def __MOVE__(self, states:set, symbol:str):
		M = set()
		
		for s in states:
			key = (s, symbol)
			D = self.NFA.Delta(key)
			if D[0] != None:
				M.update(D)
		
		return M

