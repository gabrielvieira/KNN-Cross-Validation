import csv
import random
import math
import operator

def euclideanDistance(instance1, instance2, length):
	distance = 0
	for x in range(length):
		distance += pow(( float(instance1[x]) - float(instance2[x])), 2)
	return math.sqrt(distance)

def getNeighbors(trainingSet, testInstance, k):
	
	distances = []
	length = len(testInstance)-1

	for x in range(len(trainingSet)):
		dist = euclideanDistance(testInstance, trainingSet[x], length)
		distances.append((trainingSet[x], dist))

	distances.sort(key=operator.itemgetter(1))
	neighbors = []

	for x in range(k):
		neighbors.append(distances[x][0])
	return neighbors

def getAccuracy(testSet, predictions):
	correct = 0
	for x in range(len(testSet)):
		if testSet[x][-1] == predictions[x]:
			correct += 1
	return (correct/float(len(testSet))) * 100.0

def getResponse(neighbors):
	classVotes = {}
	for x in range(len(neighbors)):
		response = neighbors[x][-1]
		if response in classVotes:
			classVotes[response] += 1
		else:
			classVotes[response] = 1
	sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True)
	return sortedVotes[0][0]

#with open('iris.data', 'rt') as csvfile:
csvfile = open('iris/iris.csv', 'rt')
lines = csv.reader(csvfile)
dataset = list(lines)
#dataset = dataset [:-1]

#10 fold cross
rangeSize =  round ( len(dataset) / 10)
#array o accuracy
accuracyArray = []
#confusion matrix with classes

#confusion_matrix = [[]]
#version of algorithm
Q = len(dataset)
P = 3
M = P

w, h = P + 1, P + 1;
confusion_matrix  = [[0 for x in range(w)] for y in range(h)] 

if P%2 == 0:
	M = P + 1

#v1
#algorithm_prefix = 'v1'
#k = 1

#v2
#algorithm_prefix = 'v2'
#k = M + 2

#v3
#algorithm_prefix = 'v3'
#k = (M * 10) + 1

#v4
'''
algorithm_prefix = 'v4'

div = int(Q/2)

if div%2 == 0:
	k = div + 1
else:
	k = div

print (k)
'''

for x in range(10):

	#x = 9
	#define range
	leftRange = x * rangeSize
	rightRange = leftRange + rangeSize
	#define data sets
	testSet = dataset[leftRange : rightRange]
	trainingSet = dataset[:]
	del trainingSet[leftRange : rightRange]

	predictions=[]


	for y in range(len(testSet)):

		neighbors = getNeighbors(trainingSet, testSet[y], k)
		result = getResponse(neighbors)
		predictions.append(result)
		confusion_matrix[int(testSet[y][-1]) + 1][int(result) + 1] += 1

	accuracy = getAccuracy(testSet, predictions)
	accuracyArray.append(accuracy)
	print('Accuracy: ' + repr(accuracy) + '%')

print (confusion_matrix)
print( sum(accuracyArray) / float(len(accuracyArray)) )


classes = ['Iris-setosa' , 'Iris-versicolor' , 'Iris-virginica']
for z in range(len(classes)):
	confusion_matrix[0][z + 1] = classes[z]
	confusion_matrix[z + 1][0] = classes[z]

fl = open('iris/' + algorithm_prefix + '_confusion_matrix.csv', 'w')

writer = csv.writer(fl)
#writer.writerow(['label1', 'label2', 'label3']) #if needed
for values in confusion_matrix:
    writer.writerow(values)

fl.close()    


fl = open('iris/' + algorithm_prefix + '_error_round.csv', 'w')

writer = csv.writer(fl)
#writer.writerow(['label1', 'label2', 'label3']) #if needed
writer.writerow(accuracyArray)

fl.close()    


