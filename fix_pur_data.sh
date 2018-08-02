files = '/Users/nataliemall/Box Sync/herman_research_box/tulare_git_repo/pur_pre_1990/pur1990/udc90_54.txt'
for file in files:
	new = open(file).read().replace('?','0')
	open(file + '_fixed', 'w').write(new)

	