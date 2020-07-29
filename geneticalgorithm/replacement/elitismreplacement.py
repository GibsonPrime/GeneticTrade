from typing import List
from ..member import Member
from ..utils import mcutils
from ..utils.membersortingcomparator import MemberSortingComparator
from .replacementmethod import ReplacementMethod

class ElitismReplacement(ReplacementMethod):
	"""Replace with elitism replacement
	
	Retain n strongest members"""
	# ============
	# Properties
	# ============	
	__numMembersToRetain = 0

	# ============
	# Methods
	# ============	
	# ------------
	# Initialisation
	# ------------
	def __init__(self, numMembersToRetain: int):
		# Input validation
		if not type(numMembersToRetain) is int:
			raise TypeError('numMembersToRetain must be int.')

		# Property assignment
		self.__numMembersToRetain = numMembersToRetain

	# ------------
	# Next population
	# ------------
	def nextPop(self, in_population: List[Member]) -> List[Member]:
		population = in_population.copy()
		super().nextPop(population)
		sortedPop = mcutils.mergeSortList(population, MemberSortingComparator()) 
		del sortedPop[self.__numMembersToRetain - 1:len(population)]
		return sortedPop
