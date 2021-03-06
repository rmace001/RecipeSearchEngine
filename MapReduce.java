package edu.ucr.cs.cs242.RecipeSearch;

import java.io.IOException;
import java.util.StringTokenizer;

import java.io.File;
import org.apache.commons.io.FileUtils;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.input.FileSplit;

public class MapReduce {

    public static class InvertedIndexNameMapper 
            extends Mapper<Object, Text, Text, Text> {

        private Text nameKey = new Text();
        private Text fileNameValue = new Text();

        @Override
        public void map(Object key, Text value, Context context
                ) throws IOException, InterruptedException {
            String data = value.toString();
            String[] field = data.split(",", -1);
            String firstName = null;
            if (null != field && field.length == 9 && field[0].length() > 0) {
                firstName=field[0];
                String fileName = ((FileSplit) context.getInputSplit()).getPath().getName();
                nameKey.set(firstName);
                fileNameValue.set(fileName);
                context.write(nameKey, fileNameValue);
            }
        }
    }

    public static class InvertedIndexNameReducer 
            extends Reducer<Text, Text, Text, Text> {
        private Text result = new Text();

        public void reduce(Text key, Iterable<Text> values, 
                Context context
                ) throws IOException, InterruptedException {
            StringBuilder sb = new StringBuilder();
            boolean first = true;
            for (Text value : values) {
                if (first) {
                    first = false;
                } else {
                    sb.append(" ");
                }
                if (sb.lastIndexOf(value.toString()) < 0) {
                    sb.append(value.toString());
                }
            }
            result.set(sb.toString());
            context.write(key, result);
        }
    }

    public static void main(String[] args) throws Exception {
        /*
         * * I have used my local path in windows change the path as per your
         * * local machine
         * */
        args = new String[] { "file:///home/padawong/Workspace/MapReduce/input",
            "file:///home/padawong/Workspace/MapReduce/output" };
        /* delete the output directory before running the job */
        FileUtils.deleteDirectory(new File(args[1]));
        /* set the hadoop system parameter */
        System.setProperty("hadoop.home.dir", "~/hadoop-3.3.0/");
        if (args.length != 2) {
            System.err.println("Please specify the input and output path");
            System.exit(-1);
        }
        
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "Find_Average_Salary");
        job.setJarByClass(MapReduce.class);
//        job.setJobName("Find_Average_Salary");
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        job.setMapperClass(InvertedIndexNameMapper.class);
        job.setReducerClass(InvertedIndexNameReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }

    /*
    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "word count");
        job.setJarByClass(MapReduce.class);
        job.setMapperClass(TokenizerMapper.class);
        job.setCombinerClass(IntSumReducer.class);
        job.setReducerClass(IntSumReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
    */
}
