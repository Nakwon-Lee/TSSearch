from __future__ import absolute_import, division, print_function, unicode_literals

import glob
import os
import sys
from xml.etree.ElementTree import Element, SubElement, dump

sys.dont_write_bytecode = True # prevent creation of .pyc files
for egg in glob.glob(os.path.join(os.path.dirname(__file__), os.pardir, 'lib', 'python-benchmark', '*.egg')):
    sys.path.insert(0, egg)

import benchexec.runexecutor
from TraversalStrategyModels import *

def other_after_run(outlog,var):

	print('filename: ',outlog)

	f = open(outlog,"r")
	lines = f.readlines()
	f.close()

	dic = {}

	# loop for extracting other metrics

	for line in lines:
		if line.find("Number of affected states:") >= 0:
			tokens = line.split()
			dic[var[0]] = tokens[4]

		if line.find("Visited lines:") >= 0:
			tokens = line.split()
			dic[var[1]] = tokens[len(tokens)-1]
    
		if line.find("Visited conditions:") >= 0:
			tokens = line.split()
			dic[var[2]] = tokens[len(tokens)-1]

	return dic

def comparefitness(old,new):
	
	ret = 0

	#compare fitness of two vals.
	#if vals1 is better, return -1, if vals2 is better, return 1
	#if vals1 and vals2 have same fitness, return 0

	return ret

def makingAtomTotalOrders(labfuncs):

	atos = []

	for labfunc in labfuncs:
		if labfunc[1] == 1: #TtOdr with finite domain
			ato = FiniteDomainTotalOrder(labfunc[0],labfunc[3],labfunc[2])
			atos.append(ato)
		elif labfunc[1] == 0: #TtOdr with infinite domain
			ato = AtomicTotalOrder(labfunc[0],labfunc[2])
			atos.append(ato)
		else:
			print('labfunc should be finite or infinite domain')

	return atos

def ttOdrToXML(pttOdr,pxmlfile):
	ttodrelem = Element('ttOdr')
	xmlDFS(pttOdr.toroot,ttodrelem)
	indent(ttodrelem)
	dump(ttodrelem)

def xmlDFS(curr,elem):
	ato = curr.ato
	subelem = Element(curr.ato.name)
	subelem.attrib['Odr'] = str(curr.ato.odr)
	elem.append(subelem)
	if isinstance(ato,FiniteDomainTotalOrder):
		for i in range(len(curr.children)):
			subelem2 = Element(curr.ato.name + ' switch')
			subelem2.attrib['Domain'] = str(curr.ato.domain[i])
			elem.append(subelem2)
			xmlDFS(curr.children[i],subelem2)
	elif isinstance(ato,AtomicTotalOrder):
		subelem3 = Element(curr.ato.name + ' else')
		elem.append(subelem3)
		if len(curr.children) is not 0:
			xmlDFS(curr.children[0],subelem3)

def indent(elem, level=0):
    i = '\n' + level*'  '
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def ttOdrToJAVA(pttOdr,pJavafile):
	pass

def main():

	print('Traversal Strategy Search Start')

	currts = None
	bestts = None
	currvals = None
	outlog = 'output.log'
	fitvars = ('NoAffS','VL','VC')
	labfuncs = (('IsAbs',1,(0,1),0),('blkD',0,0),('CS',0,0),('CS',0,1),('RPO',0,0),('RPO',0,1),('uID',0,0),('uID',0,1))
	atos = None

	atos = makingAtomTotalOrders(labfuncs)

	#print(atos)

	currts = TraversalStrategy(atos)
	currts.randomOdrGen()

	currts.printTS()

	ttOdrToXML(currts,1)

	while(1):
		#TODO Make a new solution
		# local search
		# make a new search strategy formula (total order)

		#TODO Calculate the fitness of the new solution
		# execution of cpachecker with new total order
		benchexec.runexecutor.main()
		newvals = other_after_run(outlog,fitvars)
		print('ret: ',newvals)
		#fitness = comparefitness(currvals,newvals)

		#TODO If the new solution is better than the best solution, change the solution
		#if fitness is 1: #new one is better than old one
		#	pass
		#else if fitness is 0:
			#TODO update bestts with specific probability
		#	pass

		break

	return bestts

if __name__ == '__main__':
    main()
