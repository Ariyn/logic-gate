import itertools
from copy import copy, deepcopy

class TruthTableMissingElement:
	pass

class WrongInputAddress:
	pass

class NotEnoughInput:
	pass
class WrongInput:
	pass

SLOWMODE, HYPERMODE = 0, 1

class Gate:
	def __init__(self, name, input, output):

		self.name = name
		self.inputNumber, self.outputNumber = input, output
		
		self.outputTable = [None] * output
		self.inputTable = [None] * input
		self.truthTable = []
		self.children = []

	def __str__(self):
		return "%d input %s gate" % (self.inputNumber, self.name.upper())

	def setTruthTable(self, *krag):
		if len(krag) != self.inputNumber+self.outputNumber:
			raise TruthTableMissingElement

		self.truthTable.append(tuple(krag))

	def addInput(self, address, input):
		self.inputTable[address] = input
		self.checkOutput()

	def checkOutput(self, output = 0):
		retVal = None

		if None in self.inputTable:
			return NotEnoughInput

		correctData = self.truthTable
		for i in range(0, self.inputNumber):
			correctData = [x for x in correctData if x[i] == self.inputTable[i]]

		retVal = None
		if correctData != []:
			retVal = correctData[0][:-self.outputNumber]
			self.output = retVal

andGate, orGate, notGate = Gate("and", 2, 1), Gate("or", 2, 1), Gate("not", 1, 1)

andGate.setTruthTable(0,0,0)
andGate.setTruthTable(0,1,0)
andGate.setTruthTable(1,0,0)
andGate.setTruthTable(1,1,1)

orGate.setTruthTable(0,0,0)
orGate.setTruthTable(0,1,1)
orGate.setTruthTable(1,0,1)
orGate.setTruthTable(1,1,1)

notGate.setTruthTable(0,1)
notGate.setTruthTable(1,0)

if __name__ == "__main__":
	or2Gate = Gate("2 way or", 2, 2)

	or2Gate.setTruthTable(0,0, 0, 1)
	or2Gate.setTruthTable(0,1, 1, 0)
	or2Gate.setTruthTable(1,0, 1, 0)
	or2Gate.setTruthTable(1,1, 1, 0)

	or2Gate.addInput(0, 0)
	or2Gate.addInput(1, 1)

	print(or2Gate.output[1])

	# print(format(8, "08b"))
	g = Gate("input", 3, 3)
	
	input = 3
	for i in range(0, pow(2, input)):
		binList = [int(x) for x in format(i, "0%db" % input)]*2
		print(binList)

		g.setTruthTable(*binList)

		
