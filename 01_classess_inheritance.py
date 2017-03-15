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


loc = "/home/arslan/src/provenance/hadoop/"


source_files = [(fname.strip(), open(fname.strip()).read()) for fname in open("/home/arslan/src/provenance/hadoop/java_source_files.txt")]
all_classes = []
for fname, orig_source in source_files:
    #if fname != "/home/arslan/src/provenance/hadoop/hadoop-hdfs-project/hadoop-hdfs-client/src/main/java/org/apache/hadoop/hdfs/inotify/Event.java":
    #    continue
    source = [line.strip() for line in orig_source.split("\n") if line.strip()]
    package = [line.split(" ")[-1].replace(";", "") for line in source if line.startswith("package ")]
    if not package:
        print "NO PACKAGE:", fname
        continue
    package = package[0]

    imports = [item.replace("|", "").strip() for item in \
                        re.findall("\|import\s+([^;]+)", "|" + "|".join(source) + "|")]

    #source_txt = "\n".join([line for line in source ])
    source_txt_no_comments = remove_comments(orig_source)
    source_txt_no_comments_no_br = source_txt_no_comments.replace("\n", " ")

    headers = []
    for class_def_header in re.findall("(?:final\s+|abstract\s+|private\s+|public\s+|static\s+)*(?:class|enum|interface)\s+[_a-zA-Z][^{};]*{", source_txt_no_comments_no_br):
        headers += [class_def_header]

    def find_bounds(header, source, start = 0):
        left = source.index(header, start)
        open_bracets = 1
        for pos in xrange(left + len(header), len(source)):
            if source[pos] == "{":
                open_bracets += 1
            elif source[pos] == "}":
                open_bracets -= 1
            if open_bracets == 0:
                break
        return (left, pos + 1)

    def get_class_name(class_header):
        return re.findall("(?:class|enum|interface)\s+([_A-Za-z][^\s<>,{}]*)", header)[0]

    def get_extends_implements(class_header):
        header_no_templates = header
        while True:
            upd = re.subn("<[^<>]*>", "", header_no_templates)[0]
            if upd == header_no_templates:
                break
            header_no_templates = upd
        extends = []
        for item in re.findall("(?:extends|implements)\s+((?:[a-zA-Z0-9_.-]+(?:,\s+)*)+)", header_no_templates):
            extends += re.split(",\s+", item.strip())
        uppercase = [item.strip() for item in re.findall(" [A-Z][^\s,]*| java\.[^\s,]*| org.apache[^\s,]*", header_no_templates)]
        return extends

    classes = []
    header_start = 0
    for header in headers:
        class_name = get_class_name(header)
        extends = get_extends_implements(header)
        bounds = find_bounds(header, source_txt_no_comments_no_br, header_start)
        classes += [(class_name, extends, bounds, header)]
        header_start = bounds[0] + 1
        #print classes[-1]

    for cl_index in xrange(len(classes)):
        class_name, extends, bounds, header = classes[cl_index]
        enclosing_classes = []
        for other_cl_index in xrange(len(classes)):
            if other_cl_index == cl_index:
                continue
            other_bounds = classes[other_cl_index][2]
            if other_bounds[0] < bounds[0] and other_bounds[1] > bounds[1]:
                enclosing_classes.append((other_bounds[1] - other_bounds[0], classes[other_cl_index][0]))
        enclosing_classes = sorted(enclosing_classes, key=lambda tuple: -tuple[0])
        full_class_name_in_scope = ".".join(class_name for _, class_name in enclosing_classes)
        full_class_name_in_scope = not full_class_name_in_scope and class_name or full_class_name_in_scope + "." + class_name
        classes[cl_index] = (full_class_name_in_scope, extends, bounds, header)
    cl = [class_name for class_name, _, _, _ in classes if not "." in class_name]
    if len(cl) > 1:
        print cl, fname
        for item in classes:
            print "\t", item
        for line in orig_source:
            if "class " in line:
                print [line]

    for full_class_name_in_scope, extends, bounds, header in classes:
        all_classes += [(package + "." + full_class_name_in_scope, extends, imports, package, bounds, fname)]





fcns = [item[0] for item in all_classes]
freqs = {}
for item in fcns:
    freqs.setdefault(item, 0)
    freqs[item] += 1
for item, freq in freqs.items():
    if freq > 1:
        print item, freq
        for elem in all_classes:
            if elem[0] == item:
                print "\t", elem

fcns = set(fcns)

default_classes = set(["Appendable","AutoCloseable","CharSequence","Cloneable","Comparable","Iterable","Readable",
                       "Runnable","Thread.UncaughtExceptionHandler","Boolean","Byte","Character","Character.Subset",
                       "Character.UnicodeBlock","Class","ClassLoader","ClassValue","Compiler","Double","Enum","Float",
                       "InheritableThreadLocal","Integer","Long","Math","Number","Object","Package","Process",
                       "ProcessBuilder","ProcessBuilder.Redirect","Runtime","RuntimePermission","SecurityManager","Short",
                       "StackTraceElement","StrictMath","String","StringBuffer","StringBuilder","System","Thread",
                       "ThreadGroup","ThreadLocal","Throwable","Void","Character.UnicodeScript","ProcessBuilder.Redirect.Type",
                       "Thread.State","ArithmeticException","ArrayIndexOutOfBoundsException","ArrayStoreException",
                       "ClassCastException","ClassNotFoundException","CloneNotSupportedException","EnumConstantNotPresentException",
                       "Exception","IllegalAccessException","IllegalArgumentException","IllegalMonitorStateException",
                       "IllegalStateException","IllegalThreadStateException","IndexOutOfBoundsException","InstantiationException",
                       "InterruptedException","NegativeArraySizeException","NoSuchFieldException","NoSuchMethodException",
                       "NullPointerException","NumberFormatException","ReflectiveOperationException","RuntimeException",
                       "SecurityException","StringIndexOutOfBoundsException","TypeNotPresentException",
                       "UnsupportedOperationException","AbstractMethodError","AssertionError","BootstrapMethodError",
                       "ClassCircularityError","ClassFormatError","Error","ExceptionInInitializerError","IllegalAccessError",
                       "IncompatibleClassChangeError","InstantiationError","InternalError","LinkageError",
                       "NoClassDefFoundError","NoSuchFieldError","NoSuchMethodError","OutOfMemoryError",
                       "StackOverflowError","ThreadDeath","UnknownError","UnsatisfiedLinkError","UnsupportedClassVersionError",
                       "VerifyError","VirtualMachineError","Deprecated","Override","SafeVarargs","SuppressWarnings"])


java_default_classes = set(["java.util.Collection","java.util.Comparator","java.util.Deque","java.util.Enumeration","java.util.EventListener",\
"java.util.Formattable","java.util.Iterator","java.util.List","java.util.ListIterator","java.util.Map","java.util.Map.Entry",\
"java.util.NavigableMap","java.util.NavigableSet","java.util.Observer","java.util.Queue","java.util.RandomAccess","java.util.Set",\
"java.util.SortedMap","java.util.SortedSet","java.util.AbstractCollection","java.util.AbstractList","java.util.AbstractMap",\
"java.util.AbstractMap.SimpleEntry","java.util.AbstractMap.SimpleImmutableEntry","java.util.AbstractQueue","java.util.AbstractSequentialList",\
"java.util.AbstractSet","java.util.ArrayDeque","java.util.ArrayList","java.util.Arrays","java.util.BitSet","java.util.Calendar",\
"java.util.Collections","java.util.Currency","java.util.Date","java.util.Dictionary","java.util.EventObject","java.util.FormattableFlags",\
"java.util.Formatter","java.util.GregorianCalendar","java.util.HashMap","java.util.HashSet","java.util.Hashtable",\
"java.util.IdentityHashMap","java.util.LinkedHashMap","java.util.LinkedHashSet","java.util.LinkedList","java.util.ListResourceBundle",\
"java.util.Locale","java.util.Locale.Builder","java.util.Objects","java.util.Observable","java.util.PriorityQueue",\
"java.util.Properties","java.util.PropertyPermission","java.util.PropertyResourceBundle","java.util.Random","java.util.ResourceBundle",\
"java.util.ResourceBundle.Control","java.util.Scanner","java.util.ServiceLoader","java.util.SimpleTimeZone","java.util.Stack",\
"java.util.StringTokenizer","java.util.Timer","java.util.TimerTask","java.util.TimeZone","java.util.TreeMap","java.util.TreeSet",\
"java.util.UUID","java.util.Vector","java.util.WeakHashMap","java.util.Locale.Category","java.util.ConcurrentModificationException",\
"java.util.DuplicateFormatFlagsException","java.util.EmptyStackException","java.util.FormatFlagsConversionMismatchException",\
"java.util.FormatterClosedException","java.util.IllegalFormatCodePointException","java.util.IllegalFormatConversionException",\
"java.util.IllegalFormatException","java.util.IllegalFormatFlagsException","java.util.IllegalFormatPrecisionException",\
"java.util.IllegalFormatWidthException","java.util.IllformedLocaleException","java.util.InputMismatchException",\
"java.util.InvalidPropertiesFormatException","java.util.MissingFormatArgumentException","java.util.MissingFormatWidthException",\
"java.util.MissingResourceException","java.util.NoSuchElementException","java.util.TooManyListenersException",\
"java.util.UnknownFormatConversionException","java.util.UnknownFormatFlagsException","java.util.ServiceConfigurationError",\
"java.io.Closeable","java.io.DataInput","java.io.DataOutput","java.io.Externalizable","java.io.FileFilter",\
"java.io.FilenameFilter","java.io.Flushable","java.io.ObjectInput","java.io.ObjectInputValidation","java.io.ObjectOutput",\
"java.io.ObjectStreamConstants","java.io.Serializable","java.io.BufferedInputStream","java.io.BufferedOutputStream",\
"java.io.BufferedReader","java.io.BufferedWriter","java.io.ByteArrayInputStream","java.io.ByteArrayOutputStream",\
"java.io.CharArrayReader","java.io.CharArrayWriter","java.io.Console","java.io.DataInputStream","java.io.DataOutputStream",\
"java.io.File","java.io.FileDescriptor","java.io.FileInputStream","java.io.FileOutputStream","java.io.FilePermission",\
"java.io.FileReader","java.io.FileWriter","java.io.FilterInputStream","java.io.FilterOutputStream","java.io.FilterReader",\
"java.io.FilterWriter","java.io.InputStream","java.io.InputStreamReader","java.io.LineNumberReader",\
"java.io.ObjectInputStream","java.io.ObjectInputStream.GetField","java.io.ObjectOutputStream",\
"java.io.ObjectOutputStream.PutField","java.io.ObjectStreamClass","java.io.ObjectStreamField","java.io.OutputStream",\
"java.io.OutputStreamWriter","java.io.PipedInputStream","java.io.PipedOutputStream","java.io.PipedReader",\
"java.io.PipedWriter","java.io.PrintStream","java.io.PrintWriter","java.io.PushbackInputStream","java.io.PushbackReader",\
"java.io.RandomAccessFile","java.io.Reader","java.io.SequenceInputStream","java.io.SerializablePermission",\
"java.io.StreamTokenizer","java.io.StringReader","java.io.StringWriter","java.io.Writer","java.io.CharConversionException",\
"java.io.EOFException","java.io.FileNotFoundException","java.io.InterruptedIOException","java.io.InvalidClassException",\
"java.io.InvalidObjectException","java.io.IOException","java.io.NotActiveException","java.io.NotSerializableException",\
"java.io.ObjectStreamException","java.io.OptionalDataException","java.io.StreamCorruptedException",\
"java.io.SyncFailedException","java.io.UnsupportedEncodingException","java.io.UTFDataFormatException",\
"java.io.WriteAbortedException","java.io.IOError", \
"java.util.concurrent.ArrayBlockingQueue","java.util.concurrent.ThreadPoolExecutor","java.util.concurrent.TimeUnit"
 ])


external_libs_classes = set(["org.apache.zookeeper.AsyncCallback.StringCallback", "org.apache.zookeeper.AsyncCallback.StatCallback"])



output = open("all_classes_detailed_info1.txt", "w")
count = 0
for fcn, extends, imports, package, bounds, fname in all_classes:
    count += 1
    #print fname, count
    extends_fcns = []
    for extend in extends:
        if extend.startswith("org.") or extend.startswith("javax.") or extend.startswith("java.") or extend.startswith("com."):
            extends_fcns.append(extend)
            continue
        if extend in fcns:
            extends_fcns.append(extend)
            continue
        if (package + "." + extend) in fcns:
            extends_fcns.append(package + "." + extend)
            continue

        if 1:
            selected = []
            for other_fcn in fcns:
                if other_fcn.startswith(package + ".") and other_fcn.endswith("." + extend):
                    selected.append(other_fcn)
            if len(selected) == 1:
                extends_fcns.append(selected[0])
                continue

        if 1:
            package_chunks = package.split(".")
            class_chunks = fcn.split(".")
            matched = False
            for depth in xrange(len(package_chunks), len(class_chunks)):
                hypothesis = ".".join(class_chunks[:depth]) + "." + extend
                if hypothesis in fcns:
                    matched = True
                    extends_fcns.append(hypothesis)
                    break
            if matched:
                continue
        import_matched = False
        for imported in imports:
            if imported == extend or imported.endswith("." + extend) or imported.endswith("." + extend.split(".")[0]):
                extends_fcns.append(imported)
                import_matched = True
                break
            if imported + "." + extend in external_libs_classes:
                extends_fcns.append(imported + "." + extend)
                import_matched = True
                break
            if imported.endswith("*"):
                hypothesis = imported[:-1] + extend
                if hypothesis in fcns or hypothesis in java_default_classes or hypothesis in external_libs_classes:
                    extends_fcns.append(hypothesis)
                    import_matched = True
                    break
            if imported + "." + extend in fcns:
                extends_fcns.append(imported + "." + extend)
                import_matched = True
                break
        if import_matched:
            continue
        if extend in default_classes:
            extends_fcns.append("java.lang." + extend)
            continue

        if 1:
            selected = set()
            for other_fcn in fcns:
                if other_fcn.startswith(package + ".") and other_fcn.endswith("." + extend):
                    selected.add(other_fcn)
            if selected:
                print "GUESSING:", selected
                extends_fcns.append(min(selected))
                continue

        print "FUCKUP", fcn, extend, fname

        #print imports
        #print package
        #for other_fcn in fcns:
        #    if other_fcn.startswith(package) and other_fcn.endswith(extend):
        #        print "> ", other_fcn
        #exit()
    fcn, extends_fcns, imports, package, bounds, fname
    output.write(fcn + "\t" + "|".join(extends_fcns) + "\t" + package + "\t" + str(bounds) + "\t" + fname + "\t" + "|".join(imports) + "\n")



output.close()







