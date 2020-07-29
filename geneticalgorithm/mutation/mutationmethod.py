import random
from typing import List
from abc import ABC
from ..member import Member

class MutationMethod(ABC):
	"""Base class

	Extend this class to create a cutsom mutation method.
	Sub classes should override _doMutate method, which should call super()._doMutate().
	If custom properties are required at initialisation, super().__init__() should also be called.
	"""
	# ============
	# Properties
	# ============
	__mutationRate = 0.0

	# ============
	# Methods
	# ============
	def __init__(self, mutationRate: float):
		if not(type(mutationRate) is float):
			raise TypeError('mutationRate must be float.')
		if 0.0 > mutationRate > 1.0:
			raise ValueError('mutationRate must be between 0.0 and 1.0.')

		self.__mutationRate = mutationRate

	def mutate(self, in_population: List[Member]) -> List[Member]:
		population = in_population.copy()
		for m in population:
			if random.random() < self.__mutationRate:
				i = random.randint(0, len(m.getChromosome()) - 1)
				m.setAllele(i, self._doMutate(m.getChromosome()[i]))

		return population

	def _doMutate(self, allele: float) -> float:
		if not(type(allele) is float):
			raise TypeError('allele must be float.')
