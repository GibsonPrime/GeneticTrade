# ================================================
# Genetic Algorithm Tests
# 
# These tests are mostly shite btw.  Just wanted something to
# run a verify, but limited cases, all manually generated, testing
# functions rather than properties etc. etc.
# 
# This needs to be split up, fixed and deleted.
# ================================================
import unittest
from genetic_algorithm import *


# ------------------------------------------------
# Member
# ------------------------------------------------
class TestMember(unittest.TestCase):
	# ------------
	# Initialise valid and gets
	# ------------
	def test_initValidAndGets(self):
		chromosomes = [
		[0.1, 54.3, 543.2, 5.2], 
		[0.000002, 345.234, 45.34, 56456.43, 4.5, 3.4, 656.3, 29945.3, 8943234.3, 48584.2, 3.4, 0.1, 4350.34234, 45353.2],
		[1.1, 3.4, 56.3, 99.3],
		[0.1]]

		fitnesses = [3.4, 4564564564.234, 0.000001, 345.24354]

		for i in range(0, len(fitnesses) - 1):
			m = Member(chromosomes[i], fitnesses[i])
			self.assertIsInstance(m, Member)
			self.assertEqual(m.getChromosome(), chromosomes[i])
			self.assertEqual(m.getFitness(), fitnesses[i])

	# ------------
	# Initialise invalid
	# ------------
	def test_initInvalid_chromosomeType(self):
		# Invalid chromosome type
		with self.assertRaises(TypeError) as cm:
			Member("string", 0.1)
		with self.assertRaises(TypeError) as cm:
			Member(1, 0.1)
		with self.assertRaises(TypeError) as cm:
			Member(True, 0.1)
		with self.assertRaises(TypeError) as cm:
			Member([0.1, "0.3", 0.2], 0.1)
		with self.assertRaises(TypeError) as cm:
			Member([0.4, 0.9, True], 0.1)
		with self.assertRaises(TypeError) as cm:
			Member([4, 0.9, 0.2], 0.1)

	def test_initInvalid_chromosomeValue(self):
		# Invalid chromosome value
		with self.assertRaises(ValueError) as cm:
			Member([], 0.1)

	def test_initInvalid_fitnessType(self):
		# Invalid fitness type
		with self.assertRaises(TypeError) as cm:
			Member([0.1], 1)
		with self.assertRaises(TypeError) as cm:
			Member([0.1], "string")
		with self.assertRaises(TypeError) as cm:
			Member([0.1], False)

	# ------------
	# Set fitness
	# ------------
	def test_setFitnessValid(self):
		fitnesses = [3.4, 4564564564.234, 0.000001, 345.24354, 5555.4, 23.1, 54.3, 0.0123412]

		m = Member([0.1], 0.2)

		for i in range(0, len(fitnesses) - 1):
			m.setFitness(fitnesses[i])
			self.assertEqual(m.getFitness(), fitnesses[i])

	def test_setFitnessInvalid_type(self):
		m = Member([0.1], 0.2)

		fitnesses = [1, True, m, "0.3"]

		for i in range(0, len(fitnesses) - 1):
			with self.assertRaises(TypeError) as cm:
				m.setFitness(fitnesses[i])


# ================================================
# Selection Methods
# ================================================
# ------------------------------------------------
# Base class
# ------------------------------------------------
class TestSelectionMethod(unittest.TestCase):
	# ------------
	# Initialise valid
	# ------------
	def test_initValid(self):
		targetNumMembers = [1,999999,123,43,1235,23]

		for i in range(0, len(targetNumMembers)):
			sm = SelectionMethod(targetNumMembers[i])
			self.assertIsInstance(sm, SelectionMethod)

	# ------------
	# Initialise invalid
	# ------------
	def test_initInvalid_targetNumMembersType(self):
		targetNumMembers = ["string", 0.34, False]

		for i in range(0, len(targetNumMembers)):
			with self.assertRaises(TypeError) as cm:
				sm = SelectionMethod(targetNumMembers[i])

	def test_initInvalid_targetNumMembersValue(self):
		targetNumMembers = [0, -1]

		for i in range(0, len(targetNumMembers)):
			with self.assertRaises(ValueError) as cm:
				sm = SelectionMethod(targetNumMembers[i])

	# ------------
	# Select invalid
	# ------------
	def test_selectInvalid_populationEmpty(self):
		sm = SelectionMethod(1)
		with self.assertRaises(ValueError) as cm:
			sm.select([])

	def test_selectInvalid_populationType(self):
		sm = SelectionMethod(1)
		inputs = [True, 1, "string"]

		for i in range (0, len(inputs)):
			with self.assertRaises(TypeError) as cm:
				sm.select(inputs[i])

	# ------------
	# Get probabilities valid
	# ------------
	def test_getProbabilitiesValid(self):
		populations = [
		[Member([0.1], 1.0), Member([0.1], 1.0), Member([0.1], 1.0), Member([0.1], 1.0)],
		[Member([0.1], 1.0), Member([0.1], 2.0), Member([0.1], 3.0), Member([0.1], 4.0)],
		[Member([0.1], 0.1), Member([0.1], 0.1), Member([0.1], 0.1), Member([0.1], 0.1)],
		[Member([0.1], 0.1), Member([0.1], 0.2), Member([0.1], 0.3), Member([0.1], 0.4)],
		[Member([0.1], 6666.0), Member([0.1], 7777.0), Member([0.1], 8888.0), Member([0.1], 9999.0)]]
		results = [
		[(0,1/4), (1,1/4 * 2), (2,1/4 * 3), (3,1/4 * 4)],
		[(0,1/10), (1,1/10 + 2/10), (2,1/10 + 2/10 + 3/10), (3,1/10 + 2/10 + 3/10 + 4/10)],
		[(0,0.1/0.4), (1,0.1/0.4 * 2), (2,0.1/0.4 * 3), (3,0.1/0.4 * 4)],
		[(0,0.1), (1,0.1 + 0.2), (2,0.1 + 0.2 + 0.3), (3,0.1 + 0.2 + 0.3 + 0.4)],
		[(0,6666/(6666+7777+8888+9999)), (1,6666/(6666+7777+8888+9999) + 7777/(6666+7777+8888+9999)), 
		(2,6666/(6666+7777+8888+9999) + 7777/(6666+7777+8888+9999) + 8888/(6666+7777+8888+9999)),
		(3,6666/(6666+7777+8888+9999) + 7777/(6666+7777+8888+9999) + 8888/(6666+7777+8888+9999) + 9999/(6666+7777+8888+9999))]]

		sm = SelectionMethod(1)

		for i in range(0, len(results)):
			self.assertEqual(sm._getProbabilities(populations[i], sum(m.getFitness() for m in populations[i])), results[i])

	# ------------
	# Get probabilities invalid
	# ------------
	def test_getProbabilitiesInvalid_summedFitnessType(self):
		sm = SelectionMethod(1)
		population = [Member([0.1],0.1), Member([0.1],0.1)]
		summedFitnesses = ["string", 1, True]

		for i in range(0, len(summedFitnesses)):
			with self.assertRaises(TypeError) as cm:
				sm._getProbabilities(population, summedFitnesses[i])

	def test_getProbabilitiesInvalid_summedFitnessZero(self):
		sm = SelectionMethod(1)
		population = [Member([0.1],0.1), Member([0.1],0.1)]

		with self.assertRaises(ValueError) as cm:
			sm._getProbabilities(population, 0.0)

	def test_getProbabilitiesInvalid_populationNonMemberType(self):
		sm = SelectionMethod(1)
		populations = [
		[Member([0.1],0.1),1],
		[Member([0.1],0.1),"test"],
		[Member([0.1],0.1),True]]

		for i in range(0,len(populations)):
			with self.assertRaises(TypeError) as cm:
				sm._getProbabilities(populations[0],1.0)


# ------------------------------------------------
# Proportional selection
# ------------------------------------------------
class TestMemberType(Member):
	memid = None
	def __init__(self, chromosome: List[float], fitness: float, memid: int):
		super().__init__(chromosome, fitness)
		self.memid = memid


class TestProportionalSelection(unittest.TestCase):
	# ------------
	# Do Proportional Select valid
	# ------------
	def test_doProportionalSelectValid(self):
		targetNumMembers = [10, 400, 5000]
		populations = [
		[TestMemberType([0.1],1.0,0), TestMemberType([0.1],2.0,1), TestMemberType([0.1],3.0,2), TestMemberType([0.1],4.0,3)],
		[TestMemberType([0.1],50.21,0), TestMemberType([0.1],123.95,1), TestMemberType([0.1],354.18,2), TestMemberType([0.1],456.21,3)],
		[TestMemberType([0.1],2568.115681,0), TestMemberType([0.1],3198.1525,1), TestMemberType([0.1],9999.9999,2), TestMemberType([0.1],5897.1526,3)]]
		probabilities = [
		[(0,0.1), (1,0.3), (2,0.6), (3,1.0)],
		[(0,0.0509979178304809), (1,0.176892996800569), (2,0.536630948148901), (3,1.0)],
		[(0,0.118547849486111), (1,0.266176724688491), (2,0.727783460846602), (3,1.0)]]
		expectedProportions = [
		[0.1, 0.2, 0.3, 0.4],
		[0.0509979178304809, 0.125895078970088, 0.359737951348332, 0.463369051851099],
		[0.118547849486111, 0.147628875202379, 0.461606736158112, 0.272216539153398]]

		for i in range(0, len(populations)):
			ps = ProportionalSelection(targetNumMembers[i])
			out = ps._ProportionalSelection__doProportionalSelect(populations[i], probabilities[i])
			self.assertEqual(len(out), targetNumMembers[i])
			self.assertNotEqual(out, populations[i])

			outProportions = [0,0,0,0]
			for m in out:
				self.assertIsInstance(m, Member)
				self.assertIn(m, populations[i])
				outProportions[m.memid] += 1

			for j, p in enumerate(outProportions):
				self.assertAlmostEqual(p / targetNumMembers[i], expectedProportions[i][j], delta=0.2)

	# ------------
	# Do Proportional Select invalid
	# Function private and only called locally, so no type checking is performed.
	# population size checked in Base.select, which is always called first.
	# population element type checked in Base.__getProbabilities, which is always called first.
	# probabilities generated by Base.__getProbabilities. If pop size != empty and elements are valid,
	# output list must be non empty.
	# ------------
	def test_doProportionalSelectInvalid_inputListLengthsDiffer(self):
		in1 = [1,2,3]
		in2 = [1,2,3,4]

		with self.assertRaises(ValueError) as cm:
			ps = ProportionalSelection(1)
			ps._ProportionalSelection__doProportionalSelect(in1, in2)


# ------------------------------------------------
# Stochastic selection
# ------------------------------------------------
class TestStochasticSelection(unittest.TestCase):
	# ------------
	# Get proportions valid
	# ------------
	def test_getProportionsValid(self):
		probabilities = [
		[(0,0.1), (1,0.3), (2,0.6), (3,1.0)],
		[(0,0.124324324324324), (1,0.356756756756757), (2,0.648648648648649), (3,1.0)],
		[(0,0.182379004771643), (1,0.397818677573279), (2,0.659713701431493), (3,1.0)]]
		results = [
		[0.05, 0.15, 0.3, 0.5],
		[0.0583756345177665, 0.16751269035533, 0.304568527918782, 0.469543147208122],
		[0.0814224196959783, 0.177604650101188, 0.294526696997824, 0.446446233205009]]

		ss = StochasticSelection(1)
		for i in range(0, len(probabilities)):
			out = ss._StochasticSelection__getProportions(probabilities[i])
			for j, val in enumerate(out):
				self.assertAlmostEqual(val, results[i][j], delta=0.000000000001)

	# ------------
	# Get proportions invalid
	# Function is private and only called from StochasticSelection.Select
	# with input generated by getProbabilities (test above).
	# ------------
	
	# ------------
	# Do stochastic select valid
	# ------------
	def test_doStochasticSelectValid(self):
		populations = [
		[TestMemberType([0.1],1.0,0), TestMemberType([0.1],2.0,1), TestMemberType([0.1],3.0,2), TestMemberType([0.1],4.0,3)],
		[TestMemberType([0.1],50.21,0), TestMemberType([0.1],123.95,1), TestMemberType([0.1],354.18,2), TestMemberType([0.1],456.21,3)],
		[TestMemberType([0.1],2568.115681,0), TestMemberType([0.1],3198.1525,1), TestMemberType([0.1],9999.9999,2), TestMemberType([0.1],5897.1526,3)]]
		proportions = [
		[0.25, 0.25, 0.25, 0.25],
		[0.1, 0.2, 0.3, 0.4],
		[0, 0, 0, 1.0]]
		targetNumMembers = 100

		ss = StochasticSelection(targetNumMembers)
		for i in range(0,len(populations)):
			out = ss._StochasticSelection__doStochasticSelect(populations[i], proportions[i])
			self.assertEqual(len(out), targetNumMembers)			
			outProportions = [0, 0, 0, 0]
			for m in out:
				self.assertIsInstance(m, Member)
				self.assertIn(m, populations[i])
				outProportions[m.memid] += 1

			for j, op in enumerate(outProportions):
				self.assertEqual(op/targetNumMembers, proportions[i][j])

	# ------------
	# Do stochastic select invalid
	# Function is private and only called from StochasticSelection.Select
	# with input generated by getProportions (test above).
	# ------------


# ------------------------------------------------
# Tournament selection
# ------------------------------------------------
class TestTournamentSelection(unittest.TestCase):
	# ------------
	# Select valid
	# ------------
	def test_selectValid(self):
		populations = [
		[TestMemberType([0.1],1.0,0), TestMemberType([0.1],2.0,1)],
		[TestMemberType([0.1],1.0,0), TestMemberType([0.1],2.0,1), TestMemberType([0.1],3.0,2)]]
		targetNumMembers = [3,10]

		# populations[0] and targetNumMembers[0] should
		# result in output of 3x member with ID 1.
		ts = TournamentSelection(targetNumMembers[0])
		out = ts.select(populations[0])
		self.assertEqual(len(out), targetNumMembers[0])
		for m in out:
			self.assertEqual(m.memid, 1)
			self.assertIsInstance(m, Member)
			self.assertIn(m, populations[0])

		# populations[1] and targetNumMembers[1] should
		# result in output of 10x member with ID 1 or 2.
		ts = TournamentSelection(targetNumMembers[1])
		out = ts.select(populations[1])
		self.assertEqual(len(out), targetNumMembers[1])
		for m in out:
			self.assertAlmostEqual(m.memid, 2, delta=1)
			self.assertIsInstance(m, Member)
			self.assertIn(m, populations[1])


# ------------------------------------------------
# Truncation selection
# ------------------------------------------------
class TestTruncationSelection(unittest.TestCase):
	# ------------
	# Initialise invalid
	# 
	# Valid init tested with selection
	# ------------
	def test_initialiseInvalid_numToTrimType(self):
		numToTrims = ["string", 4.5, False, None]
		for n in numToTrims:
			with self.assertRaises(TypeError) as cm:
				ts = TruncationSelection(1, n)
	
	def test_initialiseInvalid_numToTrimValue(self):
		numToTrims = [-999, -1, 0]
		for n in numToTrims:
			with self.assertRaises(ValueError) as cm:
				ts = TruncationSelection(1, n)

	# ------------
	# Select valid
	# 
	# Also tests valid initialisation
	# ------------
	def test_selectValid(self):
		population = [TestMemberType([0.1],1.0,0), TestMemberType([0.1],2.0,1), TestMemberType([0.1],3.0,2), TestMemberType([0.1],4.0,3), TestMemberType([0.1],5.0,4)]
		targetNumMembers = [5,10,15,20]
		numToTrims = [1,2,3,4]

		# Trim 1
		ts = TruncationSelection(targetNumMembers[0], numToTrims[0])
		out = ts.select(population)
		self.assertEqual(len(out), targetNumMembers[0])
		for m in out:
			self.assertNotEqual(m.memid, 0)
			self.assertIsInstance(m, Member)
			self.assertIn(m, population)

		# Trim 2
		ts = TruncationSelection(targetNumMembers[1], numToTrims[1])
		out = ts.select(population)
		self.assertEqual(len(out), targetNumMembers[1])
		for m in out:
			self.assertNotEqual(m.memid, 0)
			self.assertNotEqual(m.memid, 1)
			self.assertIsInstance(m, Member)
			self.assertIn(m, population)

		# Trim 3
		ts = TruncationSelection(targetNumMembers[2], numToTrims[2])
		out = ts.select(population)
		self.assertEqual(len(out), targetNumMembers[2])
		for m in out:
			self.assertNotEqual(m.memid, 0)
			self.assertNotEqual(m.memid, 1)
			self.assertNotEqual(m.memid, 2)
			self.assertIsInstance(m, Member)
			self.assertIn(m, population)

		# Trim 4
		ts = TruncationSelection(targetNumMembers[3], numToTrims[3])
		out = ts.select(population)
		self.assertEqual(len(out), targetNumMembers[3])
		for m in out:
			self.assertNotEqual(m.memid, 0)
			self.assertNotEqual(m.memid, 1)
			self.assertNotEqual(m.memid, 2)
			self.assertNotEqual(m.memid, 3)
			self.assertIsInstance(m, Member)
			self.assertIn(m, population)

	# ------------
	# Select invalid
	# 
	# Population validated by base class.
	# numToTrim otherwise validated in class __init__.
	# ------------
	def test_selectInvalid_numToTrimTooLarge(self):
		population = [1,2,3]
		numToTrim = [3,4]

		for i in range(0,len(numToTrim)):
			ts = TruncationSelection(1,numToTrim[i])
			with self.assertRaises(IndexError) as cm:
				ts.select(population)

# ================================================
# Crossover Methods
# ================================================
# ------------------------------------------------
# Base class
# ------------------------------------------------
class TestCrossoverMethod(unittest.TestCase):
	# ------------
	# Initialise valid
	# ------------
	def test_initValid(self):
		crossoverRates = [0.1, 0.2, 0.3]
		crossoverSelectionMethods = [CrossoverSelectionMethod.LINEAR, CrossoverSelectionMethod.RANDOM, CrossoverSelectionMethod.LINEARRANDOM]
		doShuffles = [True, True, False]

		for i in range(0,len(crossoverRates)):
			crossMethod = CrossoverMethod(crossoverRates[i], crossoverSelectionMethods[i], doShuffles[i])
			self.assertIsInstance(crossMethod, CrossoverMethod)
			self.assertEqual(crossMethod._crossoverRate, crossoverRates[i])

	# ------------
	# Initialise invalid
	# ------------
	def test_initInvalid_crossoverRateType(self):
		crossoverRates = [1, False, "2"]
		for i in range(0,len(crossoverRates)):
			with self.assertRaises(TypeError) as cm:
				crossMethod = CrossoverMethod(crossoverRates[i], CrossoverSelectionMethod.LINEAR, False)

	def test_initInvalid_crossoverRateValue(self):
		crossoverRates = [-99.9, 0.0, -0.00001]
		for i in range(0,len(crossoverRates)):
			with self.assertRaises(ValueError) as cm:
				crossMethod = CrossoverMethod(crossoverRates[i], CrossoverSelectionMethod.LINEAR, False)

	def test_initInvalid_crossoverSelectionMethodType(self):
		selectionMethods = ["LINEAR", 1, False]
		for i in range(0,len(selectionMethods)):
			with self.assertRaises(TypeError) as cm:
				crossMethod = CrossoverMethod(0.1, selectionMethods[i], False)

	def test_initInvalid_doShuffleType(self):
		doShuffles = ["True", 0, 1.0]
		for i in range(0,len(doShuffles)):
			with self.assertRaises(TypeError) as cm:
				crossMethod = CrossoverMethod(0.1, CrossoverSelectionMethod.LINEAR, doShuffles[i])

	# ------------
	# Crossover valid
	# ------------
	def test_crossoverValid(self):
		pool = [TestMemberType([0.1],1.0, 1), TestMemberType([0.2],2.0,2), TestMemberType([0.3],3.0,3),
		TestMemberType([0.4],4.0, 4), TestMemberType([0.5],5.0,5), TestMemberType([0.6],6.0,6)]
		
		crossMethod = CrossoverMethod(0.1, CrossoverSelectionMethod.LINEAR, False)
		crossMethod.crossover(pool)
		for i in range(0,len(pool)):
			self.assertEqual(pool[i].memid, i+1)
		
		poolCopy = pool.copy()
		crossMethod = CrossoverMethod(0.1, CrossoverSelectionMethod.LINEAR, True)
		crossMethod.crossover(pool)
		exactMatch = True
		for i, m in enumerate(pool):
			if m.memid != poolCopy[i].memid:
				exactMatch = False
		self.assertNotEqual(exactMatch, True)

	# ------------
	# Crossover invalid
	# ------------
	def test_crossoverInvalid_poolEmpty(self):
		pool = []
		crossMethod = CrossoverMethod(0.1, CrossoverSelectionMethod.LINEAR, False)
		with self.assertRaises(ValueError) as cm:
			crossMethod.crossover(pool)

	def test_crossoverInvalid_poolNotList(self):
		pools = [1, "pool", False]
		crossMethod = CrossoverMethod(0.1, CrossoverSelectionMethod.LINEAR, False)
		for i in range(0,len(pools)):
			with self.assertRaises(TypeError) as cm:
				crossMethod.crossover(pools[i])

	# ------------
	# Select valid
	# Also tests private selection functions
	# ------------
	def test_selectValid(self):
		pools = [
		[TestMemberType([0.1],1.0, 1), TestMemberType([0.2],2.0,2), TestMemberType([0.3],3.0,3)],
		[TestMemberType([0.4],4.0, 4), TestMemberType([0.5],5.0,5), TestMemberType([0.6],6.0,6)],
		[TestMemberType([0.7],7.0, 7), TestMemberType([0.8],8.0,8), TestMemberType([0.9],9.0,9)]]
		crossoverSelectionMethods = [CrossoverSelectionMethod.LINEAR, CrossoverSelectionMethod.RANDOM, CrossoverSelectionMethod.LINEARRANDOM]

		# Linear
		crossMethod = CrossoverMethod(0.1, CrossoverSelectionMethod.LINEAR, False)
		for i in range(0,len(pools)):
			out = crossMethod._select(pools[i].copy())
			self.assertEqual(out[0],pools[i][0])
			self.assertEqual(out[1],pools[i][1])

		# Linear Random
		crossMethod = CrossoverMethod(0.1, CrossoverSelectionMethod.LINEARRANDOM, False)
		for i in range(0,len(pools)):
			out = crossMethod._select(pools[i].copy())
			self.assertEqual(out[0],pools[i][0])
			self.assertIn(out[1],pools[i])

		# Random
		crossMethod = CrossoverMethod(0.1, CrossoverSelectionMethod.RANDOM, False)
		for i in range(0,len(pools)):
			out = crossMethod._select(pools[i].copy())
			self.assertIn(out[0],pools[i])
			self.assertIn(out[1],pools[i])

	# ------------
	# Select invalid
	# ------------
	def test_selectInvalid_poolEmpty(self):
		pool = []
		crossMethod = CrossoverMethod(0.1, CrossoverSelectionMethod.LINEARRANDOM, False)
		with self.assertRaises(ValueError) as cm:
			crossMethod._select(pool.copy())

	def test_selectInvalid_poolType(self):
		pool = "list"
		crossMethod = CrossoverMethod(0.1, CrossoverSelectionMethod.LINEARRANDOM, False)
		with self.assertRaises(TypeError) as cm:
			crossMethod._select(pool)

	def test_selectInvalid_poolElementType(self):
		pool = [TestMemberType([0.1],1.0, 1), "Member"]
		crossMethod = CrossoverMethod(0.1, CrossoverSelectionMethod.LINEARRANDOM, False)
		with self.assertRaises(TypeError) as cm:
			crossMethod._select(pool)

	def test_selectInvalid_chromsomeLengthError(self):
		pool = [TestMemberType([0.1, 0.2],1.0, 1), TestMemberType([0.2],2.0,2), TestMemberType([0.3, 0.4, 0.5],3.0,3)]
		crossMethod = CrossoverMethod(0.1, CrossoverSelectionMethod.LINEARRANDOM, False)
		with self.assertRaises(ValueError) as cm:
			crossMethod._select(pool.copy())


# ------------------------------------------------
# Uniform crossover
# ------------------------------------------------
#class UniformCrossoverTestType(UniformCrossover):
#	def setMembers(self, members):
#		self.__members = members

class TestUniformCrossover(unittest.TestCase):
	# ------------
	# Initialise invalid
	# ------------
	def test_initInvalid_fitnessBiasType(self):
		biases = [1, 4.3, "True"]
		for i in range(0,len(biases)):
			with self.assertRaises(TypeError) as cm:
				uco = UniformCrossover(0.1, CrossoverSelectionMethod.LINEAR, False, biases[i])

	# ------------
	# Crossover valid
	# ------------
	def test_crossoverValid(self):
		pool1 = [TestMemberType([0.1],1.0, 1), TestMemberType([0.2],2.0,2), TestMemberType([0.3],3.0,3),
		TestMemberType([0.4],4.0, 4), TestMemberType([0.5],5.0,5), TestMemberType([0.6],6.0,6)]
		pool2 = [TestMemberType([0.1],1.0, 1), TestMemberType([0.2],2.0,2), TestMemberType([0.3],3.0,3),
		TestMemberType([0.4],4.0, 4), TestMemberType([0.5],5.0,5)]

		uco = UniformCrossover(0.1, CrossoverSelectionMethod.LINEAR, False, False)

		out1 = uco.crossover(pool1)
		self.assertIsInstance(out1, list)
		self.assertEqual(len(out1), 6)
		for m in out1:
			self.assertIsInstance(m, Member)

		out2 = uco.crossover(pool2)
		self.assertIsInstance(out2, list)
		self.assertEqual(len(out2), 4)
		for m in out2:
			self.assertIsInstance(m, Member)

	# ------------
	# Generate bias valid
	# ------------
	def test_generateBiasValid(self):
		# no fitness bias - 50/50
		pool = [TestMemberType([0.1],1.0, 1), TestMemberType([0.2],2.0,2)]
		uco = UniformCrossover(0.1, CrossoverSelectionMethod.LINEAR, False, False)
		uco._select(pool.copy())
		b = uco._UniformCrossover__generateBias()
		self.assertEqual(b,0.5)

		# fitness bias
		# Would be nice to test, but self.__members is always empty.  Fuck knows why.
		# len(self.__members) in setMembers function returns 2.
		# bTarget = 1/3
		# uco = UniformCrossoverTestType(0.1, CrossoverSelectionMethod.LINEAR, False, True)
		# uco.setMembers(uco._select(pool.copy()))
		# b = uco._UniformCrossover__generateBias()
		# self.assertEqual(b,bTarget)


if __name__ == '__main__':
    unittest.main()
