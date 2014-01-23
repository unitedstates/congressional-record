import re

class Regex(object):

    def __init__(self, string):
        self.string = string
        # a list of tuples containing (regex_string, xml_opening_tag)
        self.opentags = []
        self.closetags = []

    def insert_before(self, re_string, tag, group=None):
        # start tags are inserted at the start of a regex match. if group is
        # specified, matched at the beginning of the group instead.
        self.opentags.append((re_string, tag, group))

    def insert_after(self, re_string, tag, group=None):
        # start tags are inserted at the start of a regex match. if group is
        # specified, matched at the end of the group instead.
        self.closetags.append((re_string, tag, group))


    def apply(self):
        indexes = {}
        # identify where all the opening tags go (those that get inserted at
        # the start of the regex match)
        for regex, tag, group in self.opentags:
            matchobj = re.search(regex, self.string)
            if matchobj:
                if group:
                    start = matchobj.start(group)
                else:
                    start = matchobj.start()
                # the tag for a given position is stored as a list, because
                # there may be more than one tag that goes here. (eg a quote
                # that end at the end of a paragraph).
                if start not in indexes:
                    indexes[start] = []
                indexes[start].append(tag)

        # identify where all the closing tags go (those that get inserted at
        # the end of the regex match)
        for regex, tag, group in self.closetags:
            matchobj = re.search(regex, self.string)
            if matchobj:
                if group:
                    end = matchobj.end(group)
                else:
                    end = matchobj.end()
                # the tag for a given position is stored as a list, because
                # there may be more than one tag that goes here. (eg a quote
                # that end at the end of a paragraph).
                if end not in indexes:
                    indexes[end] = []
                indexes[end].append(tag)

        if len(indexes):
            #print indexes

            # we need to split the string into substrings between each pair of
            # (sorted) indices, eg. at index_n and index_n+1. a substring is
            # also needed from the beginning of the string to the first split
            # index, and from the last split index to the end of the string.
            l = indexes.keys()
            l.sort()
            first_substring = [(0,l[0])]
            last_substring = [(l[-1], len(self.string))]
            pairs = first_substring + [(l[i], l[i+1]) for i in xrange(len(l)-1)] + last_substring

            output = []
            # make sure we don't duplicate any insertions.
            already_matched = []
            for start, stop in pairs:
                substr = self.string[start:stop]
                # is there a tag that goes here?
                if start in indexes.keys() and start not in already_matched:
                    output.append(substr)
                    for tag in indexes[start]:
                        output.append(tag)
                    already_matched.append(start)
                elif stop in indexes.keys() and stop not in already_matched:
                    output.append(substr)
                    for tag in indexes[stop]:
                        output.append(tag)
                    already_matched.append(stop)
                else:
                    output.append(substr)
            # now join the pieces of the output string back together
            outputstring = ''.join(output)
            return outputstring
        else:
            # if there were no matches, return the string unchanged.
            return self.string
