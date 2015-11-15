import itertools
from copy import copy, deepcopy
from gates import *

class AlreadySameGateName:
	pass

class IC(Gate):
	def __init__(self, name, input, output, mode = SLOWMODE):
		super().__init__(name, input, output)

		self.mode = mode

		self.gates = {}

		g = Gate("input", input, input)
		for i in range(0, pow(2, input)):
			binList = [int(x) for x in format(i, "0%db" % input)]*2

			g.setTruthTable(*binList)

		self.addGate(g, "input")

		g = Gate("output", output, output)
		for i in range(0, pow(2, output)):
			binList = [int(x) for x in format(i, "0%db" % output)]*2
			g.setTruthTable(*binList)

		self.addGate(g, "output")

		self.connections = {}

	def addGate(self, gate, name):
		if name not in self.gates:
			# self.gates[name] = []

			self.gates[name] = deepcopy(gate)
		else:
			raise AlreadySameGateName

	def addInput(self, address, input):
		self.inputTable[address] = input

		if self.mode == SLOWMODE:
			self.gates["input"].addInput(address, input)

			# self.checkOutput()

	def connectGate(self, *krag):
		# [(gate1, g1OutputAddr, gate2, g2InputAddr), ...]
		for i in krag:
			if type(i[0]) != str and type(i[2]) != str or type(i[1]) != int or type(i[3]) != int:
				raise WrongInput

			if i[0] not in self.gates or i[2] not in self.gates:
				print(i[0], i[2], self.gates)
				raise WrongInput

			g1 = self.gates[i[0]][i[1]]
			for g2 in self.gates[i[2]]:
				g1.connectOutput(g2, i[3])

		# if self.mode == HYPERMODE:
		# 	self.createTruthMap()
	
	def newConnectGate(self, *krag):
		# [(gate1, g1OutputAddr, gate2, g2InputAddr), ...]
		for i in krag:
			oGate, oGateAddr = i[0], i[1]
			dGate, dGateAddr = i[2], i[3]

			if type(oGate) != str and type(dGate) != str or type(oGateAddr) != int or type(dGateAddr) != int:
				raise WrongInput

			if oGate not in self.gates or dGate not in self.gates:
				print(oGate, dGate, self.gates)
				raise WrongInput

			if oGate not in self.connections:
				self.connections[oGate] = {}

			if dGate not in self.connections[oGate]:
				self.connections[oGate][dGate] = []

			self.connections[oGate][dGate].append((oGateAddr, dGateAddr))

	def calculateOutput(self, oGateName="input"):
		print(self.connections)

		for dGateName in self.connections[oGateName]:
			for e in self.connections[oGateName][dGateName]:
				oGateAddr, dGateAddr = e[0], e[1]
				print(oGateName, oGateAddr, dGateName, dGateAddr)

				# set each gate input here
				# and check output
				# and make recursion this function to next gate

				# oGate = self.gates[oGateName].checkOutput(oGateAddr)
				# dGate = self.gates[dGateName][dGateAddr]

				# print(dGate)


if __name__ == "__main__":
	norGate = IC("nor", 2, 1, SLOWMODE)
	norGate.addGate(orGate, "or1")
	norGate.addGate(notGate, "not1")

	norGate.newConnectGate(
		("input", 0, "or1", 0),
		("input", 1, "or1", 1),
		("or1", 0, "not1", 0),
		("not1", 0, "output", 0)
	)
	# print(norGate.truthTable)

	norGate.addInput(0,1)
	norGate.addInput(1,1)
	norGate.calculateOutput()
	# print(d)