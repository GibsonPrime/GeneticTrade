import random
from typing import List
from ..member import Member
from .selectionmethod import SelectionMethod

class TournamentSelection(SelectionMethod):
	"""Tournament selection
	
	Select 2 random members, then chose the one with the highest fitness
	until output population size is equal to target population size."""
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

		# Generate output list
		# Type checking of population elements also performed here
		outputList = []
		while len(outputList) < self._targetNumMembers:			
			i1 = random.randint(0, len(population) - 1)
			i2 = -1
			while i2 < 0 and i2 == i1:
				i2 = random.randint(0, len(population) - 1)
			
			member1 = population[i1]
			member2 = population[i2]

			if not (isinstance(member1, Member) and isinstance(member2, Member)):
				raise TypeError('population must be list of Members')

			if member1.getFitness() > member2.getFitness():
				outputList.append(member1)
			else:
				outputList.append(member2)

		# Return output
		return outputList
