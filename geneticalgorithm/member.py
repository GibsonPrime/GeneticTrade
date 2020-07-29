from typing import List


class Member():
	""""Member
	
	Defines a population member."""
	
	# ============
	# Properties
	# ============	
	_chromosome = []
	_fitness = 0.0

	# ============
	# Methods
	# ============
	# ------------
	# Initialise
	# ------------
	def __init__(self, chromosome: List[float], fitness: float):
		# Input validation
		if len(chromosome) == 0:
			raise ValueError('chromosome must be non empty')
		if not type(chromosome) is list:
			raise TypeError('chromosome must be list of floats.')
		for a in chromosome:
			if not type(a) is float:
				raise TypeError('chromosome must be list of floats.')
		if not(type(fitness) is float):
			raise TypeError('fitness must be float.')

		# Property assignment
		self._chromosome = chromosome
		self._fitness = fitness

	# ------------
	# Access
	# ------------
	def getChromosome(self) -> List[float]:
		return self._chromosome

	def setAllele(self, index: int, allele: float):
		if not(type(index) is int):
			raise TypeError('index must be int.')
		if 0 > index > len(self._chromosome) - 1:
			raise IndexError('index must be within bounds of chromosome.')
		if not(type(allele) is float):
			raise TypeError('allele must be float.')

		self._chromosome[index] = allele

	def getFitness(self) -> float:
		return self._fitness

	def setFitness(self, fitness: float):
		if not(type(fitness) is float):
			raise TypeError('fitness must be float.')		
		self._fitness = fitness
