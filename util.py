def apply_seq(function, sequence):
    for item in sequence: 
        function(item)

def str_list_to_int(l):
    new_list = []
    for e in l:
        try:
            e = int(e)
        except:
            continue
        else:
            new_list.append(e)

    return new_list
