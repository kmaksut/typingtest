def is_space(item, show_index: bool = False):
    index = 0
    for i in item:
        if i == " ":
            index +=1
    
    if show_index == True:
        if index >= 1:
            return {"isSpace":True,"index":index}
        else:
            return {"isSpace":False,"index":index}
    
    if index >= 1:
        return True
    else:
        return False