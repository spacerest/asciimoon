def stretch(list_to_stretch, length):
	return list_to_stretch + ([list_to_stretch[-1]] * (length - len(list_to_stretch)))
    #return [list_to_stretch[i * len(list_to_stretch) // length] for i in range(length)]