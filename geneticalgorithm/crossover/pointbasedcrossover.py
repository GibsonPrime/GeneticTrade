import random
from typing import List, Tuple
from ..member import Member
from .crossovermethod import CrossoverMethod
from .crossovermethod import CrossoverSelectionMethod

class PointBasedCrossover(CrossoverMethod):
	"""Point based crossover
	
	1. Select next two members of input population list.
	2. Swap alleles from index points[0][0] to index points[0][1].
	3. Iterate until points exhausted.
	4. Iterate until output population size is equal to input population
	size.
	
	Best combined with LINEAR crossover selection method."""
	# ============
	# Properties
	# ============
	__points = []

	# ============
	# Methods
	# ============
	# ------------
	# Initialise
	# ------------
	def __init__(self, 
				crossoverRate: float, 
				crossoverSelectionMethod: CrossoverSelectionMethod, 
				doShuffle: bool, 
				points: List[Tuple[int,int]]):
		super().__init__(crossoverRate, crossoverSelectionMethod, doShuffle)

		# Input validation
		if len(points) <= 0:
			raise ValueError('points list must be non empty.')
		if len(points[0]) != 2:
			raise ValueError('points list tuples must be of length 2.')
		if not type(points) is list:
			raise TypeError('points must be list of (int, int) tuples.')

		# Property assignment
		self.__points = points	

	# ------------
	# Crossover
	# ------------
	def crossover(self, in_pool: List[Member]) -> List[Member]:
		pool = in_pool.copy()

		super().crossover(pool)

		# Generate output list
		outputList = []

		while len(pool) > 2:
			# Get members and remove parents from input population pool
			members = super()._select(pool)
			pool.remove(members[0])
			pool.remove(members[1])

			# Type check members
			if not (type(members[0]) is Member and type(members[1]) is Member):
			 	raise TypeError('pool must be list of Members')

			# Perform crossover
			rand = random.random()
			if rand < self._crossoverRate:
				child1Chromosome = members[0].getChromosome()
				child2Chromosome = members[1].getChromosome()

				# Iterate through all sets of crossover points
				for p in self.__points:
					# Type check p
					if not (type(p) is tuple and type(p[0]) is int and type(p[1]) is int):
						raise TypeError('points must be list of (int, int) tuples')
					if (0 > p[0] > len(pool) - 1) or (0 > p[1] > len(pool) - 1):
						raise IndexError('points must be within bounds of chromosome length')

					# Perform crossover for p
					for i in range(p[0], p[1]):
						child1Chromosome[i] = members[1].getChromosome()[i]
						child2Chromosome[i] = members[0].getChromosome()[i]
				
				# Add new members to output list
				outputList.append(Member(child1Chromosome, 0.0))
				outputList.append(Member(child2Chromosome, 0.0))
			else:
				# Add parents to output list
				outputList.append(members[0])
				outputList.append(members[1])

		# Return output list
		return outputList
