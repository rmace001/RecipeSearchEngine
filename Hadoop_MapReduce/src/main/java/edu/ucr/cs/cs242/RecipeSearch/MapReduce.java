// References: https://hadoop.apache.org/docs/current/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html, https://timepasstechies.com/map-reduce-inverted-index-sample/
package edu.ucr.cs.cs242.RecipeSearch;

import java.io.IOException;
import java.util.StringTokenizer;

import java.io.*;
import org.apache.commons.io.FileUtils;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.NLineInputFormat;
import org.apache.hadoop.mapreduce.lib.output.LazyOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.input.FileSplit;
import java.util.Arrays;
import java.util.StringTokenizer;
import java.nio.file.Paths;
import java.nio.file.Files;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;


public class MapReduce {

    public static class InvertedIndexMapper
            extends Mapper<Object, Text, Text, Text> {

            private Text recipe = new Text();
            private Text word = new Text();

            @Override
            public void map(Object key, Text value, Context context
                    ) throws IOException, InterruptedException {
                String data = value.toString();

                // Extract recipe link
                String[] input = data.split("\t", 2);
                String link = input[0];

                // Remove punctuation from non-link data
                String[] field = input[1].replaceAll("\\p{Punct}", " ").toLowerCase().split("\t");
                StringTokenizer it = new StringTokenizer(Arrays.toString(field)
                        /* Remove punc added by split */        .replace(",", "")
                                                                .replace("[", "")
                                                                .replace("]", ""));
                recipe.set(link);

                while (it.hasMoreTokens()) {
                    word.set(it.nextToken());
                    // Emit term and recipe link
                    context.write(word, recipe);
                }
                    }
    }

    // Reducer: compiles index
    public static class InvertedIndexReducer
            extends Reducer<Text, Text, Text, Text> {
            private Text list = new Text();

            public void reduce(Text key, Iterable<Text> links, 
                    Context context
                    ) throws IOException, InterruptedException {

                StringBuilder sb = new StringBuilder();

                // Build list of links delimited by space
                boolean first = true;
                for (Text link : links) {
                    if (first) {
                        first = false;
                    } 
                    else {
                        // Space as delimiter
                        sb.append(" ");
                    }

                    // Append link
                    if (sb.lastIndexOf(link.toString()) < 0) {
                        sb.append(link.toString());
                    }
                }
                list.set(sb.toString());
                context.write(key, list);
                    }
    }

    public static void main(String[] args) throws Exception {
        // Hardcoding directories
        args = new String[] { "file:///home/padawong/Workspace/MapReduce/input",
            "file:///home/padawong/Workspace/MapReduce/output" };
        if (args.length != 2) {
            System.err.println("Parameters missing. Usage: input_dir output_dir");
            System.exit(-1);
        }

        // Clean up data file for proper mapreduce parsing
        java.nio.file.Path file = Paths.get("./input/data.json");
        Charset charset = StandardCharsets.UTF_8;
        String str = new String(Files.readAllBytes(file), charset);
        str = str.replace("\\n", " ")
                 .replace("\"}, {", "\n")
                 .replace("[{", "")
                 .replace("}]", "")
                 .replace("\"recipe_link\": \"", "")
                 .replaceAll("\\[.]", "")
                 .replace("\", \"recipe_title\": \"", "\t")
                 .replace("\", \"special_equipment\": \"", "\t")
                 .replace("\", \"notes\": \"", "\t")
                 .replace("\", \"ingredients\": \"", "\t")
                 .replaceAll("\", \"active_time\": .*, \"total_time\": .*, \"direction\": \"", "\t")
                 .replaceAll("\", \"total_time\": .*, \"active_time\": .*, \"direction\": \"", "\t");
        Files.write(file, str.getBytes(charset));

        System.setProperty("hadoop.home.dir", "~/hadoop-3.3.0/");

        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "Index");
        job.setJarByClass(MapReduce.class);
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        job.setMapperClass(InvertedIndexMapper.class);
        job.setReducerClass(InvertedIndexReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
