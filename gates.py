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
	def __init__(self, name, input):
		self.name = name
		self.input, self.output = input, None

		self.inputTable = [None] * input
		self.truthTable = []
		self.children = []

	def __str__(self):
		return "%d input %s gate" % (self.input, self.name.upper())

	def setTruthTable(self, *krag):
		if len(krag) != self.input+1:
			raise TruthTableMissingElement

		self.truthTable.append(tuple(krag))

	def connectOutput(self, gate, address):
		if gate.input <= address:
			raise WrongInputAddress
		self.children.append(
			(gate, address)
		)

	def addInput(self, address, input):
		self.inputTable[address] = input

		self.checkOutput()

	def checkOutput(self):
		if None in self.inputTable:
			return NotEnoughInput

		correctData = self.truthTable
		for i in range(0, self.input):
			correctData = [x for x in correctData if x[i] == self.inputTable[i]]

		retVal = None
		if correctData != []:
			retVal = correctData[0][self.input]
			for i in self.children:
				i[0].addInput(i[1], retVal)
		
		self.output = retVal
		return retVal

	# def activeGate(self, *krag):
	# 	if len(krag) != self.input:
	# 		raise NotEnoughInput

	# 	correctData = self.truthTable
	# 	for i in range(0, self.input):
	# 		correctData = [x for x in correctData if x[i] == krag[i]]

	# 	return correctData[0][self.input]

class IC(Gate):
	def __init__(self, name, input, output, mode = SLOWMODE):
		super().__init__(name, input, output, mode)

		self.gates = {"input":[], "output":[]}

		for i in range(0, input):
			g = Gate("input %d"%i, 1)
			g.setTruthTable(0,0)
			g.setTruthTable(1,1)

			self.gates["input"].append(g)

		for i in range(0, output):
			g = Gate("output %d"%i, 1)
			g.setTruthTable(0,0)
			g.setTruthTable(1,1)

			self.gates["output"].append(g)

	def addGate(self, gate, name):
		if name not in self.gates:
			self.gates[name] = []

		self.gates[name].append(deepcopy(gate))

	def connectGate(self, *krag):
		# [(gate1, g1Addr, gate2, g2Addr), ...]
		# if gate1 is "input"
		#	connect gate2 to main input address
		# else if gate1 is "output"
		# 	connect gate2 to main output address

		for i in krag:
			if type(i[0]) != str and type(i[2]) != str or type(i[1]) != int or type(i[3]) != int:
				raise WrongInput

			if i[0] not in self.gates or i[2] not in self.gates:
				raise WrongInput

			g1 = self.gates[i[0]][i[1]]
			for g2 in self.gates[i[2]]:
				g1.connectOutput(g2, i[3])

		if self.mode == HYPERMODE:
			self.createTruthMap()

	def checkOutput(self, address=0):
		retVal = None

		if self.mode == HYPERMODE:
			correctData = self.truthTable
			for i in range(0, self.inputNumber):
				correctData = [x for x in correctData if x[i] == self.inputTable[i]]

			if correctData != []:
				retVal = correctData[0][self.inputNumber]
				for i in self.children:
					i[0].addInput(i[1], retVal)
			
			# self.output = retVal
			return retVal

		elif self.mode == SLOWMODE:
			retVal = self.gates["output"][address].output

		return retVal


	def createTruthMap(self):
		product = itertools.product((0,1), repeat=self.inputNumber)

		backup, self.mode = self.mode, SLOWMODE

		for i in product:
			for e in range(0, self.inputNumber):
				self.addInput(e,i[e])

			self.setTruthTable(i[0],i[1],self.checkOutput())

		self.mode = backup


if __name__ == "__main__":
	andGate, orGate, notGate = Gate("and", 2), Gate("or", 2), Gate("not", 1)

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


	norGate = IC("nor", 2, 1, HYPERMODE)
	norGate.addGate(andGate, "and1")
	norGate.addGate(notGate, "not1")

	norGate.connectGate(
		# (norGate.input0, norGate.k1, 0),
		# (norGate.input1, norGate.k1, 1),
		("input", 0, "and1", 0),
		("input", 1, "and1", 1),
		("and1", 0, "not1", 0),
		("not1", 0, "output", 0)
	)
	print(norGate.truthTable)

	norGate.addInput(0,0)
	norGate.addInput(1,0)
	d = norGate.checkOutput(0)
	print(d)

	nandGate = IC("nand", 2, 1, HYPERMODE)
	nandGate.addGate(andGate, "and")
	nandGate.addGate(notGate, "not")

	nandGate.connectGate(
		("input", 0, "and", 0),
		("input", 1, "and", 1),
		("and", 0, "not", 0),
		("not", 0, "output", 0)
	)
	print(nandGate.truthTable)