import sys
import pdb

def MakeDocumentQs(document):
    read_file = open(document, 'r')
    write_file = open("PenDocQs.test", 'w') 

    for line in read_file:
        if len(line) > 1:
            write_file.write(line[:-2])
            write_file.write("?")
            write_file.write("\n") 
        else:
            write_file.write(line)

def MakeDocumentWithFeatures(read_document, write_document):
    read_file = open(read_document, 'r')
    write_file = open(write_document, 'w')

    last_line = '\n'
    line_number = 1
    for line in read_file:
        # pdb.set_trace()
        write_line = ""
        if len(line) > 1:
            line_array = line.split()
            last_line_array = last_line.split()
            write_line = "Word=" + line_array[0] + " "
            write_line += "Pos=" + line_array[1] + " "

            if not len(last_line) > 1:
                write_line += "StartS=t "
            else:
                write_line += "PPos=" + last_line_array[1] + " "
                write_line += "StartS=f "
            
            write_line += line[-2:]
            write_file.write(write_line)

        else:
            write_file.write(line)

        last_line = line
        line_number += 1 

    
if __name__ == '__main__':
    # Create Pen Test Document with ?'s 
    MakeDocumentQs("PenDocComplete.test")

    # Create Doc With Word/ Pos/ PastPos/ Start Sent
    MakeDocumentWithFeatures("PenDoc.dat", "PenDocFeatures.dat")
    MakeDocumentWithFeatures("PenDocQs.test", "PenDocFeatures.test")
      
