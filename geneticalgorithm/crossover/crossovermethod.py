import random
from typing import List, Tuple
from abc import ABC
from enum import Enum
from ..utils import mcutils
from ..member import Member

# ================================================
# Crossover Methods
# ================================================
class CrossoverSelectionMethod(Enum):
	"""Crossover selection method enumerator
	
	1 = Linear - Select crossover pool members first to last.
	2 = Random - Randomly crossover pool members.  Members will be different.
	3 = LinearRandom - Select first member first to last, select second, 
	different member randomly."""
	LINEAR = 1
	RANDOM = 2
	LINEARRANDOM = 3


class CrossoverMethod(ABC):
	"""Base class
	
	Extend this class to create a cutsom crossover method.
	Sub classes should override crossover method, which should call super().crossover().
	If custom properties are required at initialisation, super().__init__() should also be called.
	
	Crossover rate is crossover threshold.  For every crossover event,
	a random number is generated to dictate whether or not crossover occurs.
	If crossover occurs, corssover method is executed and children are produced.
	If no crossover occurs, parents are placed into output list.
	 
	Crossover selection method dictates how population members are selected
	for crossover.
	 
	Each input population member can only crossover once.
	 
	doShuffle flag dicates whether or not the input population list
	should be randomly shuffled prior to selection."""
	# ============
	# Properties
	# ============
	_crossoverRate = 0.0
	__selectionMethod = CrossoverSelectionMethod.LINEAR
	__doShuffle = False

	# ============
	# Methods
	# ============
	# ------------
	# Initialise
	# ------------
	def __init__(self, crossoverRate: float, crossoverSelectionMethod: CrossoverSelectionMethod, doShuffle: bool):
		# Input validation
		if not type(crossoverRate) is float:
			raise TypeError('crossoverRate must be float.')
		if crossoverRate <= 0:
			raise ValueError('crossoverRate must be greater than 0.')
		if not type(crossoverSelectionMethod) is CrossoverSelectionMethod:
			raise TypeError('crossoverSelectionMethod must be CrossoverSelectionMethod.')
		if not type(doShuffle) is bool:
			raise TypeError('doShuffle must be bool.')

		# Property assignment
		self._crossoverRate = crossoverRate
		self.__selectionMethod = crossoverSelectionMethod
		self.__doShuffle = doShuffle

	# ------------
	# Crossover
	# ------------
	def crossover(self, pool: List[Member]) -> List[Member]:
		# Input validation
		if len(pool) == 0:
			raise ValueError('pool must be non empty.')
		if not type(pool) is list:
			raise TypeError('pool must be list of Members')

		# Shuffle input list if crossover method requires it
		if self.__doShuffle:
			pool = mcutils.shuffleList(pool, len(pool))

	# ------------
	# Select memebers
	# ------------
	def _select(self, pool: List[Member]) -> Tuple[Member, Member]:
		# Input validation
		if len(pool) == 0:
			raise ValueError('pool must be non empty.')
		if not type(pool) is list:
			raise TypeError('pool must be list of Members')

		# Perform selection
		output = None
		if self.__selectionMethod == CrossoverSelectionMethod.LINEAR:
			output = self.__selectLinear(pool)
		elif self.__selectionMethod == CrossoverSelectionMethod.LINEARRANDOM:
			output = self.__selectLinearRandom(pool)
		else:
			output = self.__selectRandom(pool)

		if len(output) <= 0:
			raise RuntimeError('Member selection for crossover failed.  Selected members list is empty.')
		# Type check members
		if not (isinstance(output[0], Member) and isinstance(output[1], Member)):
		 	raise TypeError('pool must be list of Members')
		# Check members have equal chromosomes
		if len(output[0].getChromosome()) != len(output[1].getChromosome()):
			raise ValueError('Member chromosomes must be of equal length.')

		return output
	
	def __selectLinear(self, pool: List[Member]) -> Tuple[Member, Member]:
		"""Linear
		Select in input population list order
		Members can only be used once, so will be removed from input list
		after selection.  Hence, can always reference indicies 0 and 1."""
		return (pool[0], pool[1])

	def __selectLinearRandom(self, pool: List[Member]) -> Tuple[Member, Member]:
		"""LinearRandom
		Select first member in input population list order.
		Select second, different member at random."""
		# Select members
		i2 = -1
		while i2 <= 0:
			i2 = random.randint(0, len(pool) - 1)

		return (pool[0], pool[i2])

	def __selectRandom(self, pool: List[Member]) -> Tuple[Member, Member]:
		"""Random
		Select both members randomly, but ensure they are different"""
		i1 = random.randint(0, len(pool) - 1)
		i2 = -1
		while i2 < 0 or i2 == i1:
			i2 = random.randint(0, len(pool) - 1)

		return (pool[i1], pool[i2])
