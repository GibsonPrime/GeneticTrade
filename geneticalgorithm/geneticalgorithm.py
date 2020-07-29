from typing import List
from .member import Member
from .selection.selectionmethod import SelectionMethod
from .crossover.crossovermethod import CrossoverMethod
from .replacement.replacementmethod import ReplacementMethod
from .mutation.mutationmethod import MutationMethod


class GeneticAlgorithm:
	"""Genetic Algorithm
	
	An implementation of genetic algorithm, with configurable
	selection, crossover and population replacement methods.
	
	It provides a basic population Member class which should be
	inherited by a project implementation which represents project
	specific member traits and functions.
	
	The execution of the system executes the select, replace and crossover
	functions.  The "run" part of the process and the fitness function
	must be defined in the project layer.
	
	Custom selection, replace and crossover functions can be
	implemented by inheriting the respective base classes.
	
	Selection method - Dictates members who have a chance to crossover
	Replace method - Dictates which members of the population are replaced
	Crossover method - Produces children or retains parents based on crossover rate
	
	Use:
	1. Instantiate selection and crossover method objects
	2. Instantiate a GeneticAlgorithm using those objects
	3. Add Members to the GeneticAlgorithm population
	4. Test the population against your training set in the project layer
	5. Update the fitness value for each Member
	6. Check for stopping criteria in project layer
	7. Call GeneticAlgorithm.execute()"""
	
	# ============
	# Properties
	# ============	
	__population = []
	__selectionMethod = None
	__crossoverMethod = None
	__mutationMethod = None
	__replacementMethod = None

	# ============
	# Methods
	# ============
	# ------------
	# Initialise
	# ------------
	def __init__(
		self,
		selectionMethod: SelectionMethod,
		crossoverMethod: CrossoverMethod,
		replacementMethod: ReplacementMethod,
		mutationMethod: MutationMethod):
		# Input validation
		if not isinstance(selectionMethod, SelectionMethod):
			raise TypeError('selectionMethod must be an instance of a sub class of SelectionMethod.')
		if not isinstance(crossoverMethod, CrossoverMethod):
			raise TypeError('crossoverMethod must be an instance of a sub class of CrossoverMethod.')
		if not isinstance(replacementMethod, ReplacementMethod):
			raise TypeError('replacementMethod must be an instance of a sub class of ReplacementMethod.')
		if not isinstance(mutationMethod, MutationMethod):
			raise TypeError('mutationMethod must be an instance of a sub class of MutationMethod.')		

		# Property assignment
		self.__selectionMethod = selectionMethod
		self.__crossoverMethod = crossoverMethod
		self.__mutationMethod = mutationMethod
		self.__replacementMethod = replacementMethod

	# ------------
	# Execute
	# ------------
	def execute(self):
		# Check setup
		if len(self.__population) == 0:
			return ValueError('Population has no members.')

		# Execute
		crossoverPool = self.__selectionMethod.select(self.__population)		
		crossovers = self.__crossoverMethod.crossover(crossoverPool)
		self.__population = self.__replacementMethod.nextPop(self.__population)		
		self.__population.extend(crossovers)
		self.__population = self.__mutationMethod.mutate(self.__population)

	# ------------
	# Population access
	# ------------
	def getPopulation(self) -> List[Member]:
		return self.__population.copy()

	def addMember(self, member: Member):
		# Input validation
		if not (isinstance(member, Member)):
			raise TypeError('member must be an instance of, or instance of a sub class of Member.')
		if len(self.__population) > 0 and len(self.__population[0].getChromosome()) != len(member.getChromosome()):
				raise ValueError('Members of a single population must have chromosomes of equal length.')

		# Add member
		self.__population.append(member)

	def removeMember(self, member):
		# Input validation
		if not (isinstance(member, Member)):
			raise TypeError('member must be an instance of, or instance of a sub class of Member.')

		# Remove member
		self.__population.remove(member)

	def clearPopulation(self):
		if not(type(self.__population) is None):
			self.__population.clear()

	def setMemberFitness(self, memberIndex: int, fitness: float):
		self.__population[memberIndex].setFitness(fitness)
