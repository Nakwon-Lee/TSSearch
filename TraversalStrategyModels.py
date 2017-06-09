
class TraversalStrategy:

	def __init__(self,patos):
		self.atos = patos
		self.toroot = None

	def randomOdrGen(self):
		

	def validation(self): #validating made traversal strategy
		#TODO check whether all items in FiniteDomain are considred or not (child is not mandatory but it is divided for each domain item)
		#Same labfuncs in a path is not allowed
		pass

class AtomicTotalOrder:

	def __init__(self,pname,podr):
		self.name = pname
		self.odr = podr

class FiniteDomainTotalOrder(AtomicTotalOrder):

	def __init__(self,pname,podr,pdomain):
		super().__init__(pname,podr)
		self.domain = pdomain #domain is a tuple

class TtOdrNode:

	def __init__(self,pato):
		self.ato = pato
		self.children = []
