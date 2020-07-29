from typing import List, Tuple
from abc import ABC
from ..member import Member

class SelectionMethod(ABC):
	"""Base class

	Extend this class to create a cutsom selection method.
	Sub classes should override select() method, which should call super().select().
	If custom properties are required at initialisation, super().__init__() should also be called.
	"""
	# ============
	# Properties
	# ============	
	_targetNumMembers = 0

	# ============
	# Methods
	# ============	
	# ------------
	# Initialise
	# ------------
	def __init__(self, targetNumMembers: int):
		# Input validation
		if not type(targetNumMembers) is int:
			raise TypeError('targetNumMembers must be int.')
		if targetNumMembers <= 0:
			raise ValueError('targetNumMembers must be greater than 0.')

		# Property assignment
		self._targetNumMembers = targetNumMembers

	# ------------
	# Select
	# ------------
	def select(self, population: List[Member]) -> List[Member]:
		# Input validation
		if len(population) == 0:
			raise ValueError('population must be non empty.')
		if not type(population) is list:
			raise TypeError('population must be list of Members')

	# Generate list of (member index in population, probability) tuples.
	# Type checking of population elements also performed here.
	# Used by proportional and stochastic selection methods
	def _getProbabilities(self, population: List[Member], summedFitness: float) -> List[Tuple[int, float]]:
		# Input validation
		if not type(summedFitness) is float:
			raise TypeError('summedFitness must be float.')
		if summedFitness == 0:
			raise ValueError('summedFitness must be non 0.')

		outputList = []
		for i, member in enumerate(population):
			if not type(member) is Member:
				raise TypeError('population must be list of Members')
			if i > 0:
				outputList.append((i, outputList[i-1][1] + (member.getFitness() / summedFitness)))
			else:
				outputList.append((i, (member.getFitness() / summedFitness)))

		return outputList
