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

def MakeDocumentNoQs(document, writeDoc):
    read_file = open(document, 'r')
    write_file = open(writeDoc, 'w') 

    for line in read_file:
        if len(line) > 1:
            write_file.write(line[:-2])
            # write_file.write("?")
            write_file.write("\n") 
        else:
            write_file.write(line)

def MakeDocumentWithFeatures(read_document, write_document):
    read_file = open(read_document, 'r')
    write_file = open(write_document, 'w')

    last_line = '\n'
    line_number = 1
    for line in read_file:
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

def CompareDocuments(correct_doc, comparing_doc):
    total_tags = 0.0
    correct_tags = 0.0
    current_correct_group = ""
    current_comparing_group = ""
    previous_correct_tag = ""
    previous_comparing_tag = ""
    correct_file = open(correct_doc, 'r')
    comparing_file = open(comparing_doc, 'r')
    same_groups = 0
    correct_file_groups = 0
    comparing_file_groups = 0

    for line_i,line_j in zip(correct_file, comparing_file):
        if len(line_i) > 1:
            total_tags += 1

            # Add to Each Group Text if I
            if (line_i[-2] == "I"):
                current_correct_group += line_i[-2]
            if (line_j[-2] == "I"):
                current_comparing_group += line_j[-2]
            
            # Establish Group number if Not I and prev I
            if not (line_j[-2] == "I"):
                if previous_comparing_tag == "I":
                    comparing_file_groups += 1

            if not (line_i[-2] == "I"):
                if previous_correct_tag == "I":
                    correct_file_groups += 1
                    # Check if previous I
                    if current_comparing_group == current_correct_group:
                        same_groups += 1

            # Reset Current Group if not I
            if (line_i[-2] == "B"):
                current_correct_group = line_i[-2]
            elif (line_i[-2] == "O"):
                current_correct_group = ""

            if (line_j[-2] == "B"):
                current_comparing_group = line_i[-2]
            elif (line_j[-2] == "O"):
                current_comparing_group = ""


            # For Accuracy Tag
            if (line_i[-2] == line_j[-2]):
                correct_tags += 1

            previous_correct_tag = line_i[-2]
            previous_comparing_tag = line_j[-2]

    accuracy = (correct_tags/total_tags) * 100.00
    NPPrec = float(same_groups) / float(comparing_file_groups)
    Recall = float(same_groups) / float(correct_file_groups)
    FMeasure = 2 * ((NPPrec * Recall)/(NPPrec + Recall))

    print "Total Tags: " + str(total_tags)
    print "Correct Tags: " + str(correct_tags)
    print ""
    print "Accuracy = " + str(accuracy)
    print ""
    print "Total Key Groups: " + str(correct_file_groups)
    print "Total Created Groups: " + str(comparing_file_groups)
    print "Total Same Groups: " + str(same_groups)
    print ""
    print "Prec: " + str(NPPrec)
    print "Recall: " + str(Recall)
    print "FMeasure: " + str(FMeasure)

def MakeInputReadyForJava(java_ready_orig_feat, java_ready_test):
    MakeDocumentWithFeatures("PenDoc.dat", java_ready_orig_feat)
    MakeDocumentWithFeatures("PenDocComplete.test", "deleteme.test")          
    MakeDocumentNoQs("deleteme.test", java_ready_test)


if __name__ == '__main__':
    
    # Create Documents
    #MakeInputReadyForJava("PenDocFeaturesPos.dat", "Pos.test")
    # Compare Documents 
    CompareDocuments("PenDocTrainingComplete.test", "PosResults.test")


