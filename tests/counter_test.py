from collections import Counter

dc = {}
dc['abc@gmail.com'] = Counter()

def dict_to_count():
	if 'abc@gmail' not in dc:
		dc['abc@gmail.com'] = Counter()

	for word in ['red', 'blue', 'red', 'green', 'blue', 'blue']:
		dc['abc@gmail.com'][word] += 1

	print dc['abc@gmail.com']

	if 'def@gmail' not in dc:
		dc['def@gmail.com'] = Counter()

	for word in ['red', 'blue', 'red', 'green', 'blue', 'blue']:
		dc['def@gmail.com'][word] += 1

	return dc

print dict_to_count()
