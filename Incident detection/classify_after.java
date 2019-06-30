/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package javaapplication5;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;
import java.util.Map;
import java.util.Set;
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
public class classify_after {
    public static void main(String[] args) throws IOException, ParseException {
        String index="E:\\Stream\\After\\Data\\Test\\tornado_index";
        String temp=new String();
        IndexReader reader = DirectoryReader.open(FSDirectory.open(Paths.get(index)));
        IndexSearcher searcher = new IndexSearcher(reader);
        Analyzer analyzer = new StandardAnalyzer();
        QueryParser parser = new QueryParser("contents", analyzer);
        
        
        String [] queries={"serial terrorist terror bomb blast explos explod attack",
                           "earthquak quak magnitud shock tremor",
                           "heavi rain cyclon flood drown water level bank river sea ocean",
                           "shoot shot shooter mass massacr fire gun",
                           "typhoon tornado wind rain storm insid",
                           "fir fire forest burn wildfir bushfir burnt"
                            };
        String [] categories={"Bombing",
                               "Earthquake",
                               "Flood",
                               "Shooting",
                               "Tornado",
                               "Wildfire"};
        Query [] q = new Query [queries.length];
        for (int i=0;i<queries.length; ++i){
            q[i]=parser.parse(queries[i]);
        }
        
        int l=queries.length;
            
        Map <String, double[]> scores = new Hashtable <String, double[]>();
        try{
        FileReader fr=new FileReader("E:\\Stream\\After\\Data\\Test\\tornado_ids");
        BufferedReader br=new BufferedReader(fr);
        
        String line;
        while ((line=br.readLine()) != null){
            double [] arr = new double [l];
            scores.put(line,arr);
            for (int iter=0;iter<l;iter++){
                scores.get(line)[iter]=0.0;
            }
        }
        
        br.close();
        fr.close();
        }
        catch(Exception e){
            System.out.println("Error in reading");
        }
        
        for (int j=0;j<l;j++){
            TopDocs docs = searcher.search(q[j], 50000);
            ScoreDoc[] filterScoreDosArray = docs.scoreDocs;            
            System.out.println(filterScoreDosArray.length+"");
            for (int i = 0; i < filterScoreDosArray.length; ++i) {
                int docId = filterScoreDosArray[i].doc;
                Document d = searcher.doc(docId);
                String p=d.get("path");
                String id=p.substring(p.lastIndexOf("\\")+1);
                System.out.println(j+" "+id);
                scores.get(id)[j]=filterScoreDosArray[i].score;
            }
        }
/*        
       String towrite=new String();
       Set< Map.Entry< String,double []> > st = scores.entrySet();   
       for (Map.Entry< String,double []> me:st){
           String tweet_id=me.getKey();
           towrite+=(tweet_id+"\t\t\t");
           for (int i=0;i<l;i++)
               towrite+=(""+scores.get(tweet_id)[i]+ "\t");
           towrite+="\n";
       }
       towrite=towrite.substring(0, towrite.length()-1);

        FileWriter fw=new FileWriter("E:\\Stream\\TREC IS\\test\\aus_shooting_test");
        try{
        fw.write(towrite);}
        catch(Exception e){
            System.out.println(e+"");
        }
        fw.close();
        
        List <String> done = new ArrayList <String>();
*/

        String out_string=new String();
        Set< Map.Entry< String,double []> > st = scores.entrySet();  
       for (Map.Entry< String,double []> me:st){
           String tweet_id=me.getKey();
           double [] tweet_scores = me.getValue();
           double max_score=-1.0;
           int cat_index=-1;
           for (int i=0;i<l;i++){
               if (tweet_scores[i]>max_score){
                   max_score=tweet_scores[i];
                   cat_index=i;
               }
           }
           if (max_score!=0.0){
               out_string= out_string + tweet_id +'\t'+categories[cat_index]+'\t'+(max_score/13.0)+'\n';
           }
           System.out.println(""+max_score);
       }
        
       FileWriter fw_out=new FileWriter("E:\\Stream\\After\\Data\\Test\\tornado_out");
       fw_out.write(out_string);
       fw_out.close();
       
//        temp=temp.substring(0, temp.length()-1);
        
        
    }
    
     public static double sigmoid(double x) {
    return (1/( 1 + Math.pow(Math.E,(-1*x))));
  }
    
}
