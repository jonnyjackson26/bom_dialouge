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
    unfinishedDialouge=None
    verse=1
    chapter=1 #need to think about if i want to start with 0 or 1
    for line in file:
        if "[" in line and "]" in line:
            verse = line[line.index("[") + 1:line.index("]")] #gets the number between the []
        elif line == "\n":
            chapter += .5 # bc theres two blank lines before each new chapter

        if ">" in line and "<" in line: 
            if unfinishedDialouge!=None and f"</{unfinishedDialouge.who}>" in line: #the end of a multi-versed quote (that was opened previously)
                unfinishedDialouge.end_verse=verse
                unfinishedDialouge.end_word=len(line[:line.index(f"</{unfinishedDialouge.who}>")].split())-1
                dialouge.append(unfinishedDialouge)
                unfinishedDialouge=None

                
            who=line[line.index("<")+1:line.index(">")]
            if f"</{who}>" in line:
                startWord=len(line[:line.index("<")].split())-1 #tells how many words (seperated by " ") are before the first index of "<"
                endWord=len(line[:line.index("</")].split())-1
                dialouge.append(Dialogue(who,bookIndex,chapter,verse,verse,startWord,endWord))
            else: #the quote is multi-versed lol like spans over more than just one verse
                startWord=len(line[:line.index("<")].split())-1
                unfinishedDialouge=Dialogue(who,bookIndex,chapter,verse,None,startWord,None)

            #two dialouges in one verse
            lineWithoutWhoTag=line.replace(f"</{who}>",'').replace(f"<{who}>",'')
            if ("<" in lineWithoutWhoTag) and ( ">" in lineWithoutWhoTag):
                who=lineWithoutWhoTag[lineWithoutWhoTag.index("<")+1:lineWithoutWhoTag.index(">")]
                if who[0:1]=="/":
                    pass #probably something with nested dialouge
                else:
                    print(f"{who} has a multi dialouge verse in {chapter}:{verse}")
                    if f"</{who}>" in lineWithoutWhoTag:
                        startWord=len(lineWithoutWhoTag[:lineWithoutWhoTag.index("<")].split())-1 #tells how many words (seperated by " ") are before the first index of "<"
                        endWord=len(lineWithoutWhoTag[:lineWithoutWhoTag.index("</")].split())-1
                        dialouge.append(Dialogue(who,bookIndex,chapter,verse,verse,startWord,endWord))
                    else: #the quote is multi-versed lol like spans over more than just one verse
                        startWord=len(lineWithoutWhoTag[:lineWithoutWhoTag.index("<")].split())-1
                        unfinishedDialouge=Dialogue(who,bookIndex,chapter,verse,None,startWord,None)
                

for d in dialouge:
    d.who=d.who.lower()

writeToDialougeFile()


