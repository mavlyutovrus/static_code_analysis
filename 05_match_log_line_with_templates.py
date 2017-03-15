

templates = []
for line in open("template_chunks.txt"):
    if line.startswith("TT"):
        fcn, package, chunks = line[:-1].split("\t")[-1].split("||")
        if not chunks:
            continue
        chunks = chunks.split("<:::>")
        template_chunks = [chunk.startswith("__") and chunk[2:].split("___") or chunk for chunk in chunks]
        if "merge conseq strings":
            actual_length = 0
            for chunk_index in xrange(len(template_chunks)):
                if type(template_chunks[chunk_index]) == str and actual_length > 0 and type(template_chunks[actual_length - 1]) == str:
                    template_chunks[actual_length - 1] += template_chunks[chunk_index]
                else:
                    template_chunks[actual_length] = template_chunks[chunk_index]
                    actual_length += 1
            template_chunks = template_chunks[:actual_length]
        if "remove placeholders":
            chunk_index = 0
            while chunk_index < len(template_chunks):
                chunk = template_chunks[chunk_index]
                if type(chunk) == str and "{}" in chunk:
                    prefix = chunk[:chunk.find("{}")]
                    suffix = chunk[chunk.find("{}") + 2:]
                    template_chunks[chunk_index] = prefix
                    template_chunks = template_chunks[:chunk_index + 2] + [suffix] + template_chunks[chunk_index + 2:]
                chunk_index += 1
        static_length = 0
        for chunk in template_chunks:
            if type(chunk) == str:
                static_length += len(chunk)
        if static_length > 10:
            templates += [(fcn, package, template_chunks)]

processed = 0
total_matched = 0
for line in open("feb_2016_sorted_by_time.txt"):
    time1, time2, text = line[:-1].split("||")
    if " org.apache.zookeeper" in text:
        continue
    if "INFO FSNamesystem.audit: allowed=" in text:
        continue
    if "INFO org.apache.hadoop.hdfs.server.datanode.DataNode.clienttrace" in text:
        continue
    if "INFO org.apache.hadoop.hdfs.StateChange: BLOCK* allocateBlock: " in text:
        continue
    if "INFO org.apache.hadoop.hdfs.server.namenode.FSEditLog: Number of transactions" in text:
        continue
    processed += 1
    if processed % 1000 == 0:
        print "..", processed, total_matched


    possible_matches = []
    for fcn, package, template_chunks in templates:
        matched = True
        for chunk in template_chunks:
            if type(chunk) == str:
                if not chunk in text:
                    matched = False
                    break
        if matched:
            possible_matches += [(fcn, package, template_chunks)]

    matched_templates = []
    for fcn, package, template_chunks in possible_matches:
        matched = True
        matched_elements = []
        abs_start  = text.find(":") + 1
        start = abs_start
        elements2match = []
        for chunk in template_chunks:
            if type(chunk) != str:
                elements2match.append(chunk)
                continue
            pos = text.find(chunk, start)
            if pos < start:
                matched = False
                break
            if len(elements2match) > 0:
                matched_elements += [ (elements2match[0], text[start:pos] ) ]
                elements2match = []
            elif pos > start and start > abs_start:
                print "FUCKUP", [chunk], start, pos, text[start:pos]
                print template_chunks
                matched = False
                break
            matched_elements += [chunk]
            #print chunk, pos, text
            start = pos + len(chunk)
        if matched:
            if elements2match:
                if start < len(text):
                    matched_elements += [(elements2match[0], text[start:])]
                else:
                    matched = False
            elif start < len(text):
                matched = False
        if matched:
            #print "cool"
            matched_templates += [(fcn, package, template_chunks, matched_elements)]
    if not matched_templates:
        print text
        for possible in possible_matches:
            print "\t\t", possible[2]
        pass
    else:
        #print text
        #for fcn, package, template_chunks, matched_elements in matched_templates:
        #    print "\t", matched_elements
        pass
    #else:
    #    print "cool"
    """
    if len(matched_templates) > 1:
        print text
        for fcn, package, template_chunks in matched_templates:
            print "\t", template_chunks
        #print [chunk in text for chunk in check]
    if matched_templates:
        total_matched += 1
    """




