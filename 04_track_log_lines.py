from infer_type_mod import resolve_type
from utils import *


globals = {}

def cortesian_sum(list_of_lists):
    if not list_of_lists:
        return []
    all_chains = list_of_lists[0]
    for next_list in list_of_lists[1:]:
        new_all_chains = []
        for chain in all_chains:
            for value in next_list:
                new_all_chains += [chain + value]
        all_chains = new_all_chains
    return all_chains


markup_by_file = {}
if 1:
    fname = ""
    source = ""
    line_offsets = []
    markup = {}
    count = 0
    for markup_fname in ["all_files_markup2.txt", "all_files_markup.txt", "all_files_markup1.txt"]:
        #if count > 100:
        #    break
        for line in open(markup_fname):
            if line.startswith("FNAME:"):
                count += 1
                if count % 1000 == 0:
                    print "..processed", count
                if fname:# and fname == "/home/arslan/src/provenance/hadoop/hadoop-tools/hadoop-streaming/src/main/java/org/apache/hadoop/streaming/io/KeyOnlyTextOutputReader.java":
                    markup_by_file[fname] = markup2tree(markup)
                    del markup
                markup = {}
                fname = line.replace("FNAME:", "").strip()
                source = open(fname).read()
                line_offsets = get_line_offsets(source)
                continue
            delim = line.find("=")
            coords, label = line[:delim], line[delim + 1: -1]
            sline, scol, eline, ecol = [int(item) for item in coords.split(":")]
            start = line_offsets[sline - 1] + scol - 1
            end = line_offsets[eline - 1] + ecol
            markup.setdefault((start, end), set()).add(label)
    markup_by_file[fname] = markup2tree(markup)
    del markup


def get_class_node(start, end, fname, fcn, source):
    #print start, end, fname
    diff = 100000
    best = ""
    for node in all_nodes(markup_by_file[fname]):
        if node.start == start and node.end == end:
            return node
        diff_new = abs(node.start - start) + abs(node.end - end)
        if diff_new < diff:
            diff = diff_new
            best = node
    print "FUCKUP", diff, fcn, best.labels
    print best.get_snippet(source)[:200]
    return None

def extract_log_calls_from_method_declartion(method_decl_node):
    log_call_stacks = []
    def get_log_call_stacks(node_stack):
        node = node_stack[-1]
        if "expr.MethodCallExpr" in node.labels:
            method_call_text = node.get_snippet(source).lower()
            pre_call_snippet = method_call_text.split("(")[0].strip()
            if pre_call_snippet.endswith("log.debug") or pre_call_snippet.endswith("log.warn") \
                    or pre_call_snippet.endswith("log.info") or pre_call_snippet.endswith("logauditmessage"):
                #if pre_call_snippet.endswith("logauditmessage"):
                #    print "CHHEEEEECKKKKKK"
                #    print method_call_text
                #    print "--"
                log_call_stacks.append([item for item in node_stack])
                return False
        return True
    method_decl_node.DFS1([], get_log_call_stacks)
    return log_call_stacks


def get_constitutes(expressionNode, source):
    log_line_elements = []
    unrolled = []
    processing_deque = [expressionNode]
    while processing_deque:
        node = processing_deque[0]
        processing_deque = processing_deque[1:]
        if "expr.StringLiteralExpr" in node.labels:
            unrolled += [node.get_snippet(source)]
            continue
        if "expr.BinaryExpr" in node.labels:
            processing_deque = node.children + processing_deque
            continue
        if "expr.SimpleName" in node.labels or "expr.NameExpr" in node.labels or "expr.ThisExpr" in node.labels:
            #print node.get_snippet(source)
            #print "---"
            #print log_call_stack[-1].get_snippet(source)
            # print "====="
            #yield node
            unrolled.append(node)
            continue
        if "expr.MethodCallExpr" in node.labels:
            cur_node = node
            all_params = []
            while cur_node and "expr.MethodCallExpr" in cur_node.labels:
                cur_node_snippet = cur_node.get_snippet(source)
                has_caller = "expr.MethodCallExpr" in cur_node.children[0].labels or \
                                "." in cur_node_snippet and cur_node_snippet.index("(") > cur_node_snippet.index(".")
                if has_caller:
                    caller = cur_node.children[0]
                    method_name = cur_node.children[1]
                    params = cur_node.children[2:]
                else:
                    caller = None
                    method_name = cur_node.children[0]
                    params = cur_node.children[1:]
                cur_node = None
                all_params = params + all_params
                if caller == None or caller.get_snippet(source) == "this":
                    unrolled += [("this", method_name.get_snippet(source), "mcall")]
                elif "expr.MethodCallExpr" in caller.labels:
                    cur_node = caller
                else:
                    unrolled += [(caller, method_name.get_snippet(source), "mcall")]
            processing_deque = all_params + processing_deque
            continue
        if "expr.FieldAccessExpr" in node.labels:
            unrolled += [(node.children[0], node.children[1].get_snippet(source), "facc")]
            continue
        if "expr.NullLiteralExpr" in node.labels:
            continue
        if "expr.EnclosedExpr" in node.labels:
            processing_deque = node.children + processing_deque
            continue
        if "expr.IntegerLiteralExpr" in node.labels:
            continue
        if "expr.ConditionalExpr" in node.labels:
            processing_deque = node.children + processing_deque
            continue
        if "expr.ArrayAccessExpr" in node.labels:
            processing_deque = node.children + processing_deque
            continue
        if "type.ClassOrInterfaceType" in node.labels:
            continue
        if "type.PrimitiveType" in node.labels:
            continue
        if "expr.DoubleLiteralExpr" in node.labels:
            continue
        if "expr.BooleanLiteralExpr" in node.labels:
            continue
        if "expr.CharLiteralExpr" in node.labels:
            unrolled += [node.get_snippet(source)]
            continue
        if "expr.UnaryExpr" in node.labels:
            processing_deque = node.children + processing_deque
            continue
        if "expr.ClassExpr" in node.labels:
            continue
        if "expr." in node.labels:
            processing_deque = node.children + processing_deque
            #print node.get_snippet(source)
            continue
        if "type.PrimitiveType" in node.labels:
            continue
        processing_deque = node.children + processing_deque
        #print node.get_snippet(source)
        #print node.labels
        #print "----"
    return unrolled


def get_method_call_params_chains_safe(method_call_node, source):
    method_snippet = method_call_node.get_snippet(source)
    positions_inside_string_constants = []
    for node in all_nodes(method_call_node):
        if "expr.StringLiteralExpr" in node.labels or "expr.CharLiteralExpr" in node.labels:
            positions_inside_string_constants += range(node.start - method_call_node.start, node.end - method_call_node.start)
    positions_inside_string_constants = set(positions_inside_string_constants)

    methods_and_params = []
    params_end_at = len(method_snippet)
    while params_end_at:
        open_bracets = 0
        params_positions = []
        params_start_at = None
        for position in xrange(params_end_at - 1, -1, -1):
            if position in positions_inside_string_constants:
                continue
            if method_snippet[position] == ")":
                open_bracets += 1
                if open_bracets == 1:
                    param_end = position
                continue
            if method_snippet[position] == "(":
                open_bracets -= 1
                if open_bracets == 0:
                    params_positions = [(position + 1, param_end)] + params_positions
                    params_start_at = position
                    break
                continue
            if open_bracets == 1 and method_snippet[position] == ",":
                params_positions = [(position + 1, param_end)] + params_positions
                param_end = position
        if params_start_at == None:
            break
        method_name = method_snippet[:params_start_at].split(".")[-1].split("=")[-1].split(" ")[-1].strip()
        #print "chunk:", method_name, "||", method_snippet[params_start_at:params_end_at].replace("\n", " ")
        #print "->->", params_positions
        params_positions = [(start + method_call_node.start, end + method_call_node.start)  for start, end in params_positions]
        parameters = [[] for _ in xrange(len(params_positions))]
        for node in all_nodes(method_call_node):  # assumes BFS or DFS manner of all_nodes
            for param_pos in xrange(len(params_positions)):
                start, end = params_positions[param_pos]
                if node.start >= start and node.end <= end:
                    if not parameters[param_pos] or parameters[param_pos][-1].end <= node.start:
                        parameters[param_pos].append(node)
        #print "->->", parameters
        methods_and_params = [(method_name, parameters)] + methods_and_params
        params_end_at = params_start_at
    return methods_and_params


def get_method_call_params(method_call_node, source, debug=False):
    method_snippet = method_call_node.get_snippet(source)
    open_bracets = 0
    params_positions = []
    param_end = None
    positions_inside_string_constants = []
    check = []
    for node in all_nodes(method_call_node):
        if "expr.StringLiteralExpr" in node.labels or "expr.CharLiteralExpr" in node.labels:
            check += [node.get_snippet(source)]
            positions_inside_string_constants += range(node.start - method_call_node.start, node.end - method_call_node.start)
    positions_inside_string_constants = set(positions_inside_string_constants)
    params_start_at = None
    for position in xrange(len(method_snippet) - 1, -1, -1):
        if position in positions_inside_string_constants:
            continue
        if method_snippet[position] == ")":
            open_bracets += 1
            if open_bracets == 1:
                param_end = position
            continue
        if method_snippet[position] == "(":
            open_bracets -= 1
            if open_bracets == 0:
                if position + 1 < param_end and method_snippet[position + 1:param_end].strip():
                    params_positions = [(position + 1, param_end)] + params_positions
                params_start_at = position
                break
            continue
        if open_bracets == 1 and method_snippet[position] == ",":
            params_positions = [(position + 1, param_end)] + params_positions
            param_end = position
    method_name = method_snippet[:params_start_at].split(".")[-1]
    caller = None
    params_positions = [(start + method_call_node.start, end + method_call_node.start)  for start, end in params_positions]

    parameters = [[] for _ in xrange(len(params_positions))]
    for node in all_nodes(method_call_node):#assumes BFS or DFS manner of all_nodes
        if not caller and node.start == method_call_node.start and node.end - node.start <= params_start_at - len(method_name):
            caller = node
        for param_pos in xrange(len(params_positions)):
            start, end = params_positions[param_pos]
            if node.start >= start and node.end <= end:
                if not parameters[param_pos] or parameters[param_pos][-1].end <= node.start:
                    parameters[param_pos].append(node)
    if debug:
        print method_snippet
        print "\tcaller:", caller and caller.get_snippet(source).replace("\n", " ") or None
        print "\tmethod name:", method_name
        for param_pos in xrange(len(params_positions)):
            start, end = params_positions[param_pos]
            #print "\t-> ", method_snippet[start - method_call_node.start:end - method_call_node.start].replace("\n", " ")
            for node in parameters[param_pos]:
                print "\t\t--- ", node.get_snippet(source).replace("\n", " "), node.start, node.end

    if [1 for array in parameters if len(array) != 1]:
        #TODO: reconsider action
        return (caller, method_name, [])

    parameters = [nodes[0] for nodes in parameters]
    return (caller, method_name, parameters)

stat = [0, 0, 0]

THIS = 3224232434
expanded = [0, 0, 0]
sb_expanded = [0, 0]
def expand_string_var(string_var_node, root_node, source):
    expanded[2] += 1
    path2var_node = build_path(string_var_node, root_node)
    method_node = None
    for node_in_path in path2var_node:
        if node_in_path.labels & set(["body.MethodDeclaration", 'body.ConstructorDeclaration']):
            method_node = node_in_path
    variable_assignement_nodes = []
    other_occurences = []
    obj_snippet = string_var_node.get_snippet(source)
    def find_variable_updates(stack):
        leaf = stack[-1]
        if leaf.start >= string_var_node.start:
            return False
        if leaf.get_snippet(source) == obj_snippet:
            used = False
            for node in stack:
                if ("body.VariableDeclarator" in node.labels or "expr.AssignExpr" in node.labels) and node.children:
                    if node.end < string_var_node.start:
                        first_child = node.children[0]
                        while first_child.children:
                            first_child = first_child.children[0]
                        if first_child.get_snippet(source) == obj_snippet:
                            variable_assignement_nodes.append(node)
                            used = True
            if not used:
                other_occurences.append( (stack[-3].get_snippet(source), [node.labels for node in stack[1:]], ) )
        return True
    method_node.DFS1([], find_variable_updates)
    if len(variable_assignement_nodes):
        expanded[1] += 1
    if len(variable_assignement_nodes) == 1:
        expanded[0] += 1
    return [assignement.children[1:] for assignement in variable_assignement_nodes]




def expand_stringbuilder_var(stringbuilder_var_node, root_node, source):
    sb_expanded[1] += 1
    path2var_node = build_path(stringbuilder_var_node, root_node)
    method_node = None
    for node_in_path in path2var_node:
        if node_in_path.labels & set(["body.MethodDeclaration", 'body.ConstructorDeclaration']):
            method_node = node_in_path
    variable_assignement_nodes = []
    obj_snippet = stringbuilder_var_node.get_snippet(source)
    var_declaration_nodes = []
    #print obj_snippet
    used_spaces = set()
    def find_variable_updates(stack):
        leaf = stack[-1]
        if leaf.start >= stringbuilder_var_node.start:
            return False
        if leaf.get_snippet(source) == obj_snippet:
            for node in stack:
                considered = False
                for position in xrange(node.start, node.end):
                    if position in used_spaces:
                        considered = True
                        break
                if considered:
                    continue
                if "body.VariableDeclarator" in node.labels and node.children:
                    declare_snippet = node.get_snippet(source).replace("\n", " ")
                    #print "VARDECL", declare_snippet
                    if "StringBuilder(" in declare_snippet:
                        var_declaration_nodes.append(node)
                        constitutes = []
                        methods_and_params = get_method_call_params_chains_safe(node, source)
                        for method_name, params in methods_and_params:
                            if "StringBuilder" in method_name:
                                if len(params) != 1 or not params[0] or not "expr.IntegerLiteralExpr" in params[0][0].labels:
                                    for param_nodes in params:
                                        constitutes += param_nodes
                            elif "append" in method_name:
                                for param_nodes in params:
                                    constitutes += param_nodes
                            else:
                                print "ADFAFASDADFSA", method_name
                    else:
                        constitutes = node.children[1:]
                        #print "CHEEECK:", [elem.get_snippet(source).replace("\n", " ") for elem in constitutes]
                    #for constitute in constitutes:
                    #    print "\t\t-> ", constitute.get_snippet(source)
                    for constitute in constitutes:
                        variable_assignement_nodes.append(constitute)
                    for position in xrange(node.start, node.end):
                        used_spaces.add(position)
                if "expr.AssignExpr" in node.labels and node.children:
                    #print "ASSIGN", node.get_snippet(source).replace("\n", " ")
                    pass
                if "expr.MethodCallExpr" in node.labels and node.children:
                    node_snippet = node.get_snippet(source).replace("\n", " ")
                    if node_snippet.startswith(obj_snippet):
                        #print "MethodCall", node_snippet
                        constitutes = []
                        methods_and_params = get_method_call_params_chains_safe(node, source)
                        for method_name, params in methods_and_params:
                            if "StringBuilder" in method_name or "append" in method_name:
                                for param_nodes in params:
                                    constitutes += param_nodes
                            else:
                                print "ADFAFASDADFSA", method_name
                            # print "CHEEECK:", [elem.get_snippet(source).replace("\n", " ") for elem in constitutes]
                        for constitute in constitutes:
                            variable_assignement_nodes.append(constitute)
                        for position in xrange(node.start, node.end):
                            used_spaces.add(position)
        return True
    method_node.DFS1([], find_variable_updates)
    variable_assignement_nodes = sorted(variable_assignement_nodes, key= lambda node : node.end)
    if var_declaration_nodes:
        min_node_start = max([node.start for node in  var_declaration_nodes])
        variable_assignement_nodes = [node for node in variable_assignement_nodes if node.start >= min_node_start]
    #print "Selected nodes:"
    #for node in variable_assignement_nodes:
    #    print "selected:\t", node.get_snippet(source).replace("\n", " ")
    branches_keys = set()
    branches = []
    var_modifications = []
    for node_index in xrange(len(variable_assignement_nodes)):
        node = variable_assignement_nodes[node_index]
        path2var_node = build_path(node, root_node)
        cond_path = []
        cond_path_str = ""
        for path_pos in xrange(len(path2var_node) - 1):
            path_node = path2var_node[path_pos]
            next_path_node = path2var_node[path_pos + 1]
            if 'stmt.IfStmt' in path_node.labels:
                child_index = [index for index in xrange(len(path_node.children)) if path_node.children[index] == next_path_node][0]
                cond_path += [(path_node.start, path_node.end, child_index)]
                cond_path_str += str(path_node.start) + ":" + str(path_node.end) + ":" + str(child_index) + "_"
        var_modifications += [(cond_path_str, node)]
        if cond_path and not (cond_path_str in branches_keys):
            branches.append(cond_path)
            branches_keys.add(cond_path_str)

    final_chains = []
    #print branches
    for comb in xrange(2 ** len(branches)):
        taken_branches = []
        not_taken_branches = []
        ifs = {}
        for branch in branches:
            take = comb % 2
            comb >>= 1
            if take:
                taken_branches.append(branch)
                for ifstart, ifend, branch_index in branch:
                    ifs.setdefault((ifstart, ifend), set()).add(branch_index)
            else:
                not_taken_branches.append(branch)
        controversial = False
        for if_key, taken_branches_indices in ifs.items():
            if len(taken_branches_indices) != 1:
                controversial = True
                break
        if not controversial:
            taken_ifs_selection = []
            for taken_branch in taken_branches:
                taken_ifs_selection += taken_branch
            for not_taken_branch in not_taken_branches:
                if not_taken_branch[-1] in taken_ifs_selection:
                    controversial = True
                    break
        if controversial:
            continue
        taken_branches_keys = set(["".join([str(ifstart) + ":" + str(ifend) + ":" + str(if_ch_index) + "_" \
                                for ifstart, ifend, if_ch_index in branch]) for branch in taken_branches])
        #print "--"
        chain = []
        for branch_key, node in var_modifications:
            if not branch_key or branch_key in taken_branches_keys:
                chain.append(node)
                #print "\t\t--> ", node.get_snippet(source).replace("\n", " ")
        if chain:
            final_chains.append(chain)
        #print "--"
    #print "-------"
    #print len(branches_keys), branches_keys, branches
    return final_chains





def expand(node, source, get_var_type_func, root_node):
    if type(node) == str:
        return [[node]]
    if node == THIS:
        return [[THIS]]
    if "expr.StringLiteralExpr" in node.labels:
        return [[node.get_snippet(source).strip()[1:-1].replace("\\\"", "\"").replace("\\n", "<BR>").replace("\\t", "<TAB>") ]]
    if "expr.CharLiteralExpr" in node.labels:
        return [[node.get_snippet(source).strip()[1:-1].replace("\\\"", "\"").replace("\\n", "<BR>").replace("\\t", "<TAB>") ]]
    if "expr.IntegerLiteralExpr" in node.labels:
        return [[node.get_snippet(source)], []]
    if "expr.DoubleLiteralExpr" in node.labels:
        return [[node.get_snippet(source)], []]
    if "expr.BooleanLiteralExpr" in node.labels:
        return [[node.get_snippet(source)], []]
    if "expr.NullLiteralExpr" in node.labels:
        return [["null"], []]
    if "expr.BinaryExpr" in node.labels or 'expr.EnclosedExpr' in node.labels:
        outputs = [[]]
        for subnode in node.children:
            suffixes = expand(subnode, source, get_var_type_func, root_node)
            new_outputs = []
            for output in outputs:
                for suffix in suffixes:
                    new_outputs += [output + suffix]
            outputs = new_outputs
        return outputs
    if "expr.ConditionalExpr" in node.labels:
        if len(node.children) != 3:
            print "FUCKUP in conditional expression"
            exit()
        return expand(node.children[1], source, get_var_type_func, root_node) + expand(node.children[2], source, get_var_type_func, root_node)

    if "expr.ThisExpr" in node.labels:
        return [[THIS]]

    if "expr.SimpleName" in node.labels or "expr.NameExpr" in node.labels:
        node_type = get_var_type_func(node)
        if node_type == "String":
            possible_expansions = expand_string_var(node, root_node, source)
            all_chains = []
            for chain in possible_expansions:
                all_chains += cortesian_sum([expand(chain_node, source, get_var_type_func, root_node) for chain_node in chain])
            if all_chains:
                return all_chains
        if node_type and "StringBuilder" in node_type:
            #print "Started for:", node_type, "::", node.get_snippet(source)
            possible_expansions = expand_stringbuilder_var(node, root_node, source)
            all_chains = []
            for chain in possible_expansions:
                #for node in chain:
                #    print "-->\t", node.get_snippet(source)
                #print "--"
                all_chains += cortesian_sum([expand(chain_node, source, get_var_type_func, root_node) for chain_node in chain])
            if all_chains:
                return all_chains
        return [[node]]

    if "expr.FieldAccessExpr" in node.labels:
        return [[node]]

    if "expr.ArrayAccessExpr" in node.labels:
        return [[node.children[0]]]

    if "expr.UnaryExpr" in node.labels:
        return [node.children]

    if "expr.MethodCallExpr" in node.labels:
        caller, method_name, params = get_method_call_params(node, source)
        if not params and method_name == "toString":
            return caller and expand(caller, source, get_var_type_func, root_node) or [[THIS]]
        if len(params) == 1 and not caller and method_name == "toString":
            return [[params[0]]]
        if method_name in ["stringify", "stringifyException"]:
            return [[params[0]]]
        if method_name in ["formatTime"] and caller and caller.get_snippet(source) == "StringUtils":
            return [params]
        if method_name in ["join"] and caller and caller.get_snippet(source) == "StringUtils":
            if params[1].labels & set(['expr.CharLiteralExpr', "expr.StringLiteralExpr"]):
                return [[params[0]]]
            else:
                return [[params[1]]]
        if method_name in ["byteDesc"] and caller and caller.get_snippet(source) == "StringUtils":
            return [[params[0]]]
        if method_name in ["toString", "asList"] and caller and caller.get_snippet(source) == "Arrays":
            return [[params[0]]]
        if caller and caller.get_snippet(source).startswith("Joiner"):
            return [[params[0]]]
        if caller and caller.get_snippet(source) == "TextFormat":
            return [[params[0]]]
        if method_name in ["mapToString"] and caller and caller.get_snippet(source) == "QuorumCall":
            return [[params[0]]]

        if caller and caller.get_snippet(source).startswith("MessageFormat") and method_name == "format":
            format_string = ""
            for subnode in all_nodes_post_order(params[0]):
                if "expr.BinaryExpr" in subnode.labels:
                    continue
                if not "expr.StringLiteralExpr" in subnode.labels:
                    #TODO: expand
                    print "FUCKU11111P1111"
                    return [[node]]
                    exit()
                format_string += subnode.get_snippet(source).strip()[1:-1]
            by_pos = []
            keys = []
            for format_param_index in xrange(1, len(params)):
                key = "{" + str(format_param_index - 1) + "}"
                by_pos += [(format_string.find(key), format_param_index)]
                keys.append(key)
            for key in keys:
                format_string = format_string.replace(key, "{}")
            by_pos.sort()
            unrolled = [params[format_param_index] for _, format_param_index in by_pos]
            format_string_chunks = format_string.split("{}")
            for chunk_index in xrange(len(format_string_chunks) - 1, 0, -1):
                unrolled = unrolled[:chunk_index] + [format_string_chunks[chunk_index]] + unrolled[chunk_index:]
            unrolled = [format_string_chunks[0]] + unrolled
            if 1:
                outputs = [[]]
                for subnode in unrolled:
                    suffixes = expand(subnode, source, get_var_type_func, root_node)
                    new_outputs = []
                    for output in outputs:
                        for suffix in suffixes:
                            new_outputs += [output + suffix]
                    outputs = new_outputs
                return outputs

        if caller and caller.get_snippet(source) == "String" and method_name == "format":
            format_string = ""
            for subnode in all_nodes_post_order(params[0]):
                if "expr.BinaryExpr" in subnode.labels:
                    continue
                if set(['expr.NameExpr', 'expr.SimpleName']) & subnode.labels and subnode.get_snippet(source) in globals:
                    print "YAMMI", subnode.get_snippet(source), globals[subnode.get_snippet(source)]
                    format_string += globals[subnode.get_snippet(source)][0]
                    continue
                if not "expr.StringLiteralExpr" in subnode.labels:
                    print "FUCKU11111P", subnode.labels
                    print node.get_snippet(source)
                    return [[node]]
                format_string += subnode.get_snippet(source).strip()[1:-1]

            import re
            keys = re.findall("%[0-9\.]*[a-z]", format_string)
            for key in keys:
                format_string = format_string.replace(key, "{}")
            unrolled = params[1:]
            format_string_chunks = format_string.split("{}")
            for chunk_index in xrange(len(format_string_chunks) - 1, 0, -1):
                unrolled = unrolled[:chunk_index] + [format_string_chunks[chunk_index]] + unrolled[chunk_index:]
            unrolled = [format_string_chunks[0]] + unrolled
            if 1:
                outputs = [[]]
                for subnode in unrolled:
                    suffixes = expand(subnode, source, get_var_type_func, root_node)
                    new_outputs = []
                    for output in outputs:
                        for suffix in suffixes:
                            new_outputs += [output + suffix]
                    outputs = new_outputs
                return outputs
    return [[node]]
    """
    if "expr.EnclosedExpr" in node.labels:
        processing_deque = node.children + processing_deque
        continue
    if "expr.ArrayAccessExpr" in node.labels:
        processing_deque = node.children + processing_deque
        continue
    if "type.ClassOrInterfaceType" in node.labels:
        continue
    if "type.PrimitiveType" in node.labels:
        continue
    if "expr.ClassExpr" in node.labels:
        continue
    if "expr." in node.labels:
        processing_deque = node.children + processing_deque
        # print node.get_snippet(source)
        continue
    if "type.PrimitiveType" in node.labels:
        continue
    """



def get_log_line_constitutes(log_call_stack, source, get_var_type_func):
    log_call_node = log_call_stack[-1]
    _, _, parameters = get_method_call_params(log_call_node, source)
    if not parameters:
        return None
    expanded_params_chains = [expand(param, source, get_var_type_func, log_call_stack[0]) for param in parameters]
    unrolled_chains = [[item] for item in expanded_params_chains[0]]
    expanded_params_chains = expanded_params_chains[1:]
    while expanded_params_chains:
        next_chunk = expanded_params_chains[0]
        expanded_params_chains = expanded_params_chains[1:]
        new_all_chains = []
        for chain in unrolled_chains:
            for add_chain in next_chunk:
                new_all_chains += [chain + [add_chain]]
        unrolled_chains = new_all_chains
    return unrolled_chains


def to_prev_leaf(stack):
    stack = [item for item in stack]
    change_pos = 0
    while len(stack) > 1:
        leaf = stack[-1]
        stack.pop()
        stop = False
        for index in xrange(len(stack[-1].children)):
            if stack[-1].children[index] == leaf:
                change_pos = index
                break
        if change_pos > 0:
            break
    if change_pos == 0:
        return []
    stack.append(stack[-1].children[change_pos - 1])
    while stack[-1].children:
        stack.append(stack[-1].children[-1])
    return stack

def get_local_var_type(var_node, class_node, fcn, source, extents, imports, type_params, extended_variables, fcn_dict):
    var_name = var_node.get_snippet(source)
    path2target = build_path(var_node, class_node)
    for cut_depth in xrange(len(path2target)):
        if path2target[cut_depth].labels & set(["body.MethodDeclaration", 'body.ConstructorDeclaration']):
            path2target = path2target[cut_depth:]
            break
    while True:
        leaf_node = path2target[-1]
        if leaf_node.labels & set(["expr.SimpleName", "expr.NameExpr"]) and leaf_node.get_snippet(source).replace("[]", "") == var_name:
            """
            if var_name == "reports":
                for node in path2target:
                    print node.labels, node.get_snippet(source)[:100]
                    print "-"
                print "-----"
            """
            for depth in xrange(len(path2target) - 1):
                # print "------- ", path2target[depth].get_snippet(source), path2target[depth].labels
                if set(["stmt.CatchClause"]) & path2target[depth].labels:
                    if len(path2target[depth].children) < 2 and set(['type.UnionType']) & path2target[depth + 1].labels:
                        types = []
                        name_node = None
                        for child_node in path2target[depth + 1].children:
                            if 'type.ClassOrInterfaceType' in child_node.labels:
                                types.append(child_node)
                            else:
                                name_node = child_node
                                break
                        if name_node and name_node.get_snippet(source) == var_name:
                            return types[0]
                    else:
                        type_node = path2target[depth].children[0]
                        name_node = path2target[depth].children[1]
                        if name_node.get_snippet(source) == var_name:
                            return type_node
                elif ("expr.VariableDeclarationExpr" in path2target[depth].labels or
                                                     'body.Parameter' in path2target[depth].labels):
                    """
                    if var_name == "notification":
                        print path2target[depth].labels
                        print path2target[depth].get_snippet(source)
                        for ch_index in xrange(len(path2target[depth].children)):
                            print str(ch_index) + "."
                            print "\t", path2target[depth].children[ch_index].labels
                            print "\t", path2target[depth].children[ch_index].get_snippet(source)
                    """

                    type_node = path2target[depth]
                    while type_node.children:
                        type_node = type_node.children[0]
                    for node in all_nodes(path2target[depth]):
                        if 'body.VariableDeclarator' in node.labels:
                            name_node = node
                            while name_node.children:
                                name_node = name_node.children[0]
                            #if var_name == "reports":
                            #    print "CHECK", type_node.get_snippet(source), "|||", name_node.get_snippet(source)
                            if name_node.get_snippet(source).replace("[]", "").strip() == var_name:
                                return type_node


                    if len(path2target[depth].children) < 2 and 'type.ArrayType' in path2target[depth + 1].labels:
                        type_node = path2target[depth + 1].children[0]
                        name_node = path2target[depth + 1].children[1]
                        while name_node.children:
                            name_node = name_node.children[0]
                        if name_node.get_snippet(source).replace("[]", "").strip() == var_name:
                            return type_node
                    else:
                        if "body.VariableDeclarator" in path2target[depth].children[1].labels:
                            type_node = path2target[depth].children[0]
                            while type_node.children:
                                type_node = type_node.children[0]
                            name_node = path2target[depth].children[1]
                            while name_node.children:
                                name_node = name_node.children[0]
                            if name_node.get_snippet(source).replace("[]", "").strip() == var_name:
                                return type_node
                        elif path2target[depth].children[1].labels & set(["expr.SimpleName", "expr.NameExpr"]):
                            type_node = path2target[depth].children[0]
                            while type_node.children:
                                type_node = type_node.children[0]
                            name_node = path2target[depth].children[1]
                            if name_node.get_snippet(source).replace("[]", "").strip() == var_name:
                                return type_node
                        elif 'expr.MarkerAnnotationExpr' in path2target[depth].children[0].labels and \
                                        'type.ClassOrInterfaceType' in path2target[depth].children[1].labels:
                            type_node = path2target[depth].children[1]
                            while type_node.children:
                                type_node = type_node.children[0]
                            name_node = path2target[depth].children[2]
                            while name_node.children:
                                name_node = name_node.children[0]
                            if name_node.get_snippet(source).replace("[]", "").strip() == var_name:
                                return type_node
                            pass
                        else:
                            pass
                            """
                            print "FUCKUP"
                            print path2target[depth].get_snippet(source)
                            for child in path2target[depth].children:
                                print "\t", child.get_snippet(source), "|||", child.labels
                            print
                            "----"
                            """


        path2target = to_prev_leaf(path2target)
        if not path2target:
            break
    return None

def get_var_type(var_node, class_node, fcn, fname, source, extended_extents, imports, type_params, extended_variables, fcn_dict):
    var_name = var_node.get_snippet(source)
    local_type_node = get_local_var_type(var_node, class_node, fcn, source, extended_extents, imports, type_params, extended_variables, fcn_dict)
    if local_type_node:
        return local_type_node.get_snippet(source)

    for field_name, var_type in extended_variables:
        if field_name == var_name:
            return var_type
    for imp in imports:
        if imp.endswith("." + var_name) or imp.endswith(".*"):
            imported_fcn = imp.replace("." + var_name, "").replace(".*", "").strip()
            if imported_fcn in fcn_dict:
                imported_vars = fcn_dict[imported_fcn][7]
                for field_name, var_type in imported_vars:
                    if field_name == var_name:
                        return var_type

    for extent_fcn in extended_extents:
        if extent_fcn in fcn_dict:
            extent_fcn_fields = fcn_dict[extent_fcn][7]
            for field_name, var_type in extent_fcn_fields:
                if field_name == var_name:
                    return var_type

    chunks = fcn.split(".")
    for depth in xrange(1, len(chunks)):
        parent_fcn = ".".join(chunks[:depth])
        if parent_fcn in fcn_dict:
            parent_fcn_fields = fcn_dict[parent_fcn][7]
            for field_name, var_type in parent_fcn_fields:
                if field_name == var_name:
                    return var_type

    #print "NOT FOUND"
    #print fcn, fname
    #print var_name
    return None



print "start"

processed = 0
fcn_dict = {}
for line in open("all_classes_detailed_info_with_resolved_vars.txt"):
    processed += 1
    if processed % 1000 == 0:
        print "..uploaded", processed
    fcn, extents, package, first, last, fname, imports, type_params, extended_variables = line[:-1].split("\t")
    first, last = int(first), int(last)
    extents = [item for item in extents.split("|") if item]
    imports = [item for item in imports.split("|") if item]
    type_params = [item for item in type_params.split("|") if item]
    extended_variables = [item.split() for item in extended_variables.split("|") if item]
    fcn_dict[fcn] = (fcn, fname, first, last, extents, imports, type_params, extended_variables, package)

for fcn, data in fcn_dict.items():
    processed += 1
    if processed % 1000 == 0:
        print "..uploaded", processed, stat
    fcn, fname, first, last, extents, imports, type_params, extended_variables, package = data
    source = open(fname).read()
    class_node = get_class_node(first, last, fname, fcn, source)
    for node in class_node.children:
        if not 'body.FieldDeclaration' in node.labels:
            continue
        snippet = node.get_snippet(source)
        if not " String " in snippet or not " final " in snippet:
            continue
        initial_node = node
        node = node.children[-1]
        if len(node.children) != 2:
            continue
        var_name, var_value = node.children
        var_name = var_name.get_snippet(source)
        unrolled = []
        deque = [var_value]
        parsable = True
        while deque and parsable:
            curr = deque[0]
            deque = deque[1:]
            if "expr.StringLiteralExpr" in curr.labels or "expr.CharLiteralExpr" in curr.labels:
                unrolled += [curr.get_snippet(source).strip()[1:-1].replace("\\\"", "\"").replace("\\n", "<BR>").replace("\\t", "<TAB>")]
            elif "expr.BinaryExpr" in curr.labels or 'expr.EnclosedExpr' in curr.labels:
                deque = curr.children + deque
            elif set(['expr.NameExpr', 'expr.SimpleName']) & curr.labels:
                if curr.get_snippet(source) in globals:
                    unrolled += [globals[curr.get_snippet(source)][0]]
                else:
                    parsable = False
                    break
            elif "expr.FieldAccessExpr" in curr.labels or 'expr.ObjectCreationExpr' in curr.labels:
                parsable = False
                break
            elif 'expr.MethodCallExpr' in curr.labels:
                parsable = False
                break
            elif 'expr.ConditionalExpr' in curr.labels:
                parsable = False
                break
            else:
                parsable = False
                break
        #if "START_MESSAGE" in var_name:
        #    print var_name, parsable, unrolled, [node.get_snippet(source).replace("\n", " ") for node in deque]
        if parsable:
            globals.setdefault(var_name, []).append("".join(unrolled))


processed = 0
log_exps = 0
for fcn, data in fcn_dict.items():
    processed += 1
    if processed % 1000 == 0:
        print "..uploaded", processed, stat
    fcn, fname, first, last, extents, imports, type_params, extended_variables, package = data

    extended_extents = set(extents)
    layer = extents
    while layer:
        new_layer = []
        for class_name in layer:
            if class_name in fcn_dict:
                new_layer += fcn_dict[class_name][4]
        layer = set(new_layer) - extended_extents
        extended_extents = extended_extents | layer

    source = open(fname).read()
    class_node = get_class_node(first, last, fname, fcn, source)
    method_nodes = []
    def collect_method_nodes(node_stack):
        # don't go into subclasses
        if len(node_stack) > 1 and node_stack[-1].labels & set(['body.ClassOrInterfaceDeclaration',
                                                                'body.EnumDeclaration',
                                                                'body.ClassDeclaration',
                                                                'body.InterfaceDeclaration']):
            return False
        if node_stack[-1].labels & set(["body.MethodDeclaration", 'body.ConstructorDeclaration']):
            method_node = node_stack[-1]
            method_nodes.append(method_node)
            return False
        return True
    class_node.DFS1([], collect_method_nodes)

    for method_node in method_nodes:
        for log_call_stack in extract_log_calls_from_method_declartion(method_node):
            #print log_call_stack
            #print log_call_stack[-1].get_snippet(source)

            def get_var_type_func(node):
                obj_type = get_var_type(node, class_node, fcn, fname, source,
                                        extended_extents, imports,
                                        type_params, extended_variables, fcn_dict)
                return obj_type
            unrolled_log_line_elements = get_log_line_constitutes(log_call_stack, source, get_var_type_func)
            if not unrolled_log_line_elements:
                continue

            unrolled_log_line_elements_merged = []
            if 1:
                for unrolled_param_set in unrolled_log_line_elements:
                    final_set_of_nodes = []
                    first_param_nodes = unrolled_param_set[0]
                    used_params = set()
                    curr_param_index = 1
                    added_param_sets = 0
                    for node in first_param_nodes:
                        if type(node) != str:
                            final_set_of_nodes.append(node)
                            continue
                        string_constant = node
                        placeholders = re.findall("\{[0-9]*\}", string_constant)
                        #print placeholders, [string_constant], unrolled_param_set
                        for placeholder in placeholders:
                            plhld_pos = string_constant.find(placeholder)
                            prefix, string_constant = string_constant[:plhld_pos], string_constant[plhld_pos + len(placeholder):]
                            if prefix:
                                final_set_of_nodes.append(prefix)
                            if placeholder[1:-1]:
                                curr_param_index = int(placeholder[1:-1]) + 1

                            if curr_param_index >= len(unrolled_param_set):
                                print "WTF:", [curr_param_index], unrolled_param_set
                                curr_param_index = len(unrolled_param_set) - 1
                            used_params.add(curr_param_index)
                            final_set_of_nodes += unrolled_param_set[curr_param_index]
                            added_param_sets += 1
                            curr_param_index += 1
                        if string_constant:
                            final_set_of_nodes.append(string_constant)
                    for param_index in xrange(1, len(unrolled_param_set)):
                        if not param_index in used_params:
                            final_set_of_nodes += unrolled_param_set[param_index]
                            added_param_sets += 1
                    if added_param_sets + 1 != len(unrolled_param_set):
                        print "FADASDADSFADSFASDFASDFADAFUKUCUP", added_param_sets, len(unrolled_param_set)
                        print method_node.get_snippet(source)
                        print "----"
                    unrolled_log_line_elements_merged += [final_set_of_nodes]

            for log_line_nodes in unrolled_log_line_elements_merged:
                serialized_param = []
                for node in log_line_nodes:
                    if type(node) == str:
                        serialized_param += ["SC:" + node]
                    elif node == THIS:
                        serialized_param += ["VR:" + fcn + ":::this"]
                    elif set(["expr.SimpleName", "expr.NameExpr"]) & node.labels:
                        node_type = get_var_type_func(node)
                        node_snippet = node.get_snippet(source).strip().replace("\n", " ")
                        serialized_param += ["VR:" + str(node_type) + ":::" + node_snippet]
                    elif "expr.MethodCallExpr" in node.labels or "expr.FieldAccessExpr" in node.labels:
                        caller_type = None
                        node_snippet = node.get_snippet(source).strip().replace("\n", " ")
                        if node_snippet.find("(") > 0 and  node_snippet.find("(") < node.get_snippet(source).find(".") or node.get_snippet(source).find(".") < 0:
                            #print "CHEEECK", node_snippet
                            caller_type = fcn
                        else:
                            caller = node
                            while caller.children:
                                caller = caller.children[0]
                            caller_snippet = caller.get_snippet(source).strip()
                            if "expr.ThisExpr" in caller.labels:
                                caller_type = fcn
                            elif caller_snippet.startswith("org.") or caller_snippet.startswith("java.") or caller_snippet[0].isupper():
                                caller_type = caller_snippet
                            else:
                                caller_type = get_var_type_func(caller)
                        serialized_param += ["MC:" + str(caller_type) + ":::" + node_snippet]
                    else:
                        serialized_param += ["UN:" + "_" + ":::" + node.get_snippet(source).strip().replace("\n", " ")]
                print "SPS:\t" + fcn + "RRRRRRRR" + package + "RRRRRRRR" + "<>>>>>>>___".join(serialized_param)
print log_exps
print expanded


