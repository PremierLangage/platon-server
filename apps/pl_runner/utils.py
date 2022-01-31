
def extends_dict(target, source):
    """ Will copy every key and value of source in target if key is not present in target """
    for key, value in source.items():
        if key not in target:
            target[key] = value
        elif type(target[key]) is dict:
            extends_dict(target[key], value)
        elif type(target[key]) is list:
            target[key] += value
    
    return target