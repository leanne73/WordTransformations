#!/usr/bin/python
'''
Created on 8/5/15
An implementation of the Damerau-Levenshtein Distance Algorithm.

arg[0] = source word, arg[1] = target word

@author: Leanne Miller
'''

import sys
import operator

# The cost associated with each operation. Order: insert, substitute, delete, flip/transpose, no-op.
costs = [2, 3, 2, 3, 0]
	
def init_matricies():
	'''Initialize bottom row and left column of distance and action matrices.'''
	
	# Cost to reach target string using only insertions
	for t in range(len(target) + 1) :
		distances[t][0] = costs[0] * t
		actions[t][0] = 0 
		
	# Cost to reach target string using only deletions
	for s in range(len(source) + 1) :
		distances[0][s] = costs[2] * s
		actions[0][s] = 2
	

def compute_matricies():
	'''Compute contents of the distance and action matricies.'''
	init_matricies()
	
	for t in range(1, len(target) + 1) :
		for s in range(1, len(source) + 1) :
			transformations = [0, 0, 0, 0, 0]
			transformations[0] = distances[t-1][s] + costs[0] # insert
			transformations[1] = distances[t-1][s-1] + costs[1] # substitute
			transformations[2] = distances[t][s-1] + costs[2] # delete
			if (t > 1 and s > 1 and target[t-1]==source[s-2] and target[t-2]==source[s-1]):
				transformations[3] = distances[t-2][s-2] + costs[3] # flip
			else:
				transformations[3] = sys.maxint
			if (target[t-1]==source[s-1]):
				transformations[4] = distances[t-1][s-1] + costs[4] # no-op
			else:
				transformations[4] = sys.maxint

			distances[t][s] = min(transformations)
			actions[t][s] = transformations.index(distances[t][s])
			

def reconstruct_edits():
        '''Reconstruct the sequence of edits. 
        Returns a list of actions performed and a list of the stages of the word's transformation.'''
   
	t = len(target)
	s = len(source)
	actions_performed = []
	stages = [target]  # list containing the intermediate forms of the word, with target at the end
	current = target
	
	while t > 0 : 
		# derive the previous form based on what action happened and make it the current form 
		a = actions[t][s]
		if a == 0 :
			action = 'Insertion'
			current = current[0:t-1] + current[t:]
			t = t-1
		elif a == 1 :
			action = 'Substitution'
			current = current[0:t-1] + source[s-1] + current[t:]
			t = t-1
			s = s-1
		elif a == 2 :
			action = 'Deletion'
			current = current[0:t] + source[s-1] + current[t:]
			s = s-1
		elif a == 3 :
			action = 'Transposition'
			current = current[0:t-2] + current[t-1] + current[t-2] + current[t:]        
			t = t-2
			s = s-2	
		elif a == 4:
			action = 'No-op'
			t = t-1
			s = s-1
		else:
			print "Error: Unexpected Action"
			print "Action was:", a
			print 'Actions:'
			print_matrix(actions)
			print "Distances:"
			print_matrix(distances)
			sys.exit()
		
		# add the new wordform to our list, ignore no-ops
                if not a == 4:
                        stages.insert(0, current)
                        actions_performed.insert(0, action)

	# Any characters left in source must be deletions
	while s > 0:
		current = current[0:t] + source[s-1] + current[t:]
		s = s-1
		stages.insert(0, current)
		actions_performed.insert(0, "Deletion")
	   
	return actions_performed, stages

def normalize():
        '''Determine how efficient the transformation was, how "close" the two words are. 
        Range: [0, 1]. Smaller numbers signify higher similarity between the words. 
        0 indicates identical words, 1 indicates words with nothing in common.'''

	max_score = max(costs) * max([len(source), len(target)])
	actual = distances[len(target)][len(source)]
	print 'Max Possible Score:', max_score
	print 'Actual Score:', actual
	print 'Normalization:', float(actual)/max_score, "\n" 
			
def print_matrix(m):
	m = m[::-1]
	for row in m:
		print row
	
def print_distance():
	print "\nEdit Distance Score is: %i" % distances[len(target)][len(source)]

def print_stages(stages):
	print "\nTransformations:"
	for version in stages:
		print version	

def print_actions(actions):
	print "\nActions Performed:"
	for a in actions:
		print a
	print ""
	
# read args
source = sys.argv[1]
target = sys.argv[2]

# Distance matrix. Stores the min cost of reaching a given target substring from a given source substring.
distances = [[0 for s in range(len(source) + 1)] for t in range(len(target) + 1)]

# Action matrix. Stores the action taken to achieve the minimum cost. Actions are represented by their index in the costs array.
actions = [[-1 for s in range(len(source) + 1)] for t in range(len(target) + 1)]

compute_matricies()
	
print_distance()
actions_performed, stages = reconstruct_edits()
print_stages(stages)
print_actions(actions_performed)
normalize()


