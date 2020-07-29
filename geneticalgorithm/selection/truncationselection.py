import random
from typing import List
from ..member import Member
from ..utils import mcutils
from ..utils.membersortingcomparator import MemberSortingComparator
from .selectionmethod import SelectionMethod

class TruncationSelection(SelectionMethod):
	"""Truncation selection

	Eliminate fixed number of weakest members, then create new population 
	randomly from remainder:
	1. Sort input population by fitness (descending).
	2. Delete weakest members (equal to numToTrim).
	3. Randomly select from remaining members until output population 
	size is equal to target population size."""
	# ============
	# Properties
	# ============	
	__numToTrim = 0

	# ============
	# Methods
	# ============
	# ------------
	# Initialise
	# ------------
	def __init__(self, targetNumMembers: int, numToTrim: int):
		super().__init__(targetNumMembers)

		# Input validation
		if not type(numToTrim) is int:
			raise TypeError('numToTrim must be int.')
		if numToTrim <= 0:
			raise ValueError('numToTrim must be greater than 0.')

		# Property assignment
		self.__numToTrim = numToTrim

	# ------------
	# Select
	# ------------
	def select(self, in_population: List[Member]) -> List[Member]:
		population = in_population.copy()

		# Call base
		super().select(population)

		# Check that population size > numToTrim index
		if len(population) <= self.__numToTrim:
			raise IndexError('numToTrim index must be less than population size.')

		# Sort population by fitness and trim
		popTrimmed = mcutils.mergeSortList(population, MemberSortingComparator())
		del popTrimmed[0:self.__numToTrim]

		# Generate output list
		outputList = []		
		while len(outputList) < self._targetNumMembers:
			outputList.append(popTrimmed[random.randint(0, len(popTrimmed) - 1)])

		# Return output
		return outputList
