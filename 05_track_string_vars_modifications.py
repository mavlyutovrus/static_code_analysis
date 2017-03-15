from infer_type_mod import resolve_type
from utils import *


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

expanded = 0
total = 0
for line in open("l"):
    if line.startswith("KKK:"):
        fname, class_node_str, method_node_str, full_type, obj_snippet = line[4:-1].split(">>><<<")
        source = open(fname).read()
        class_node = FromString2Node(class_node_str)
        method_node = FromString2Node(method_node_str)
        variable_assignement_nodes = []
        def find_variable_updates(stack):
            leaf = stack[-1]
            if leaf.get_snippet(source) == obj_snippet:
                for node in stack:
                    if "body.VariableDeclarator" in node.labels and node.children:
                        first_child = node.children[0]
                        while first_child.children:
                            first_child = first_child.children[0]
                        if first_child.get_snippet(source) == obj_snippet:
                            variable_assignement_nodes.append(node)
            return True
        method_node.DFS1([], find_variable_updates)
        if variable_assignement_nodes:
            expanded += 1
        else:
            print obj_snippet
            print method_node.get_snippet(source)
            print "---"
        total += 1

        constitutes = []
        for node in variable_assignement_nodes:
            constitutes = get_constitutes(node, source)
