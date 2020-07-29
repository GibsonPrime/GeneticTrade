from typing import List
from abc import ABC
from ..member import Member

class ReplacementMethod(ABC):
	"""Base class
	
	Extend this class to create a cutsom replacement method.
	Sub classes should override nextPop method, which should call super().nextPop().
	There is no initialisation required for the base class.
	"""
	# ============
	# Methods
	# ============
	def nextPop(self, population: List[Member]) -> List[Member]:
		# Input validation
		if len(population) == 0:
			raise ValueError('population must be non empty.')
		if not(type(population) is list and type(population[0] is Member)):
			raise TypeError('population must be list of Members')
