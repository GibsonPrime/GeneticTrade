from .mutationmethod import MutationMethod

class BitFlipMutation(MutationMethod):
	"""Bit Flip Mutation
	
	Swap a 0 to a 1 and a 1 to a 0."""
	# ============
	# Methods
	# ============
	def _doMutate(self, allele: float) -> float:
		super()._doMutate(allele)

		if not(allele == 1.0 or allele == 0.0):
			raise ValueError('Allele must be 0 or 1 for bit flip mutation.')

		if allele == 1.0:
			return 0.0
		else:
			return 1.0
