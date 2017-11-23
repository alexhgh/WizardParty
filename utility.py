import sys
import operator
import random

def preprocess(wizards, num_constraints, constraints):
	mapped_constraint = wizardsmap(wizards,constraints)
	return remove_duplicate(num_constraints, mapped_constraint)

def wizardsmap(wizards, constraints):
    node_map = {k: v for v, k in enumerate(wizards)}
    mapped_constraint = []
    for constraint in constraints:
        wiz_a = constraint[0]
        wiz_b = constraint[1]
        wiz_c = constraint[2]

        mapped_constraint += [[node_map[wiz_a],node_map[wiz_b],node_map[wiz_c]]]

    return mapped_constraint

def remove_duplicate(num_constraints, constraints):
    pairs = {}
    for constraint in constraints:
        wiz = [constraint[0],constraint[1]]
        s = frozenset(wiz)

        if len(s) == 1:
            continue
        
        if s in pairs:
            w = constraint[2]
            if w not in pairs[s]:
                pairs[s] += [w] 
                pairs[s] = sorted(pairs[s])
        else:
            pairs[s] = [constraint[2]]

    processed = []
    for p in pairs:
        for c in pairs[p]:
            l = list(p)
            processed += [[l[0],l[1],c]]

    processed = sorted(processed,key=operator.itemgetter(0))
    print("We have removed " + str(num_constraints - len(processed)) + " duplicated constraints.")
    return processed

def valid(order, constraints):

    node_map = {k: v for v, k in enumerate(order)}
    for constraint in constraints:
        wiz_a = constraint[0]
        wiz_b = constraint[1]
        wiz_c = constraint[2]

        if (wiz_a in node_map) and (wiz_b in node_map) and (wiz_c in node_map):
             wiz_a = node_map[wiz_a]
             wiz_b = node_map[wiz_b]
             wiz_c = node_map[wiz_c]

             if (wiz_a < wiz_c < wiz_b) or (wiz_b < wiz_c < wiz_a):
                return False

    return True

def possible(order,constraint):

    wiz_a = constraint[0]
    wiz_b = constraint[1]
    wiz_c = constraint[2]

    if wiz_a in order and wiz_b in order and wiz_c in order:
        index1 = order.index(wiz_a)
        index2 = order.index(wiz_b)
        index3 = order.index(wiz_c)
        if(index1<index3<index2 and index2<index3<index1):
            return [-2]
        else:
            return [-1]
    elif wiz_a in order:
        if wiz_c in order:
            return updated_possible2(order,constraint,wiz_a,wiz_c)
        elif wiz_b in order:
            return updated_possible2(order,constraint,wiz_a,wiz_b)
        else:
            return possible1(order,constraint,wiz_a)
    elif wiz_b in order:
        if wiz_c in order:
            return updated_possible2(order,constraint,wiz_b,wiz_c)
        else:
            return possible1(order,constraint,wiz_b)
    elif wiz_c in order:
        return possible1(order,constraint,wiz_c)
    else:
        print("NOT SUPPOSE TO BE NONRELATED")
        return [] 

# Given an order, there's one matching wizards in the constraint. 
def possible1(order,constraint,wiz):

    collect = []

    wiz_a = constraint[0]
    wiz_b = constraint[1]
    wiz_c = constraint[2]

    index = order.index(wiz)

    if wiz == wiz_a or wiz == wiz_b:

        otherwiz = wiz_b if (wiz == wiz_a) else wiz_a

        for i in range(index+1,len(order)+1):
            order1 = order[:]
            order1.insert(i,otherwiz)
            for j in range(0,index+1):
                order2 = order1[:]
                order2.insert(j,wiz_c)
                collect += [order2]
            for j in range(i+1,len(order1)+1):
                order2 = order1[:]
                order2.insert(j,wiz_c)
                collect += [order2]

        for i in range(0,index+1):
            order1 = order[:]
            order1.insert(i,otherwiz)
            for j in range(0,i+1):
                order2 = order1[:]
                order2.insert(j,wiz_c)
                collect += [order2]

            new_index = order1.index(wiz)
            for j in range(new_index+1,len(order1)+1):
                order2 = order1[:]
                order2.insert(j,wiz_c)
                collect += [order2]

    elif wiz == wiz_c:
        
        for i in range(0,index+1):
            order1 = order[:]
            order1.insert(i,wiz_a)
            for j in range(0,index+2):
                order2 = order1[:]
                order2.insert(j,wiz_b)

                collect += [order2]

        for i in range(index+1,len(order)+1):
            order1 = order[:]
            order1.insert(i,wiz_a)
            for j in range(index+1,len(order1)+1):
                order2 = order1[:]
                order2.insert(j,wiz_b)

                collect += [order2]
            
    else:
        print("SOMETHING WENT WRONG")


    return collect

# Given an order, there are two matchings in the constraint
def updated_possible2(order,constraint,wiz1,wiz2):

    collect = []
    wiz_a = constraint[0]
    wiz_b = constraint[1]
    wiz_c = constraint[2]

    index1 = order.index(wiz1)
    index2 = order.index(wiz2)

    if (wiz2 != wiz_c):

        assert(wiz2 == wiz_b)
        lower = min(index1,index2)
        upper = max(index1,index2)
        for i in range(0,lower+1):
            order1 = order[:]
            order1.insert(i,wiz_c)
            collect += [order1]

        for i in range(upper+1,len(order)+1):
            order1 = order[:]
            order1.insert(i,wiz_c)
            collect += [order1]
    else:

        otherwiz = wiz_b if wiz1 == wiz_a else wiz_a

        if index2 > index1:
            for i in range(0,index2+1):
                order1 = order[:]
                order1.insert(i,otherwiz)
                collect += [order1]
        else:
            for i in range(index2+1,len(order)+1):
                order1 = order[:]
                order1.insert(i,otherwiz)
                collect += [order1]

    return collect


def strategy1(num_wizards,wizards,constraints):

    possible_order = []
    #remain_constraints = sort_freq(constraints[:])
    remain_constraints = constraints[:]

    counter = 1000

    while(len(remain_constraints) > 0 and counter > 0):

        if num_wizards <= 0:
            break

        collect = variation(remain_constraints[0])
        remain_constraints = remain_constraints[1:]

        while(len(collect[0]) < num_wizards and len(remain_constraints) > 0 and counter > 0):

            new_collect = []
            candidate = find_related(collect[0],remain_constraints)
            # No more related constraints
            if (candidate == []):
                print("No more related constraints! Disjoint Set.")
                print("Number of remain:",len(remain_constraints))
                print(collect[0])
                break

            related = True
            pos = []
            for order in collect:
                pos = possible(order,candidate[0])
                #Invalid order, do not build on 
                if (pos == [-2]):
                    continue
                elif (pos == [-1]):
                    new_collect = collect
                elif (pos != []):
                    for p in pos:
                        if(valid(p,remain_constraints)):
                            new_collect += [p]
                else:
                    related = False
                    print("?")

            if (related):
                del remain_constraints[candidate[1]]

            if (new_collect == []):
                print("Wrong direction")
                return collect[0]
            elif (len(new_collect) > 10000):
                new_collect = new_collect[::2]

            random.shuffle(new_collect)
            collect = new_collect
            counter -= 1
            # s = "\r" + str(len(remain_constraints)) + " " + str(len(collect)) + " " + str(counter)
            # sys.stdout.write(s)
            # sys.stdout.flush()

        counter -= 1
        possible_order += [collect[0]]
        num_wizards -= len(collect[0])

    return sum(possible_order,[])

def find_related(order,constraints):

    candidate = []

    for i in range(len(constraints)):
        matches = 0

        for o in order:
            if o in constraints[i]:
                matches += 1

            if matches == 3:
                return [constraints[i],i,3]

        if matches == 0:
            continue
        else:
            candidate += [[constraints[i],i,matches]]

    if candidate == []:
        return []
    return sorted(candidate,key=operator.itemgetter(2),reverse=True)[0]
    
def sort_freq(constraints):
    freq = {}
    for constraint in constraints:
        frozen_constraint = frozenset(constraint)
        wiz_a = constraint[0]
        wiz_b = constraint[1]
        wiz_c = constraint[2]
        freq[frozen_constraint] = 0
        for compare in constraints:
            if compare != constraint:
                sim = 0
                for i in range(0,3):
                    var = compare[i]
                    if var == wiz_a or var == wiz_b or var == wiz_c:
                        sim += 1
                if sim >= 2:
                    freq[frozen_constraint] += 1
                    
    ready = sorted(freq.keys(), reverse=True)
    
    
    
    
    print(ready)
    sol = []
    for key in ready.keys():
        
        sol.append(key)
    return sol

def variation(constraint):

    wiz_a = constraint[0]
    wiz_b = constraint[1]
    wiz_c = constraint[2]

    return [constraint,[wiz_b,wiz_a,wiz_c],[wiz_c,wiz_a,wiz_b],[wiz_c,wiz_b,wiz_a]]

def find_optimizable(constraints):

    pairs = {}
    order = []
    name = []

    for constraint in constraints:
        s = frozenset(constraint)

        if s in pairs:
            c = pairs[s]
            wiz_a = c[2]
            wiz_c = constraint[2]
            wiz_b = c[0] if c[0] != wiz_c else c[1]

            if wiz_a not in name:
                name += [wiz_a]
            if wiz_b not in name:
                name += [wiz_b]
            if wiz_c not in name:
                name += [wiz_c]

            order += [[wiz_a,wiz_b,wiz_c],[wiz_c,wiz_b,wiz_a]]
        else:
            pairs[s] = constraint

    return sorted(order,key=operator.itemgetter(0)), name

def optimization1(wizards, limited_constraints):

    return












