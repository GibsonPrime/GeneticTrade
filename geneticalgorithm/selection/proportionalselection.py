import random
from typing import List, Tuple
from ..member import Member
from ..utils import mcutils
from ..utils.membersortingcomparator import MemberSortingComparator
from .selectionmethod import SelectionMethod

class ProportionalSelection(SelectionMethod):
	"""Proportional selection
	
	Member has propbability of selection proportional to relative fitness:
	1. Generate relative fitness (probability) = member fitness / sum of all fitnesses.
	2. Sort probabilities in ascending order.
	3. Generate random number.
	4. For each probability, if random number < probability, add member to
	output population."""
	# ============
	# Methods
	# ============
	# ------------
	# Initialise
	# ------------
	def __init__(self, targetNumMembers: int):
		super().__init__(targetNumMembers)

	# ------------
	# Select
	# ------------
	def select(self, in_population: List[Member]) -> List[Member]:
		population = in_population.copy()

		# Call base
		super().select(population)
		# Sort population by fitness ascending
		population = mcutils.mergeSortList(population, MemberSortingComparator())
		# Generate list of (member index in population, probability) tuples.		
		probabilities = self._getProbabilities(population, sum([member.getFitness() for member in population]))		
		# Return output
		return self.__doProportionalSelect(population, probabilities)

	def __doProportionalSelect(self, population: List[Member], probabilities: List[Tuple[int, float]]) -> List[Member]:
		"""Performs proportional selection
		Generate random number, select first member with probability > random number"""
		# Input validation
		if len(population) != len(probabilities):
			raise ValueError('population and probabilities lists must be of equal length.')

		# Generate proportionally selected list
		outputList = []		
		while len(outputList) < self._targetNumMembers:
			rand = random.random()
			for i in range(0, len(probabilities)):				
				if rand < probabilities[i][1]:
					outputList.append(population[probabilities[i][0]])
					break

		return outputList
