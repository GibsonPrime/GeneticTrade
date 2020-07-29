import random
import os
from geneticalgorithm.geneticalgorithm import GeneticAlgorithm
from geneticalgorithm.member import Member
from geneticalgorithm.selection.proportionalselection import ProportionalSelection
from geneticalgorithm.selection.stochasticselection import StochasticSelection
from geneticalgorithm.selection.tournamentselection import TournamentSelection
from geneticalgorithm.selection.truncationselection import TruncationSelection
from geneticalgorithm.crossover.crossovermethod import CrossoverSelectionMethod
from geneticalgorithm.crossover.uniformcrossover import UniformCrossover
from geneticalgorithm.crossover.pointbasedcrossover import PointBasedCrossover
from geneticalgorithm.replacement.completereplacement import CompleteReplacement
from geneticalgorithm.replacement.steadystatereplacement import SteadyStateReplacement
from geneticalgorithm.replacement.elitismreplacement import ElitismReplacement
from geneticalgorithm.mutation.bitflipmutation import BitFlipMutation
from geneticalgorithm.mutation.tweakbyvaluemutation import TweakByValueMutation
from geneticalgorithm.mutation.tweakbypercentagemutation import TweakByPercentageMutation


# Parameters
pop_size = 50
cross_rate = 0.2
trunc_selection_numToTrim = 10
steady_replacement_numToRemove = 45
elite_replacement_numToRetain = 5
chromosome_length = 20
mutation_rate = 0.001
points = [(0,5),(10,15)]
ga = None
max_gens = 2000

doRunFileOutput = False
doLogFileOutput = True
doConsoleOutput = True
run_inst = 0
selStart = 0
crossStart = 0
repStart = 0
mutStart = 0

if doLogFileOutput or doRunFileOutput:
	if not(os.path.isdir(".\\outputs")):
		os.mkdir("outputs")

if doLogFileOutput:
	logFile = open(".\\outputs\\00log00.txt", "w")

# Selection methods
selection_methods = [
	ProportionalSelection(pop_size),
	StochasticSelection(pop_size),
	TournamentSelection(pop_size),
	TruncationSelection(pop_size, trunc_selection_numToTrim)]

# Crossover methods
crossover_methods = [
	UniformCrossover(cross_rate, CrossoverSelectionMethod.LINEAR, False, False),
	UniformCrossover(cross_rate, CrossoverSelectionMethod.LINEAR, True, False),
	UniformCrossover(cross_rate, CrossoverSelectionMethod.LINEAR, False, True),
	UniformCrossover(cross_rate, CrossoverSelectionMethod.LINEAR, True, True),
	UniformCrossover(cross_rate, CrossoverSelectionMethod.LINEARRANDOM, False, False),
	UniformCrossover(cross_rate, CrossoverSelectionMethod.LINEARRANDOM, True, False),
	UniformCrossover(cross_rate, CrossoverSelectionMethod.LINEARRANDOM, False, True),
	UniformCrossover(cross_rate, CrossoverSelectionMethod.LINEARRANDOM, True, True),
	UniformCrossover(cross_rate, CrossoverSelectionMethod.RANDOM, False, False),
	UniformCrossover(cross_rate, CrossoverSelectionMethod.RANDOM, True, False),
	UniformCrossover(cross_rate, CrossoverSelectionMethod.RANDOM, False, True),
	UniformCrossover(cross_rate, CrossoverSelectionMethod.RANDOM, True, True),
	PointBasedCrossover(cross_rate, CrossoverSelectionMethod.LINEAR, False, points),
	PointBasedCrossover(cross_rate, CrossoverSelectionMethod.LINEAR, True, points),
	PointBasedCrossover(cross_rate, CrossoverSelectionMethod.LINEARRANDOM, False, points),
	PointBasedCrossover(cross_rate, CrossoverSelectionMethod.LINEARRANDOM, True, points),
	PointBasedCrossover(cross_rate, CrossoverSelectionMethod.RANDOM, False, points),
	PointBasedCrossover(cross_rate, CrossoverSelectionMethod.RANDOM, True, points)]

# Replacement methods
replacement_methods = [
	CompleteReplacement(),
	SteadyStateReplacement(steady_replacement_numToRemove),
	ElitismReplacement(elite_replacement_numToRetain)]

# Mutation methods
mutation_methods = [
	BitFlipMutation(mutation_rate),
	TweakByValueMutation(mutation_rate, 0.2),
	TweakByPercentageMutation(mutation_rate, 25.0)]

def generatePopulation():
	for i in range(0, pop_size):
		chromosome = []
		for j in range(0, chromosome_length):
			if random.random() > 0.5:
				chromosome.append(1.0)
			else:
				chromosome.append(0.0)

		ga.addMember(Member(chromosome, 0.0))

def setFitness():
	for i, m in enumerate(ga.getPopulation()):
		f = sum(m.getChromosome())
		if f <= 0:
			f = 0.0000000001
		ga.setMemberFitness(i, f)

def checkStop():
	for m in ga.getPopulation():
		if sum(m.getChromosome()) == chromosome_length:
			return True
	return False		

def run():
	if doConsoleOutput:
		print("run " + str(run_inst) + " started")
	if doLogFileOutput:
		logFile.write("run " + str(run_inst) + " started\n")

	if doRunFileOutput:
		# Create file
		runFile = open(".\\outputs\\run_" + str(run_inst) + ".csv", "w")

	# Headers
	if doRunFileOutput:
		runFile.write("generation, member_index, ")
		for i in range(0, chromosome_length):
			runFile.write("c" + str(i) + ", ")
		runFile.write("fitness\n")

	# Run
	done = False
	gen = 0
	while(not done and gen < max_gens):
		if doConsoleOutput:
			print(gen)
			print(len(ga.getPopulation()))
		if doRunFileOutput:
			for i, m in enumerate(ga.getPopulation()):
				runFile.write(str(gen) + ", " + str(i) + ", ")
				for i in range(0, chromosome_length):
					runFile.write(str(m.getChromosome()[i]) + ", ")
				runFile.write(str(sum(m.getChromosome())) + "\n")
		setFitness()
		ga.execute()
		done = checkStop()	
		gen += 1

	if doConsoleOutput:
		print("run " + str(run_inst) + " ended generation " + str(gen))	
		print("===============")
	if doLogFileOutput:
		logFile.write("run " + str(run_inst) + " ended generation " + str(gen) + "\n")
		logFile.write("===============\n")
	
	if doRunFileOutput:
		# Close file
		runFile.close()

# LOOP ALL COMBOS
"""for si in range(selStart,len(selection_methods)):
	for ci in range(crossStart,len(crossover_methods)):
		for ri in range(repStart,len(replacement_methods)):
			for mi in range(mutStart,len(mutation_methods)):
				ga = GeneticAlgorithm(selection_methods[si], crossover_methods[ci], replacement_methods[ri], mutation_methods[mi])
				ga.clearPopulation()
				generatePopulation()
				run()
				run_inst += 1
			mutStart = 0
		repStart = 0
	crossStart = 0
selStart = 0
mainfile.close()"""

# LOOP CROSSOVER METHODS
for ci in range(crossStart,len(crossover_methods)):
	ga = GeneticAlgorithm(selection_methods[3], crossover_methods[ci], replacement_methods[2], mutation_methods[2])
	generatePopulation()
	run()
	run_inst += 1

# SINGLE RUN
"""ga = GeneticAlgorithm(selection_methods[3], crossover_methods[0], replacement_methods[2], mutation_methods[2])
generatePopulation()
run()"""

if doLogFileOutput:
	logFile.close()