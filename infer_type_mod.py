default_classes = set(["Appendable", "AutoCloseable", "CharSequence", "Cloneable", "Comparable", "Iterable", "Readable",
                       "Runnable", "Thread.UncaughtExceptionHandler", "Boolean", "Byte", "Character",
                       "Character.Subset",
                       "Character.UnicodeBlock", "Class", "ClassLoader", "ClassValue", "Compiler", "Double", "Enum",
                       "Float",
                       "InheritableThreadLocal", "Integer", "Long", "Math", "Number", "Object", "Package", "Process",
                       "ProcessBuilder", "ProcessBuilder.Redirect", "Runtime", "RuntimePermission", "SecurityManager",
                       "Short",
                       "StackTraceElement", "StrictMath", "String", "StringBuffer", "StringBuilder", "System", "Thread",
                       "ThreadGroup", "ThreadLocal", "Throwable", "Void", "Character.UnicodeScript",
                       "ProcessBuilder.Redirect.Type",
                       "Thread.State", "ArithmeticException", "ArrayIndexOutOfBoundsException", "ArrayStoreException",
                       "ClassCastException", "ClassNotFoundException", "CloneNotSupportedException",
                       "EnumConstantNotPresentException",
                       "Exception", "IllegalAccessException", "IllegalArgumentException",
                       "IllegalMonitorStateException",
                       "IllegalStateException", "IllegalThreadStateException", "IndexOutOfBoundsException",
                       "InstantiationException",
                       "InterruptedException", "NegativeArraySizeException", "NoSuchFieldException",
                       "NoSuchMethodException",
                       "NullPointerException", "NumberFormatException", "ReflectiveOperationException",
                       "RuntimeException",
                       "SecurityException", "StringIndexOutOfBoundsException", "TypeNotPresentException",
                       "UnsupportedOperationException", "AbstractMethodError", "AssertionError", "BootstrapMethodError",
                       "ClassCircularityError", "ClassFormatError", "Error", "ExceptionInInitializerError",
                       "IllegalAccessError",
                       "IncompatibleClassChangeError", "InstantiationError", "InternalError", "LinkageError",
                       "NoClassDefFoundError", "NoSuchFieldError", "NoSuchMethodError", "OutOfMemoryError",
                       "StackOverflowError", "ThreadDeath", "UnknownError", "UnsatisfiedLinkError",
                       "UnsupportedClassVersionError",
                       "VerifyError", "VirtualMachineError", "Deprecated", "Override", "SafeVarargs",
                       "SuppressWarnings"])

primitive_types = set(["boolean", "char", "byte", "short", "int", "long", "float", "double"])


java_default_classes = set([
                            "java.util.regex.Pattern",
                            "java.util.Collection", "java.util.Comparator", "java.util.Deque", "java.util.Enumeration",
                            "java.util.EventListener", \
                            "java.util.Formattable", "java.util.Iterator", "java.util.List", "java.util.ListIterator",
                            "java.util.Map", "java.util.Map.Entry", \
                            "java.util.NavigableMap", "java.util.NavigableSet", "java.util.Observer", "java.util.Queue",
                            "java.util.RandomAccess", "java.util.Set", \
                            "java.util.SortedMap", "java.util.SortedSet", "java.util.AbstractCollection",
                            "java.util.AbstractList", "java.util.AbstractMap", \
                            "java.util.AbstractMap.SimpleEntry", "java.util.AbstractMap.SimpleImmutableEntry",
                            "java.util.AbstractQueue", "java.util.AbstractSequentialList", \
                            "java.util.AbstractSet", "java.util.ArrayDeque", "java.util.ArrayList", "java.util.Arrays",
                            "java.util.BitSet", "java.util.Calendar", \
                            "java.util.Collections", "java.util.Currency", "java.util.Date", "java.util.Dictionary",
                            "java.util.EventObject", "java.util.FormattableFlags", \
                            "java.util.Formatter", "java.util.GregorianCalendar", "java.util.HashMap",
                            "java.util.HashSet", "java.util.Hashtable", \
                            "java.util.IdentityHashMap", "java.util.LinkedHashMap", "java.util.LinkedHashSet",
                            "java.util.LinkedList", "java.util.ListResourceBundle", \
                            "java.util.Locale", "java.util.Locale.Builder", "java.util.Objects", "java.util.Observable",
                            "java.util.PriorityQueue", \
                            "java.util.Properties", "java.util.PropertyPermission", "java.util.PropertyResourceBundle",
                            "java.util.Random", "java.util.ResourceBundle", \
                            "java.util.ResourceBundle.Control", "java.util.Scanner", "java.util.ServiceLoader",
                            "java.util.SimpleTimeZone", "java.util.Stack", \
                            "java.util.StringTokenizer", "java.util.Timer", "java.util.TimerTask", "java.util.TimeZone",
                            "java.util.TreeMap", "java.util.TreeSet", \
                            "java.util.UUID", "java.util.Vector", "java.util.WeakHashMap", "java.util.Locale.Category",
                            "java.util.ConcurrentModificationException", \
                            "java.util.DuplicateFormatFlagsException", "java.util.EmptyStackException",
                            "java.util.FormatFlagsConversionMismatchException", \
                            "java.util.FormatterClosedException", "java.util.IllegalFormatCodePointException",
                            "java.util.IllegalFormatConversionException", \
                            "java.util.IllegalFormatException", "java.util.IllegalFormatFlagsException",
                            "java.util.IllegalFormatPrecisionException", \
                            "java.util.IllegalFormatWidthException", "java.util.IllformedLocaleException",
                            "java.util.InputMismatchException", \
                            "java.util.InvalidPropertiesFormatException", "java.util.MissingFormatArgumentException",
                            "java.util.MissingFormatWidthException", \
                            "java.util.MissingResourceException", "java.util.NoSuchElementException",
                            "java.util.TooManyListenersException", \
                            "java.util.UnknownFormatConversionException", "java.util.UnknownFormatFlagsException",
                            "java.util.ServiceConfigurationError", \
                            "java.io.Closeable", "java.io.DataInput", "java.io.DataOutput", "java.io.Externalizable",
                            "java.io.FileFilter", \
                            "java.io.FilenameFilter", "java.io.Flushable", "java.io.ObjectInput",
                            "java.io.ObjectInputValidation", "java.io.ObjectOutput", \
                            "java.io.ObjectStreamConstants", "java.io.Serializable", "java.io.BufferedInputStream",
                            "java.io.BufferedOutputStream", \
                            "java.io.BufferedReader", "java.io.BufferedWriter", "java.io.ByteArrayInputStream",
                            "java.io.ByteArrayOutputStream", \
                            "java.io.CharArrayReader", "java.io.CharArrayWriter", "java.io.Console",
                            "java.io.DataInputStream", "java.io.DataOutputStream", \
                            "java.io.File", "java.io.FileDescriptor", "java.io.FileInputStream",
                            "java.io.FileOutputStream", "java.io.FilePermission", \
                            "java.io.FileReader", "java.io.FileWriter", "java.io.FilterInputStream",
                            "java.io.FilterOutputStream", "java.io.FilterReader", \
                            "java.io.FilterWriter", "java.io.InputStream", "java.io.InputStreamReader",
                            "java.io.LineNumberReader", \
                            "java.io.ObjectInputStream", "java.io.ObjectInputStream.GetField",
                            "java.io.ObjectOutputStream", \
                            "java.io.ObjectOutputStream.PutField", "java.io.ObjectStreamClass",
                            "java.io.ObjectStreamField", "java.io.OutputStream", \
                            "java.io.OutputStreamWriter", "java.io.PipedInputStream", "java.io.PipedOutputStream",
                            "java.io.PipedReader", \
                            "java.io.PipedWriter", "java.io.PrintStream", "java.io.PrintWriter",
                            "java.io.PushbackInputStream", "java.io.PushbackReader", \
                            "java.io.RandomAccessFile", "java.io.Reader", "java.io.SequenceInputStream",
                            "java.io.SerializablePermission", \
                            "java.io.StreamTokenizer", "java.io.StringReader", "java.io.StringWriter", "java.io.Writer",
                            "java.io.CharConversionException", \
                            "java.io.EOFException", "java.io.FileNotFoundException", "java.io.InterruptedIOException",
                            "java.io.InvalidClassException", \
                            "java.io.InvalidObjectException", "java.io.IOException", "java.io.NotActiveException",
                            "java.io.NotSerializableException", \
                            "java.io.ObjectStreamException", "java.io.OptionalDataException",
                            "java.io.StreamCorruptedException", \
                            "java.io.SyncFailedException", "java.io.UnsupportedEncodingException",
                            "java.io.UTFDataFormatException", \
                            "java.io.WriteAbortedException", "java.io.IOError", \
                            "java.util.concurrent.ArrayBlockingQueue", "java.util.concurrent.ThreadPoolExecutor",
                            "java.util.concurrent.TimeUnit",
                            "java.net.ContentHandlerFactory", "java.net.CookiePolicy", "java.net.CookieStore",
                            "java.net.DatagramSocketImplFactory", "java.net.FileNameMap", "java.net.ProtocolFamily",
                            "java.net.SocketImplFactory", "java.net.SocketOption", "java.net.SocketOptions",
                            "java.net.URLStreamHandlerFactory", "java.net.Authenticator", "java.net.CacheRequest",
                            "java.net.CacheResponse", "java.net.ContentHandler", "java.net.CookieHandler",
                            "java.net.CookieManager", "java.net.DatagramPacket", "java.net.DatagramSocket",
                            "java.net.DatagramSocketImpl", "java.net.HttpCookie", "java.net.HttpURLConnection",
                            "java.net.IDN", "java.net.Inet4Address", "java.net.Inet6Address", "java.net.InetAddress",
                            "java.net.InetSocketAddress", "java.net.InterfaceAddress", "java.net.JarURLConnection",
                            "java.net.MulticastSocket", "java.net.NetPermission", "java.net.NetworkInterface",
                            "java.net.PasswordAuthentication", "java.net.Proxy", "java.net.ProxySelector",
                            "java.net.ResponseCache", "java.net.SecureCacheResponse", "java.net.ServerSocket",
                            "java.net.Socket", "java.net.SocketAddress", "java.net.SocketImpl",
                            "java.net.SocketPermission", "java.net.StandardSocketOptions", "java.net.URI",
                            "java.net.URL", "java.net.URLClassLoader", "java.net.URLConnection", "java.net.URLDecoder",
                            "java.net.URLEncoder", "java.net.URLStreamHandler", "java.net.Authenticator.RequestorType",
                            "java.net.Proxy.Type", "java.net.StandardProtocolFamily", "java.net.BindException",
                            "java.net.ConnectException", "java.net.HttpRetryException",
                            "java.net.MalformedURLException", "java.net.NoRouteToHostException",
                            "java.net.PortUnreachableException", "java.net.ProtocolException",
                            "java.net.SocketException", "java.net.SocketTimeoutException",
                            "java.net.UnknownHostException", "java.net.UnknownServiceException",
                            "java.net.URISyntaxException",
    "java.util.concurrent.AbstractExecutorService", "java.util.concurrent.ArrayBlockingQueue",
    "java.util.concurrent.BlockingDeque", "java.util.concurrent.BlockingQueue",
    "java.util.concurrent.BrokenBarrierException", "java.util.concurrent.Callable",
    "java.util.concurrent.CancellationException", "java.util.concurrent.CompletionService",
    "java.util.concurrent.ConcurrentHashMap", "java.util.concurrent.ConcurrentLinkedDeque",
    "java.util.concurrent.ConcurrentLinkedQueue", "java.util.concurrent.ConcurrentMap",
    "java.util.concurrent.ConcurrentNavigableMap", "java.util.concurrent.ConcurrentSkipListMap",
    "java.util.concurrent.ConcurrentSkipListSet", "java.util.concurrent.CopyOnWriteArrayList",
    "java.util.concurrent.CopyOnWriteArraySet", "java.util.concurrent.CountDownLatch",
    "java.util.concurrent.CyclicBarrier", "java.util.concurrent.Delayed", "java.util.concurrent.Exchanger",
    "java.util.concurrent.ExecutionException", "java.util.concurrent.Executor",
    "java.util.concurrent.ExecutorCompletionService", "java.util.concurrent.ExecutorService",
    "java.util.concurrent.Executors", "java.util.concurrent.ForkJoinPool",
    "java.util.concurrent.ForkJoinPool.ForkJoinWorkerThreadFactory", "java.util.concurrent.ForkJoinPool.ManagedBlocker",
    "java.util.concurrent.ForkJoinTask", "java.util.concurrent.ForkJoinWorkerThread", "java.util.concurrent.Future",
    "java.util.concurrent.FutureTask", "java.util.concurrent.LinkedBlockingDeque",
    "java.util.concurrent.LinkedBlockingQueue", "java.util.concurrent.LinkedTransferQueue",
    "java.util.concurrent.Phaser", "java.util.concurrent.PriorityBlockingQueue", "java.util.concurrent.RecursiveAction",
    "java.util.concurrent.RecursiveTask", "java.util.concurrent.RejectedExecutionException",
    "java.util.concurrent.RejectedExecutionHandler", "java.util.concurrent.RunnableFuture",
    "java.util.concurrent.RunnableScheduledFuture", "java.util.concurrent.ScheduledExecutorService",
    "java.util.concurrent.ScheduledFuture", "java.util.concurrent.ScheduledThreadPoolExecutor",
    "java.util.concurrent.Semaphore", "java.util.concurrent.SynchronousQueue", "java.util.concurrent.ThreadFactory",
    "java.util.concurrent.ThreadLocalRandom", "java.util.concurrent.ThreadPoolExecutor",
    "java.util.concurrent.ThreadPoolExecutor.AbortPolicy", "java.util.concurrent.ThreadPoolExecutor.CallerRunsPolicy",
    "java.util.concurrent.ThreadPoolExecutor.DiscardOldestPolicy",
    "java.util.concurrent.ThreadPoolExecutor.DiscardPolicy", "java.util.concurrent.TimeUnit",
    "java.util.concurrent.TimeoutException", "java.util.concurrent.TransferQueue",
    "Pack200.Packer", "Pack200.Unpacker", "Attributes", "Attributes.Name", "JarEntry", "JarFile", "JarInputStream",
    "JarOutputStream", "Manifest", "Pack200", "JarException"
                            ])

external_libs_classes = set(["org.apache.zookeeper.AsyncCallback.StringCallback", "org.apache.zookeeper.AsyncCallback.StatCallback"])

def resolve_type(type_name, fcn, extents, package, first, last, fname, imports, type_params, fcn_dict):
    if type_name in type_params:
        return type_name

    if type_name.startswith("org.") or type_name.startswith("javax.") or type_name.startswith("java.") or type_name.startswith("com."):
        return type_name

    if type_name in primitive_types:
        return type_name


    if type_name in fcn_dict:
        return type_name

    hypothesis = fcn + "." + type_name
    if hypothesis in fcn_dict:
        return hypothesis

    hypothesis = package + "." + type_name
    #print "HYPO:", hypothesis, hypothesis in fcn_dict
    if hypothesis in fcn_dict:
        return hypothesis

    if 1:
        selected = []
        for other_fcn in fcn_dict.keys():
            if other_fcn.startswith(package + ".") and other_fcn.endswith("." + type_name):
                selected.append(other_fcn)
        if len(selected) == 1:
            return selected[0]

    if 1:
        package_chunks = package.split(".")
        class_chunks = fcn.split(".")
        selected = []
        for depth in xrange(len(package_chunks), len(class_chunks)):
            hypothesis = ".".join(class_chunks[:depth]) + "." + type_name
            if hypothesis in fcn_dict:
                selected.append(hypothesis)
            parent_class_hypothesis = ".".join(class_chunks[:depth])
            #TODO it was 7 in another module!!!!!!!
            #if parent_class_hypothesis in fcn_dict and type_name in fcn_dict[parent_class_hypothesis][7]:
            if parent_class_hypothesis in fcn_dict and type_name in fcn_dict[parent_class_hypothesis][6]:
                return type_name
        if len(selected) == 1:
            return selected[0]

    for imported in imports:
        if imported == type_name or imported.endswith("." + type_name):
            return imported
        if imported.endswith("." + type_name.split(".")[0]):
            return imported + "." + ".".join(type_name.split(".")[1:])
        if imported + "." + type_name in external_libs_classes:
            return imported + "." + type_name
        if imported.endswith("*"):
            hypothesis = imported[:-1] + type_name
            if hypothesis in fcn_dict or hypothesis in java_default_classes or hypothesis in external_libs_classes:
                return hypothesis
        if imported + "." + type_name in fcn_dict:
            return imported + "." + type_name

    for extent in extents:
        if extent + "." + type_name in fcn_dict:
            return extent + "." + type_name

    if type_name in default_classes:
        return type_name

    return None