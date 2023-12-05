from pygame import locals

liste = dir(locals)

with open('wrintingOff.py', 'w') as f:

	f.write('from pygame import locals\n')
	f.write('\n')
	f.write('dico = dict()\n')
	f.write('\n')

	for key in liste:
		if '__' in key or 'pygame' in key or 'SCRAP_' in key or key in ['Color', 'Rect']:
			f.write("# ")
		f.write(f"dico['{key}'] = locals.{key}\n")


from wrintingOff import dico

revers = {}

with open('wrintingLocals.py', 'w') as f:

	for key, val in dico.items():
		f.write(f"{key:32} = {val}\n")

		if val not in revers.keys():
			revers[val] = []

		revers[val].append(key)

with open('wrintingValues.py', 'w') as f:

	sorted_keys = sorted(revers.keys())

	for key in sorted_keys:
		f.write(f"{str(key):32} = {revers[key]}\n")