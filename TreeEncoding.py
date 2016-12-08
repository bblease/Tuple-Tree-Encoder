'''

Created by Ben Blease

8/22/15

Encode and decode binary trees in list format.

Encoded to base 16 with extra bit indicating children for a node.

'''


def convert(integer, factor):
	'''converts integer to base factor'''
	num = integer
	out = ''
	while(1):
		if num == 0:
			break
		out = hex(num % factor)[-1] + out
		num = num/factor
	return out

def revert(string, factor):
	'''reverts string to base factor'''
	inp = string
	out = 0
	counter = 0
	for i in inp[::-1]:
		out += int(i, 16)*(factor**counter)
		counter += 1
	return out

#encoder/decoder

def encode_top(tup):
	output = []
	output += [convert(tup[0], 2) + '1']
	encode(tup, output)
	return output

def encode(tup, out):
	'''tree (tup) is in format (node, (leaf), (node, (leaf), (leaf)))'''
	for i in range(len(tup)):
		if type(tup[i]) is tuple:
			out += [convert(tup[i][0], 2) + '1']
			encode(tup[i], out)
		if type(tup[i]) is not tuple and i != 0:
			out += [convert(tup[i], 2) + '0']


def decode_top(out, lst):
	for j in range(len(lst)):
		if j != 0:
			if '0' in lst[j]:
				del lst[j][lst[j].index('0')]
				pass
			if '1' in lst[j]:
				del lst[j][lst[j].index('1')]
				for k in out[1:3]:
					if k[0] == lst[j][0]:
						lst[j] = k
						del out[out.index(k)]
						break
	for g in lst:
		if type(g) is list:
			if len(g) == 3:
				decode_top(out, lst[lst.index(g)])


	return out

def decode(lst):
	out = []
	lst += [[], [], [], []]
	for i in range(len(lst)-4):
		if lst[i][-1] == '1':
			if lst[i+1][-1] == '1':
				out += [[revert(lst[i][:-1], 2), [revert(lst[i+1][:-1],2), lst[i+1][-1]], [revert(lst[i+4][:-1], 2), lst[i+4][-1]]]]
			else:
				out += [[revert(lst[i][:-1], 2), [revert(lst[i+1][:-1], 2), lst[i+1][-1]], [revert(lst[i+2][:-1], 2), lst[i+2][-1]]]]
	return out



def add(lst):
	counter = 0
	for i in lst:
		counter += len(i)
	return counter

if __name__ == '__main__':
	#an example tree
	tree1 = (5,
				(3,
					(897),
					(3785)),
				(2,
					(2,
						(15),
						(15)
					),
					(2,
						(985,
							(1823575),
							(4535846)),
						(985,
							(4542342),
							(4768923))
					)
				)
			)


	#run encoding
	encoded_input = encode_top(tree1)
	encoded_output = map(lambda x: convert(revert(x, 2), 16), encoded_input)
	matched_el = decode(encoded_input)
	decoded = decode_top(matched_el, matched_el[0])
	print 'ORIGINAL:', tree1
	print 'ENCODED:', encoded_output
	print 'DECODED:', decoded
