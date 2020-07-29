from typing import List, Tuple
from ..member import Member
from ..utils import mcutils
from ..utils.membersortingcomparator import MemberSortingComparator
from .selectionmethod import SelectionMethod

class StochasticSelection(SelectionMethod):
	"""Stochastic selection
	
	Member selected a number of times equal to expectation of selection under the 
	proportional method:
	1. Generate relative fitness (probability) - member fitness / sum of all fitnesses.
	2. Get proportional representation of relative fitnesses.
	3. Add member to output population number of times = proportion * input pop size"""
	# ============
	# Methods
	# ============
	# ------------
	# Initialise
	# ------------
	def __init__(self, targetNumMembers:int):
		super().__init__(targetNumMembers)

	# ------------
	# Select
	# ------------
	def select(self, in_population: List[Member]) -> List[Member]:		
		population = in_population.copy()

		# Call base
		super().select(population)
		# Sort input list
		population = mcutils.mergeSortList(population, MemberSortingComparator())
		probabilities = self._getProbabilities(population, sum([member.getFitness() for member in population]))
		return self.__doStochasticSelect(population, self.__getProportions(probabilities))

	def __getProportions(self, probabilities: List[Tuple[int, float]]) -> List[float]:
		"""Gets proportion of final population each member should be.
		i.e. each entry of output list inidicates if member should make up 10%, 25%, 50% etc. of output population."""
		summedProbabilities = sum(probabilities[i][1] for i in range(0, len(probabilities)))
		proportions = []
		for i in range(0, len(probabilities)):
			proportions.append(probabilities[i][1] / summedProbabilities)

		return proportions

	def __doStochasticSelect(self, population: List[Member], proportions: List[float]) -> List[Member]:
		"""Performs stochastic selection
		Generate random number, select first member with probability > random number"""
		outputList = []
		for i, member in enumerate(population):
			numOfCurrentMember = round(self._targetNumMembers * proportions[i])
			for i in range(0, numOfCurrentMember):
				outputList.append(member)

		return outputList
