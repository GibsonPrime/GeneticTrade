import random
from .mutationmethod import MutationMethod

class TweakByPercentageMutation(MutationMethod):
	"""Tweak By Percentage Mutation
	
	Modifies allele by +/- % of current value."""
	# ============
	# Properties
	# ============
	__mutatePercentage = 0.0

	# ============
	# Methods
	# ============
	def __init__(self, mutationRate: float, mutatePercentage: float):
		super().__init__(mutationRate)
		if not(type(mutatePercentage) is float):
			raise TypeError('mutatePercentage must be float.')
		if not(0.0 < mutatePercentage < 100.0):
			raise ValueError('mutatePercentage must be between 0 and 100.')

		self.__mutatePercentage = mutatePercentage / 100

	def _doMutate(self, allele: float) -> float:
		super()._doMutate(allele)

		if random.random() < 0.5:
			return allele + (allele*self.__mutatePercentage)
		else:
			return allele - (allele*self.__mutatePercentage)
