from typing import List
from . import mcutils
from ..member import Member

class MemberSortingComparator(mcutils.MergeSortListComparator):
	"""Member sorting comparator.

	For use with mcutils.mergeSortList."""
	@staticmethod
	def compare(a: List[Member], b: List[Member]) -> bool:
		return a[0].getFitness() <= b[0].getFitness()