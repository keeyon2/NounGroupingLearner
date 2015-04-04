import opennlp.maxent.*;
import opennlp.maxent.io.*;

import java.io.*;
import java.util.regex.PatternSyntaxException;

import opennlp.maxent.BasicEventStream;
import opennlp.maxent.GIS;
import opennlp.maxent.GISModel;
import opennlp.maxent.PlainTextByLineDataStream;
import opennlp.maxent.RealBasicEventStream;
import opennlp.maxent.io.GISModelWriter;
import opennlp.maxent.io.SuffixSensitiveGISModelWriter;
import opennlp.model.AbstractModel;
import opennlp.model.EventStream;
import opennlp.model.OnePassDataIndexer;
import opennlp.model.OnePassRealValueDataIndexer;
import opennlp.perceptron.PerceptronTrainer;
public class MyCreateModel {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		// Training Data
		String dataFileName = "/Users/Keeyon/Documents/workspace/NLPStuff/src/PenDocFeaturesPos.dat";
		
		// Created Model
        String modelFileName = "/Users/Keeyon/Documents/workspace/NLPStuff/src/PenDocFeaturesPos.txt";
        
        // Test Data to do work on
        String testDataFileName = "/Users/Keeyon/Documents/workspace/NLPStuff/src/Pos.test";
        
        // Paste Results in
        String finishedTagsFileName = "/Users/Keeyon/Documents/workspace/NLPStuff/src/PosResults.test";
        try {
            FileReader datafr = new FileReader(new File(dataFileName));
            EventStream es = new BasicEventStream(new PlainTextByLineDataStream(datafr));
            GISModel model = GIS.trainModel(es, 50000, 4);
            File outputFile = new File(modelFileName);
            GISModelWriter writer = new SuffixSensitiveGISModelWriter(model, outputFile);
            writer.persist();
            
            // Model created and placed here
            GISModel m = (GISModel) new SuffixSensitiveGISModelReader(new File(modelFileName)).getModel();
            
            // Read file line by line
            
            BufferedReader br = new BufferedReader(new FileReader(testDataFileName));
            String line = br.readLine();
            PrintWriter out = new PrintWriter(finishedTagsFileName);
            while (line != null) {
            	int length = line.length();
            	if (length > 2)
            	{
            		String addOnFile = line.substring(0, length-2);
                	String[] splitArray = line.split("\\s+");
                	addOnFile += " " + m.getBestOutcome(m.eval(splitArray));
                	out.println(addOnFile);
            	}
            	else
            	{
            		out.println(line);
            	}
            	            	
	            line = br.readLine();
	        }
            
            out.close();
            
            System.out.println("Done");
        } catch (Exception e) {
            System.out.print("Unable to create model due to exception: ");
            System.out.println(e);
        }
	}
	
	public static String readFile(String fileName) throws IOException {
	    BufferedReader br = new BufferedReader(new FileReader(fileName));
	    try {
	        StringBuilder sb = new StringBuilder();
	        String line = br.readLine();

	        while (line != null) {
	            sb.append(line);
	            sb.append("\n");
	            line = br.readLine();
	        }
	        return sb.toString();
	    } finally {
	        br.close();
	    }
	}
}
