import xml.sax
from collections import defaultdict

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

handler = ScoreHander()
parser = xml.sax.make_parser()
parser.setContentHandler(handler)
parser.parse('cinderella.musicxml')

test_score = Score(parts=handler.parts, pitches=handler.note_count, composer=handler.composer, title=handler.title)