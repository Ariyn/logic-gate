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
	def __init__(self, name, input, output, mode = SLOWMODE):
		self.name, self.mode = name, mode
		self.inputNumber, self.outputNumber = input, output
		self.output = None

		self.inputTable = [None] * input
		self.truthTable = []
		self.children = []

	def __str__(self):
		return "%d input %s gate" % (self.inputNumber, self.name.upper())

	def setTruthTable(self, *krag):
		if len(krag) != self.inputNumber+1:
			raise TruthTableMissingElement

		self.truthTable.append(tuple(krag))

	def connectOutput(self, gate, address):
		if gate.inputNumber <= address:
			raise WrongInputAddress
		self.children.append(
			(gate, address)
		)

	def addInput(self, address, input):
		self.inputTable[address] = input

		if self.mode == SLOWMODE:
			self.gates["input"][address].addInput(0, input)

			self.checkOutput()

	def checkOutput(self):
		retVal = None

		if None in self.inputTable:
			return NotEnoughInput

		if self.mode == HYPERMODE:
			correctData = self.truthTable
			for i in range(0, self.inputNumber):
				correctData = [x for x in correctData if x[i] == self.inputTable[i]]

			retVal = None
			if correctData != []:
				retVal = correctData[0][self.inputNumber]
				for i in self.children:
					i[0].addInput(i[1], retVal)
		
			self.output = retVal
			return retVal

		elif self.mode == SLOWMODE:
			retVal = self.gates["output"][address].output

		return retVal

if __name__ == "__main__":
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

	print(andGate.truthTable)