from .mutationmethod import MutationMethod

class TweakByValueMutation(MutationMethod):
	"""Tweak By Value Mutation
	
	Modifies allele by +/- value."""
	# ============
	# Properties
	# ============
	__mutateValue = 0.0

	# ============
	# Methods
	# ============
	def __init__(self, mutationRate: float, mutateValue: float):
		super().__init__(mutationRate)
		if not(type(mutateValue) is float):
			raise TypeError('mutateValue must be float.')

		self.__mutateValue = mutateValue

	def _doMutate(self, allele: float) -> float:
		super()._doMutate(allele)
		if random.random() < 0.5:
			return allele + self.__mutateValue
		else:
			return allele - self.__mutateValue
