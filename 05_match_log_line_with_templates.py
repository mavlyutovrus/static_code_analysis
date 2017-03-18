
def tokenize(text):
    import re
    return re.findall("[a-zA-Z0-9]+", text)



templates = []
by_longest_chunk = {}
for line in open("template_chunks.txt"):
    if line.startswith("SPS:"):
        fcn, package, chunks = line[line.find("\t") + 1:-1].split("RRRRRRRR")
        if not chunks:
            continue
        chunks = chunks.replace("<TAB>", "\t").replace("<BR>", "\n").split("<>>>>>>>___")
        template_chunks = [(chunk[:chunk.find(":")], chunk[chunk.find(":") + 1:]) for chunk in chunks]
        if "merge conseq strings":
            shortened = [template_chunks[0]]
            for chunk_type, chunk in template_chunks[1:]:
                if chunk_type == "SC" and shortened[-1][0] == "SC":
                    shortened[-1] = ("SC", shortened[-1][1] + chunk)
                else:
                    shortened.append( (chunk_type, chunk) )
            template_chunks = shortened
        static_length = 0
        for chunk_type, chunk in template_chunks:
            if chunk_type == "SC":
                static_length += len(chunk)
        if static_length < 10:
            continue
        longest_chunk = ""
        for chunk_type, chunk in template_chunks:
            if chunk_type == "SC":
                for token in tokenize(chunk):
                    if len(token) > len(longest_chunk):
                        longest_chunk = token
        by_longest_chunk.setdefault(longest_chunk, []).append(len(templates))
        templates += [(fcn, package, template_chunks)]

processed = 0
total_matched = 0


used_templates = set()

for line in open("feb_2016_sorted_by_time.txt"):
    time1, time2, text = line[:-1].split("||")
    if " org.apache.zookeeper" in text:
        continue

    #if "INFO FSNamesystem.audit: allowed=" in text:
    #    continue
    #if "INFO org.apache.hadoop.hdfs.server.datanode.DataNode.clienttrace" in text:
    #    continue
    #if "INFO org.apache.hadoop.hdfs.StateChange: BLOCK* allocateBlock: " in text:
    #    continue
    #if "INFO BlockStateChange: BLOCK* addStoredBlock" in text:
    #    continue
    #if "INFO BlockStateChange: BLOCK* addToInvalidates" in text:
    #    continue
    #if "INFO org.apache.hadoop.hdfs.server.namenode.FSEditLog: Number of transactions" in text:
    #    continue
    processed += 1
    #if processed % 1000 == 0:
    #    print "..", processed, total_matched

    possible_matches = []
    for token in tokenize(text):
        if token in by_longest_chunk:
            possible_matches += by_longest_chunk[token]

    matched_templates = []
    for templ_index in possible_matches:
        fcn, package, template_chunks = templates[templ_index]
        matched = True
        matched_elements = []
        abs_start  = text.find(":") + 1
        start = abs_start
        elements2match = []
        for chunk_type, chunk in template_chunks:
            if chunk_type != "SC":
                elements2match.append(chunk)
                continue
            pos = text.find(chunk, start)
            if pos < start:
                matched = False
                break
            if len(elements2match) > 0:
                matched_elements += [ ([elem for elem in elements2match], text[start:pos] ) ]
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
                    matched_elements += [([elem for elem in elements2match], text[start:])]
                else:
                    matched = False
            elif start < len(text):
                matched = False
        if matched:
            #print "cool"
            matched_templates += [(fcn, package, template_chunks, templ_index, matched_elements)]
    if not matched_templates:
        #print text
        #for possible in possible_matches:
        #    print "\t\t", templates[possible][2]
        #    #print "\t\t", possible[2]
        pass
    else:
        #print text
        for fcn, package, template_chunks, templ_index, matched_elements in matched_templates:
            if templ_index in used_templates:
                continue
            used_templates.add(templ_index)
            key_values = []
            for match in matched_elements:
                if type(match) == tuple:
                    args, value = match
                    if value.strip():
                        key_values.append("||".join(args).replace(":::", "\t") + "\t" + value)
            print "Log line sample [%d]:" % (len(used_templates))
            print text
            print
            print "Extracted elements (type<TAB>var_name<TAB>value):"
            for key_val in key_values:
                print "\t" + key_val
            print "------"
            print

            #print "\t", matched_elements
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




