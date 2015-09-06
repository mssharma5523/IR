import os
import sys
import math

def map_k(filename='try'):
	avg_precision = []
	with open(filename) as f:
		content = f.read().splitlines()
		print content
	sum=0
	for precision in content:
		if precision != '':
			sum += int(precision)

	if len(content) == 0:
		return 0
	else:
		final_precision = float(sum)/(len(content)-1)
		return final_precision


def avg_k(precision_arr):
	precision_k=[]
	cum_sum=0
	count=0
	for precision in precision_arr:
		cum_sum +=int(precision)
		#cum_precision.append(cum_sum)
		count +=1
		precision_k.append(float(cum_sum)/count)
	precision_sum = 0
	count = 0 
	for precision in precision_k:
		count +=1
		precision_sum += (precision*precision_arr[count-1])
	avg_k = float(precision_sum)/cum_sum
	return avg_k 


def ndcg_k(precision_arr):
	ndcg = int(precision_arr[0])
	temp = []
	temp.append(int(precision_arr[0]))
	#max_ndcg = int(precision_arr[0])
	for x in range(1,len(precision_arr)):
		temp.append(precision_arr[x])
		#print precision_arr[x]
		if int(precision_arr[x]) == 0:
			ndcg += float(precision_arr[x])/(-(sys.maxint-1))
		else:
			ndcg += (float(precision_arr[x])/(math.log(int(precision_arr[x]),2)+0.001))
	temp.sort(reverse=True)
	max_ndcg = int(precision_arr[0])
	for x in range(1,len(temp)):
		if int(temp[x]) == 0:
			max_ndcg += float(temp[x])/(-(sys.maxint-1))
		else:
			max_ndcg += (float(temp[x])/(math.log(int(temp[x]),2)+0.001))
	ndcg = float(ndcg)/max_ndcg
	return ndcg


if __name__ == '__main__':
	print map_k()
	print avg_k([5,5,5,5,5,4,5,5,5,5])
	print ndcg_k([1,0,1,3,4,5,1,1,1,1])