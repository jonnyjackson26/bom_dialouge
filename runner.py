class Dialogue:
    def __init__(self, who, book_index, chapter_index, start_verse, end_verse, start_word, end_word):
        self.who = who
        self.book_index = book_index
        self.chapter_index = chapter_index
        self.start_verse = start_verse
        self.end_verse = end_verse
        self.start_word = start_word
        self.end_word = end_word

    def toString(self):
        return f"{self.who} @ book {self.book_index}, {self.chapter_index}:{self.start_verse} from words {self.start_word} to {self.end_word}"

    def to_js_string(self):
        return f'new Dialogue("{self.who}", {self.book_index}, {self.chapter_index}, {self.start_verse}, {self.end_verse}, {self.start_word}, {self.end_word})'



def writeToDialougeFile():
    with open("dialogue.js", "w") as js_file:
        js_file.write("const dialogue = [\n")
        for d in dialouge:
            js_file.write("    " + d.to_js_string() + ",\n")
        js_file.write("];\n")

dialouge=[]

bookIndex=0
path="1-nephi.txt"
with open(path, "r") as file:
    verse=1
    chapter=1 #need to think about if i want to start with 0 or 1
    for line in file:
        if "[" in line and "]" in line:
            verse = line[line.index("[") + 1:line.index("]")] #gets the number between the []
        elif line == "\n":
            chapter += .5 # bc theres two blank lines before each new chapter

        if ">" in line and "<" in line: 
            who=line[line.index("<")+1:line.index(">")]
            if f"</{who}>" in line:
                startWord=len(line[:line.index("<")].split())-1 #tells how many words (seperated by " ") are before the first index of "<"
                endWord=len(line[:line.index("</")].split())-1
                dialouge.append(Dialogue(who.lower(),bookIndex,chapter,verse,verse,startWord,endWord))

for d in dialouge:
    print(d.toString())

writeToDialougeFile()


