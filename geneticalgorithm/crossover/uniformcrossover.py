import random
from typing import List
from ..member import Member
from ..utils import mcutils
from .crossovermethod import CrossoverMethod
from .crossovermethod import CrossoverSelectionMethod

class UniformCrossover(CrossoverMethod):
	"""Uniform crossover
	
	1. Select next two members of input population list.
	2. Select allele with probability of selection from each parent.
	3. Iterate until output population size is equal to input population
	size.
	
	fitnessBias flag introduces bias in allele selection based on member fitness.
	If fitnessBias is not set, probability is 50/50."""
	# ============
	# Properties
	# ============
	__fitnessBias = False
	__members = None

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
				fitnessBias: bool):
		super().__init__(crossoverRate, crossoverSelectionMethod, doShuffle)

		# Input validation
		if not type(fitnessBias) is bool:
			raise TypeError('fitnessBias must be bool.')

		# Property assignment
		self.__fitnessBias = fitnessBias

	# ------------
	# Crossover
	# ------------
	def crossover(self, in_pool: List[Member]) -> List[Member]:
		pool = in_pool.copy()

		super().crossover(pool)

		# Generate output list
		outputList = []
		while len(pool) >= 2:
			# Get members and remove parents from input population pool			
			self.__members = super()._select(pool)
			pool.remove(self.__members[0])
			pool.remove(self.__members[1])

			bias = self.__generateBias()
			self.__doUniformCrossover(bias)
			outputList.append(self.__members[0])
			outputList.append(self.__members[1])

		# Return output list
		return outputList

	def __generateBias(self) -> float:
		"""Generate bias
		If fitness based bias is enabled, bias = lowest proportional fitness
		Otherwise, return 0.5 (50/50 - no bias)"""
		if self.__fitnessBias:
			# Get fitness of members relative to each other.
			summedFitness = self.__members[0].getFitness() + self.__members[1].getFitness()
			propMember1 = self.__members[0].getFitness() / summedFitness
			propMember2 = self.__members[1].getFitness() / summedFitness

			# Set bias threshold to lowest relative fitness
			if propMember1 < propMember2:
				return propMember1
			else:
				# If fitness of member 1 is > fitness of member 2, swap members.
				# Perform crossover algorithm requires lowest scoring member appear first.
				self.__members = self.__members[::-1]
				return propMember2
		else:
			return 0.5

	def __doUniformCrossover(self, bias: float):
		"""Do uniform crossover
		Generate random number.  
		If random number meets crossover threshold generate children, selecting alleles based on bias.
		Otherwise, return parents."""
		if not type(bias) is float:
			raise TypeError('bias must be float.')

		rand = random.random()
		if rand < self._crossoverRate:
			child1Chromosome = []
			child2Chromosome = []
			for alleleI in range(0, len(self.__members[0].getChromosome())):
				rand = random.random()
				if(rand < bias):
					child1Chromosome.append(self.__members[0].getChromosome()[alleleI])
					child2Chromosome.append(self.__members[1].getChromosome()[alleleI])
				else:
					child1Chromosome.append(self.__members[1].getChromosome()[alleleI])
					child2Chromosome.append(self.__members[0].getChromosome()[alleleI])

			# Replace parents with children
			self.__members = (Member(child1Chromosome, 0.0), Member(child2Chromosome, 0.0))
