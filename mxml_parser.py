import xml.sax
from collections import defaultdict
import json

class ScoreHander(xml.sax.ContentHandler):
    def __init__(self):
        self.parts = []
        self.note_count = defaultdict(int)
        self.current_note = Note()
        self.empty_elements = ('\n','          ','      ','        ','    ','  ')
        self.composer = None
        self.title = None
        return 

    def strip_empty(self, list):
        for element in self.empty_elements:
            if element in list:
                list.remove(element)

    def startElement(self,tag,attrs):
        self.current = tag

    def characters(self, content):
        if self.current == "part-name":
            part = content
            self.parts.append(part)
            self.strip_empty(self.parts)
        if self.current == "step":
            pitch = content
            if pitch not in self.empty_elements:
                self.current_note.set_pitch(pitch)
        if self.current == "octave":
            octave = content
            if octave not in self.empty_elements:
                self.current_note.set_octave(octave)
                note_tuple = (self.current_note.pitch,self.current_note.octave)
                self.note_count[note_tuple] += 1
        if self.current == "creator":
            composer = content
            if composer not in self.empty_elements:
                self.composer = composer
        if self.current == "work-title":
            title = content
            if title not in self.empty_elements:
                self.title = title

    def endElement(self, tag):
        return

class Note():
    def __init__(self):
        self.pitch = None
        self.octave = None
        return

    def set_pitch(self, pitch):
        self.pitch = pitch 
        return

    def set_octave(self, octave):
        self.octave = octave
        return

    def __str__(self):
        return "This note is " + self.pitch + str(self.octave)

    def __repr__(self):
        return f'{self.pitch}{self.octave}'

class Score():
    def __init__(self, **kwargs): 
        self.title = kwargs['title'] if 'title' in kwargs else None
        self.composer = kwargs['composer'] if 'composer' in kwargs else None
        self.parts = kwargs['parts'] if 'parts' in kwargs else None
        self.pitch_list = kwargs['pitches'] if 'pitches' in kwargs else None

    def remove_pitch_list_tuples(self):
        pitch_list_dict = {}
        for pitch_tuple in self.pitch_list:
            pitch = str(pitch_tuple[0]) + str(pitch_tuple[1])
            count = self.pitch_list[pitch_tuple]
            pitch_list_dict[pitch] = count
        self.pitch_list = pitch_list_dict

    def get_json(self):
        dictionary = self.get_dict()
        json_data = json.dumps(dictionary, indent=4)
        return json_data

    def get_dict(self):
        attr_dict = {}
        attr_dict['title'] = self.title
        attr_dict['composer'] = self.composer
        attr_dict['parts'] = self.parts
        if type(self.pitch_list) == defaultdict:
            self.remove_pitch_list_tuples()
        attr_dict['pitches'] = self.pitch_list
        return attr_dict

    def __str__(self):
        return f'{self.title} was composed by {self.composer}'

def parse_score(mxml_file):
    handler = ScoreHander()
    parser = xml.sax.make_parser()
    parser.setContentHandler(handler)
    parser.parse(mxml_file)
    return Score(parts=handler.parts, pitches=handler.note_count, composer=handler.composer, title=handler.title)

def parse_many_scores(file_list):
    score_dict = {}
    for file in file_list:
        score = parse_score(file)
        score_dict[score] = score
    return score_dict

#test_score = parse_score('test.musicxml')
#test_json = test_score.get_json()
#print(test_json)