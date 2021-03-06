import sys
import operator

def brute_force(num_wizards, num_constraints, wizards, constraints):

    node_map = {k: v for v, k in enumerate(wizards)}
    tryout = [node_map]
    status = True
    counter = 0
    dup = 0

    while(status):
        status = False
        counter += 1

        for i in range(num_constraints):
            
            constraint = constraints[i]

            wiz_a = node_map[constraint[0]]
            wiz_b = node_map[constraint[1]]
            wiz_mid = node_map[constraint[2]]

            if (wiz_a < wiz_mid < wiz_b) or (wiz_b < wiz_mid < wiz_a):
                new_node = node_map.copy()
                new_node[constraint[2]],new_node[constraint[0]] = new_node[constraint[0]],new_node[constraint[2]]

                if (new_node in tryout):
                    new_node = node_map.copy()
                    new_node[constraint[2]],new_node[constraint[1]] = new_node[constraint[1]],new_node[constraint[2]]

                    if (new_node in tryout):
                        return new_node

                node_map = new_node
                tryout+=[node_map]
                status = True
                break
        sys.stdout.write("\r%d" % counter)
        sys.stdout.flush()

        if(counter == 50000):
            break

    s = sorted(node_map.items(), key=operator.itemgetter(1))
    print(dup)
    return [i[0] for i in s]


def preprocess(constraints):
    pairs = {}
    for constraint in constraints:

        wiz = [constraint[0],constraint[1]]
        s = frozenset(wiz)
        
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
    return processed


def optimization(constraints):

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

    print(len(name))
    print(name)
    strategy1(order,name)
    return sorted(order,key=operator.itemgetter(0))


def strategy1(order,name):

    con_list = {k:order[:k]+order[k+1:len(order)] for k in range(len(order))}
    collect = [[k,order[k]] for k in range(len(order))]
    new_collect = []
    num_con = [len(order)-1] * len(con_list)
    seq_len = 3
    longest_seq = []
    counter = 2000
    
    while(sum(num_con) != 0 and seq_len <len(name) and counter > 0):
        dup = []


        # for each built order
        for o in collect:
            index = o[0]
            current_order = o[1]
            cons_to_choose = con_list[index]
            copy_cons = cons_to_choose[:]

            #for each constraint remain for that order
            for c in cons_to_choose:
                if (c not in copy_cons):
                    continue

                p = possible(current_order,c)

                if (p == []):
                    continue
                elif(p==[-1]):
                    copy_cons = [y for y in copy_cons if y != c]
                    continue

                copy_p = p[:]
                #remove invalid sequence
                for i in p:
                    if i not in copy_p:

                        continue

                    if not valid(i,order):
                        copy_p = [y for y in copy_p if y != i]
                        continue

                    if (seq_len < len(i)):
                        seq_len = len(i)
                        longest_seq = i
                        if(not valid(i,order)):
                            print(i)
                            print(copy_p)
                        assert(valid(i,order))

                    if i not in dup:
                        dup += [i]
                    else:
                        copy_p = [y for y in copy_p if y != i]


                new_collect += [[index,copy_p[k]] for k in range(len(copy_p))]
                copy_cons = [y for y in copy_cons if y != c]

            num_con[index] = len(copy_cons)
            con_list[index] = copy_cons[:]


        collect = new_collect[:]
        new_collect = []
        counter -= 1

    print(valid(longest_seq,order))
    print(len(longest_seq))
    print(con_list)
    print(collect)
    return longest_seq



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
        assert(not(index1<index3<index2 and index2<index3<index1))
        return  [-1]
    elif wiz_a in order and wiz_c in order:
        return possible4(order,constraint)
    elif wiz_a in order and wiz_b in order:
        return possible5(order,constraint)
    elif wiz_b in order and wiz_c in order:
        return possible6(order,constraint)
    elif wiz_a in order:
        return possible1(order,constraint)
    elif wiz_c in order:
        return possible2(order,constraint)
    elif wiz_b in order:
        return possible3(order,constraint)
    else:
        return []

#constraint 0 matches
def possible1(order, constraint):

    collect = []

    wiz_a = constraint[0]
    wiz_b = constraint[1]
    wiz_c = constraint[2]

    index = order.index(wiz_a)

    for i in range(index+1,len(order)+1):
        order1 = order[:]
        order1.insert(i,wiz_b)
        for j in range(i+1,len(order1)+1):
            order2 = order1[:]
            order2.insert(j,wiz_c)

            collect += [order2]

    return collect

#constraint 2 matches
def possible2(order, constraint):

    collect = []

    wiz_a = constraint[0]
    wiz_b = constraint[1]
    wiz_c = constraint[2]

    index = order.index(wiz_c)

    for i in range(0,index+1):
        order1 = order[:]
        order1.insert(i,wiz_b)
        for j in range(0,i+1):
            order2 = order1[:]
            order2.insert(j,wiz_a)

            collect += [order2]

    return collect


#constraint 1 matches
def possible3(order, constraint):

    collect = []

    wiz_a = constraint[0]
    wiz_b = constraint[1]
    wiz_c = constraint[2]

    index = order.index(wiz_b)

    for i in range(0,index+1):
        order1 = order[:]
        order1.insert(i,wiz_a)
        new_index = order1.index(wiz_b)
        for j in range(new_index+1,len(order1)+1):
            order2 = order1[:]
            order2.insert(j,wiz_c)

            collect += [order2]

    return collect

#constraint 0 & constraint 2 matches
def possible4(order, constraint):

    collect = []

    wiz_a = constraint[0]
    wiz_b = constraint[1]
    wiz_c = constraint[2]

    index1 = order.index(wiz_a)
    index2 = order.index(wiz_c)

    for i in range(index1+1,index2+1):
        order1 = order[:]
        order1.insert(i,wiz_b)

        collect += [order1]

    return collect

#constraint 0 & constraint 1 matches
def possible5(order,constraint):

    collect = []
    wiz_a = constraint[0]
    wiz_b = constraint[1]
    wiz_c = constraint[2]

    index = order.index(wiz_b)

    for i in range(index+1,len(order)+1):
        order1 = order[:]
        order1.insert(i,wiz_c)

        collect += [order1]
    return collect

#constraint 1 & constraint 2 matches
def possible6(order,constraint):

    collect = []
    wiz_a = constraint[0]
    wiz_b = constraint[1]
    wiz_c = constraint[2]

    index = order.index(wiz_b)

    for i in range(0,index+1):
        order1 = order[:]
        order1.insert(i,wiz_a)

        collect += [order1]
    return collect

# Given an order, there are two matchings in the constraint
def utilpossible2(order,constraint,wiz1,wiz2):

    collect = []
    wiz_a = constraint[0]
    wiz_b = constraint[1]
    wiz_c = constraint[2]

    index1 = order.index(wiz1)
    index2 = order.index(wiz2)

    if (wiz1 != wiz_c) and (wiz2 != wiz_c):

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

        if (wiz1 == wiz_c):
            otherwiz = wiz_a if wiz2 == wiz_b else wiz_b
            c_index = index1
            o_index = index2
        elif (wiz2 == wiz_c):
            otherwiz = wiz_a if wiz1 == wiz_b else wiz_b
            c_index = index2
            o_index = index1

        if c_index > o_index:
            for i in range(0,c_index+1):
                order1 = order[:]
                order1.insert(i,otherwiz)
                collect += [order1]
        else:
            for i in range(c_index+1,len(order)+1):
                order1 = order[:]
                order1.insert(i,otherwiz)
                collect += [order1]

    return collect

