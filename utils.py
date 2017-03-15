import re




def remove_comments(source_txt):
    orig_source_len = len(source_txt)

    while "\\\\" in source_txt:
        source_txt = source_txt.replace("\\\\", "||")
    while "\\\"" in source_txt:
        source_txt = source_txt.replace("\\\"", "||")
    while "\\'" in source_txt:
        source_txt = source_txt.replace("\\'", "||")
    while "\\\n" in source_txt:
        source_txt = source_txt.replace("\\\n", "||")

    one_line_comment = False
    multi_line_comment = False
    string_constant1 = False
    string_constant2 = False
    filtered = ""
    prev = ""
    for curr in source_txt:
        if curr == "\n":
            one_line_comment = False
            string_constant1 = False
            string_constant2 = False
        elif curr == "*":
            if prev == "/":
                if one_line_comment or string_constant1 or string_constant2:
                    pass
                else:
                    multi_line_comment = True
                    filtered = filtered[:-1] + " "
        elif curr == "/":
            if prev == "*":
                if multi_line_comment:
                    multi_line_comment = False
                    curr = " "
            elif prev == "/":
                if one_line_comment or string_constant2 or string_constant1 or multi_line_comment:
                    pass
                else:
                    one_line_comment = True
                    filtered = filtered[:-1] + " "
        elif curr == "\"":
            if one_line_comment or multi_line_comment or string_constant2:
                pass
            else:
                string_constant1 = not string_constant1
                if not string_constant1:
                    curr = " "
        elif curr == "'":
            if one_line_comment or multi_line_comment or string_constant1:
                pass
            else:
                string_constant2 = not string_constant2
                if string_constant2:
                    curr = " "
        prev = curr
        if multi_line_comment or one_line_comment or string_constant1 or string_constant2:
            filtered += " "
        else:
            filtered += prev

    source_txt = filtered

    for comment in re.findall("\/\*.+?\*\/", source_txt.replace("\n", "<NNNNNNNN>")):
        comment = comment.replace("<NNNNNNNN>", "\n")
        print comment
        print "----"
        print orig
        exit()

    for comment in re.findall("\/\/.+", source_txt):
        print comment
        print "----"
        print orig
        exit()

    if orig_source_len != len(source_txt):
        print "FUCKUPPPPPPPP", orig_source_len, len(source_txt)

    return source_txt


def get_line_offsets(source):
    line_offsets = [len(line) + 1 for line in source.split("\n")]
    for index in xrange(1, len(line_offsets)):
        line_offsets[index] += line_offsets[index - 1]
    line_offsets = [0] + line_offsets
    return line_offsets


def remove_interfaces(sample):
    interface_openned = False
    depth = 0
    filtered = ""
    for pos in xrange(len(sample)):
        if sample[pos] == "@":
            if not interface_openned:
                interface_openned = True
                depth = 0
        elif sample[pos] == "\n":
            if depth == 0:
                interface_openned = False
        elif interface_openned:
            if sample[pos] in "{(":
                depth += 1
            elif sample[pos] in ")}":
                depth -= 1
        if not interface_openned:
            filtered += sample[pos]
        else:
            filtered += " "
    return filtered

def a_in_b(a, b):
    return a[0] >= b[0] and a[1] <= b[1]


def FromString2Node(string):
    nodes = []
    for chunk in string.split("|||"):
        chunk = chunk.strip()
        if not chunk:
            continue
        start, end, labels = chunk.split("<>")
        start, end = int(start), int(end)
        labels = set([label for label in labels.split("|") if label])
        nodes.append(TNode(start, end, labels))
    abs_start = min([node.start for node in nodes])
    abs_end = max([node.end for node in nodes])
    root = [node for node in nodes if node.start  == abs_start and node.end == abs_end][0]
    nodes = [node for node in nodes if node != root]
    nodes = sorted(nodes, key=lambda node : (node.start, -node.end + node.start,))
    stack = [root]
    for node in nodes:
        while node.start >= stack[-1].end:
            stack.pop()
        stack[-1].children.append(node)
        stack.append(node)
    return root


class TNode:
    def __init__(self, start, end, labels):
        self.start = start
        self.end = end
        self.labels = set(labels)
        self.children = []

    def ToString(self):
        output = str(self.start) + "<>" + str(self.end) + "<>" + "|".join(self.labels) + "|||"
        for child in self.children:
            output += child.ToString()
        return output



    def size(self):
        return 1 + sum(child.size() for child in self.children)

    def DFS(self, stack, func):
        stack.append(self)
        #print len(stack),
        func(stack)
        for child in self.children:
            child.DFS(stack, func)
        stack.pop()

    def DFS1(self, stack, func):
        stack.append(self)
        #print len(stack),
        go_deeper = func(stack)
        if go_deeper:
            for child in self.children:
                child.DFS1(stack, func)
        stack.pop()

    def get_snippet(self, source):
        return source[self.start:self.end]


def build_path(node, root):
    path = [root]
    while path[-1] != node:
        matched = False
        for child in path[-1].children:
            if child.start <= node.start and child.end >= node.end:
                path.append(child)
                matched = True
                break
        if not matched:
            raise Exception("build_path", "node is not in root subtree")
    return path


def all_nodes(node):
    layer = [node]
    while layer:
        new_layer = []
        for node in layer:
            new_layer += node.children
            yield node
        layer = new_layer

def all_nodes_post_order(node):
    stack = []
    while node or stack:
        if node:
            stack.append(node)
            node = node.children and node.children[0] or None
            continue
        node = stack.pop()
        yield node
        if stack:
            for child_index in xrange(len(stack[-1].children)):
                if stack[-1].children[child_index] == node:
                    node = child_index + 1 < len(stack[-1].children) and stack[-1].children[child_index + 1] or None
                    break
        else:
            break



def markup2tree(markup):
    used = set()
    root = TNode(0, 1000000, set())
    stack = [root]
    intervals = markup.keys()
    intervals = sorted(intervals, key=lambda interval : (interval[0], -interval[1]+interval[0],))
    for interval in intervals:
        while interval[0] >= stack[-1].end:
            stack.pop()
        node = TNode(interval[0], interval[1], set(markup[interval]))
        stack[-1].children.append(node)
        stack.append(node)
    if root.size() != len(markup) + 1:
        print "FUCKUP", root.size(), len(markup)
        exit()
    return root


sample__ = """
/**
 * <p>
 * A {@link RawComparator} that uses a {@link Deserializer} to deserialize
 * the objects to be compared so that the standard {@link Comparator} can
 * be used to compare them.
 * </p>
 * <p>
 * One may optimize compare-intensive operations by using a custom
 * implementation of {@link RawComparator} that operates directly
 * on byte representations.
 * </p>
 * @param <T>
 */
@InterfaceAudience.LimitedPrivate({"HDFS", "MapReduce"})
@InterfaceStability.Evolving
@interface ClassPreamble {
   String author();
   String date();
   int currentRevision() default 1;
   String lastModified() default "N/A";
   String lastModifiedBy() default "N/A";
   // Note use of array
   String[] reviewers();
}

public abstract class DeserializerComparator<T> implements RawComparator<T> {

  private InputBuffer buffer = new InputBuffer();
  private Deserializer<T> deserializer;

  private T key1;
  private T key2;
"""

#print remove_interfaces(remove_comments(sample__))

