from builtins import object
import re
import logging

class crItem(object):
    
    def is_break(self,line):
        for pat in self.parent.item_breakers:
            if re.match(pat,line):
                return True

    def is_skip(self,line):
        for pat in self.parent.skip_items:
            if re.match(pat,line):
                return True

    def item_builder(self):
        parent = self.parent
        if parent.lines_remaining == False:
            logging.info("Reached end of document.")
            return
        item_types = parent.item_types
        content = [parent.cur_line]
        # What is this line
        for kind,params in list(item_types.items()):
            for pat in params['patterns']:
                amatch = re.match(pat,parent.cur_line)
                if amatch:
                    self.item['kind'] = kind
                    #if params['special_case']:
                    #    self.item['flag'] = params['condition']
                    #else:
                    #    self.item['flag'] = False
                    if params['speaker_re']:
                        them = amatch.group(params['speaker_group'])
                        self.item['speaker'] = them
                        if them in list(self.parent.speakers.keys()):
                            self.item['speaker_bioguide'] = \
                              self.parent.speakers[them]['bioguideid']
                        else:
                            self.item['speaker_bioguide'] = None
                    else:
                        self.item['speaker'] = params['speaker']
                        self.item['speaker_bioguide'] = None
                    break
            if amatch:
                break
        # OK so now put everything else in with it
        # that doesn't interrupt an item
        # conditional logic for edge cases goes here.
        #if self.item['flag'] == 'emptystr':
        #    pass
        #else:
        for line in parent.the_text:
            if self.is_break(line):
                break
            elif self.is_skip(line):
                pass
            else:
                content.append(line)
        # The original text was split on newline, so ...
        item_text = '\n'.join(content)
        self.item['text'] = item_text
        
                    
            
    def __init__(self,parent):
        self.item = { 'kind':'Unknown',
             'speaker':'Unknown',
             'text':None,
             'turn':-1
           }

        self.parent = parent
        self.item_builder()
        # self.item['text'] = self.find_items(contentiter)
