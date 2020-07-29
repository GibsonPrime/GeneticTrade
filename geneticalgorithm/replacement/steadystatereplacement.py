from typing import List
from ..member import Member
from ..utils import mcutils
from ..utils.membersortingcomparator import MemberSortingComparator
from .replacementmethod import ReplacementMethod

class SteadyStateReplacement(ReplacementMethod):
	"""Steady state replacement
	
	Discard n weakest members."""
	# ============
	# Properties
	# ============	
	__numMembersToRemove = 0

	# ============
	# Methods
	# ============	
	# ------------
	# Initialisation
	# ------------
	def __init__(self, numMembersToRemove: int):
		# Input validation
		if not type(numMembersToRemove) is int:
			raise TypeError('numMembersToRemove must be int.')

		# Property assignment
		self.__numMembersToRemove = numMembersToRemove

	# ------------
	# Next population
	# ------------
	def nextPop(self, in_population: List[Member]) -> List[Member]:
		population = in_population.copy()
		super().nextPop(population)
		sortedPop = mcutils.mergeSortList(population, MemberSortingComparator())
		del sortedPop[len(population) - self.__numMembersToRemove:len(population)]
		return sortedPop
