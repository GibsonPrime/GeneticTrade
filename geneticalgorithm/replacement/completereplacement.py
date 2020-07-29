from typing import List
from ..member import Member
from .replacementmethod import ReplacementMethod

class CompleteReplacement(ReplacementMethod):
	"""Replace all
	
	Entire population will be replaced."""
	# ============
	# Methods
	# ============
	def nextPop(self, in_population: List[Member]) -> List[Member]:		
		return []
