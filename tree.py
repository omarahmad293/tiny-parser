from graphviz import Graph
from main import program, Tree


def traverse_tree(t, childID, parentID, G):
    if childID is not None:  # child parent
        if type(t) == list:  # statement_seq (siblings)
            sibling_id = childID
            max_id = childID

            flag = False

            for p in G.body:
                count = 0
                if p.strip().startswith(str(parentID)) and 'IF' in p:
                    for string in G.body:
                        if f"\t{parentID} -- " in string:
                            count += 1

                    if count == 2:
                        flag = True
                        break

            if flag:
                G.edge(str(parentID), str(max_id), style='dashed')
            else:
                G.edge(str(parentID), str(max_id))

            for node in t:
                if node:
                    if max_id != childID:
                        max_id += 1

                    G.node(str(max_id), str(node.data))
                    new_parent = max_id

                    if max_id != childID:
                        G.edge(str(sibling_id), str(max_id), constraint='true')
                        G.body.append("{rank=same " + str(max_id) + " " + str(sibling_id) + "}")
                        sibling_id = max_id

                    if node.children:
                        for child in node.children:
                            max_id = traverse_tree(child, max_id + 1, new_parent, G)

            return max_id

        elif type(t) == Tree:  # single node
            if t:
                max_id = childID
                if 'op' in t.data or 'id' in t.data or 'const' in t.data:
                    G.node(str(childID), t.data, shape='oval')
                else:
                    G.node(str(childID), t.data)

                G.edge(str(parentID), str(childID))

                if t.children:
                    for child in t.children:
                        max_id = traverse_tree(child, max_id + 1, childID, G)

                return max_id

    else:  # root
        max_id = -1
        sibling_id = 0

        for node in t:
            if node:
                max_id += 1

                G.node(str(max_id), str(node.data))

                if max_id != 0:
                    G.edge(str(sibling_id), str(max_id), constraint='false')

                sibling_id = max_id

                if node.children:
                    for child in node.children:
                        max_id = traverse_tree(child, max_id + 1, sibling_id, G)


def draw():
    G = Graph(comment='Syntax Tree', node_attr={'shape': 'rectangle'})
    t = program()
    traverse_tree(t, None, 0, G)
    return G.render('image', format='pdf', view=True, cleanup=False)
