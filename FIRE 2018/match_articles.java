/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package javaapplication5;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Paths;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.store.FSDirectory;

/**
 *
 * @author Harshit
 */
public class match_articles {

    public static void main(String[] args) throws IOException, ParseException {
        String index = "E:\\Stream\\FIRE\\index_headlines";
        String tweets_folder = "E:\\Stream\\FIRE\\positive";
        int i, j;
        File folder = new File(tweets_folder);
        File[] listOfFiles = folder.listFiles();
        String matches = new String();
        for (i = 0; i < listOfFiles.length; i++) {
            String query_fname = listOfFiles[i].getPath();
            String temp = new String();
            IndexReader reader = DirectoryReader.open(FSDirectory.open(Paths.get(index)));
            IndexSearcher searcher = new IndexSearcher(reader);
            Analyzer analyzer = new StandardAnalyzer();
            QueryParser parser = new QueryParser("contents", analyzer);
            Query q = null;
            FileReader fr = new FileReader(query_fname);
            BufferedReader br = new BufferedReader(fr);
            String line = br.readLine();
            q = parser.parse(line);
            br.close();
            fr.close();
            TopDocs docs = searcher.search(q, 50000);
            ScoreDoc[] filterScoreDosArray = docs.scoreDocs;

            for (j = 0; j < filterScoreDosArray.length; j++) {
                if (filterScoreDosArray[j].score >= 30.0) {
                    int docId = filterScoreDosArray[j].doc;
                    Document d = searcher.doc(docId);
                    String p = d.get("path");
                    String article_name = p.substring(p.lastIndexOf("\\") + 1);
                    temp = "" + listOfFiles[i].getName() + "\t" + line + "\t" + article_name + "\t" + filterScoreDosArray[j].score + "\n";
                    matches += temp;
                }
            }

            /*       int docId = filterScoreDosArray[0].doc;
        Document d = searcher.doc(docId);
        String p=d.get("path");
        String article_name=p.substring(p.lastIndexOf("\\")+1);        
        if (filterScoreDosArray[0].score>=30.0)
        {   temp=""+listOfFiles[i].getName()+"\t"+line+"\t"+article_name+"\t"+filterScoreDosArray[0].score+"\n";
            matches+=temp;}
         
             */
        }
        FileWriter fw = new FileWriter("E:\\Stream\\FIRE\\news_match_output.txt");
        fw.write(matches);
        fw.close();
        System.out.println("" + matches);

//        temp=temp.substring(0, temp.length()-1);
    }

    public static double sigmoid(double x) {
        return (1 / (1 + Math.pow(Math.E, (-1 * x))));
    }

}
