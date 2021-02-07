from fpdf import FPDF
import json
import inspect,os
import pprint
import yaml



class PDF(FPDF):
    def header(self):
      pass

    def footer(self):
      pass
    def chapter_title(self, num, label):
        # Arial 12
        self.set_font('Arial', '', 30)
        # Background color
        self.set_fill_color(200, 220, 255)
        # Title
        self.cell(0, 6, 'Chapter %d : %s' % (num, label), 0, 1, 'L', 1)
        # Line break
        self.ln(4)

    def chapter_body(self, name):
        # Read text file
        with open(name, 'rb') as fh:
            txt = fh.read().decode('latin-1')
        # Times 12
        self.set_font('Times', '', 16)
        # Output justified text
        self.multi_cell(50, 5, txt)
        # Output justified text
        self.multi_cell(70, 5, txt)
        # Line break
        self.ln()
        # Mention in italics
        self.set_font('', 'I')
        self.cell(0, 5, '(end of excerpt)')
        self.dashed_line(0, 148, 10, 148, dash_length = 3, space_length = 1)

    def print_chapter(self, num, title, name):
        self.add_page()
        self.chapter_title(num, title)
        self.chapter_body(name)
    def printRecept(self,name):
        pdf.set_margins(15, 5, 5)
        pdf.set_auto_page_break(True , 5)
        self.add_page()        
        self.set_font('Arial', '', 16)
        # Background color
        self.set_fill_color(200, 220, 255)
        # Title
        self.cell(0, 10, '  %s' % (name), 0, 1, 'L', 1)
        # Line break
        self.ln(4)
    def printMultiLine(self,txt,x,w,lineHigh,justify='L'):
        oldString = ""
        for t in txt.split(' '):
          newString = oldString+t+' ' 
          if(self.get_string_width(newString)>w):
            self.set_x(x)
            self.cell(50, lineHigh, oldString,align=justify,ln=2)
            self.ln()
            #print(oldString)
            oldString = t+' '
            newString = oldString
          else:
            oldString = newString
        if(oldString == newString):
          self.set_x(x)
          self.cell(50, lineHigh, oldString,align='L',ln=2)
          #self.ln()
          
    def printIngredients(self,ingredients):
        self.set_xy(70,18)
        self.set_font('Arial', '', 14)
        allIns=""
        for i in ingredients:
          self.printMultiLine(i,22,66,3.5)
          self.ln(5)
    def printInstructions(self,instructions):
        self.set_xy(15,18)
        self.set_font('Arial', '', 14)
        # Output justified text
        for i in instructions:
          self.printMultiLine(i,90,100,3.5,justify='L')
          self.ln(5)

path = (os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
with open(path+'/rezepte.yaml') as f:
  dataMap = yaml.safe_load(f)

title = ''
pdf = PDF('P', 'mm','A4')
pdf.set_title(title)


for root, dirs, files in os.walk(dataMap['rezepte']['inputDir']):
    for rezept in files:
        print(rezept)
        if rezept.endswith((".json")):
          print(rezept)
          with open(root + os.sep + rezept, 'r') as myfile:
              data=json.load(myfile)
              #pprint.pprint(data.keys())
              
              print(data["name"])
              pprint.pprint(data["recipeIngredient"])

          pdf.printRecept(data["name"])
          pdf.printIngredients(data["recipeIngredient"])
          pdf.printInstructions(data["recipeInstructions"])
          pdf.line(0,148,20,148)
          #print(type(data["recipeInstructions"]))

pdf.output(dataMap['rezepte']['outputFile'], 'F')

