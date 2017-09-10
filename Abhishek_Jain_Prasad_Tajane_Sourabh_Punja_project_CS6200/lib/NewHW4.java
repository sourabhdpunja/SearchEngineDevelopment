import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.ArrayList;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.AnalyzerWrapper;
import org.apache.lucene.analysis.core.SimpleAnalyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.index.Term;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopScoreDocCollector;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;

/**
 * To create Apache Lucene index in a folder and add files into this index based
 * on the input of the user.
 */
public class NewHW4 {
	private static Analyzer analyzer = new StandardAnalyzer(Version.LUCENE_47);
	private static SimpleAnalyzer sAnalyzer = new SimpleAnalyzer(Version.LUCENE_47);

	private static String corpusPath = "/Users/prasadtajane/Documents/workspace/IRHW4/src/cacm/";
	private static String quitChar = "q";
	private static String queryFilePath = "/Users/prasadtajane/PycharmProjects/untitled/final/lib/";
	private static String queryFileName = "new_queries.txt";
	private static String outFilePath = "/Users/prasadtajane/PycharmProjects/untitled/final/results/";
	private static String outFileName = "Lucene_feedback";

	private static int corpusPathLen = corpusPath.split("/").length;
	private static String outFilePathName = outFilePath + outFileName;


	private IndexWriter writer;
	private ArrayList<File> queue = new ArrayList<File>();

	private static FileOutputStream out = null;

	public static void main(String[] args) throws IOException {
		System.out
		.println("Enter the FULL path where the index will be created: (e.g. /Usr/index or c:\\temp\\index)");

		System.out.println(corpusPathLen);

		String indexLocation = null;
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		//String s = br.readLine();
		String s = corpusPath;

		HW4 indexer = null;
		try {
			indexLocation = s;
			indexer = new HW4(s);
		} catch (Exception ex) {
			System.out.println("Cannot create index..." + ex.getMessage());
			System.exit(-1);
		}

		// ===================================================
		// read input from user until he enters q for quit
		// ===================================================
		while (!s.equalsIgnoreCase("q")) {
			try {
				System.out
				.println("Enter the FULL path to add into the index (q=quit): (e.g. /home/mydir/docs or c:\\Users\\mydir\\docs)");
				System.out
				.println("[Acceptable file types: .xml, .html, .html, .txt]");
				//s = br.readLine();
				if (s.equalsIgnoreCase("q")) {
					break;
				}

				// try to add file into the index
				indexer.indexFileOrDirectory(s);
				s = quitChar;
			} catch (Exception e) {
				System.out.println("Error indexing " + s + " : "
						+ e.getMessage());
			}
		}

		// ===================================================
		// after adding, we always have to call the
		// closeIndex, otherwise the index is not created
		// ===================================================
		indexer.closeIndex();

		// =========================================================
		// Now search
		// =========================================================
		IndexReader reader = DirectoryReader.open(FSDirectory.open(new File(
				indexLocation)));
		//	IndexSearcher searcher = new IndexSearcher(reader);
		//	TopScoreDocCollector collector = TopScoreDocCollector.create(100, true);

		String pathstr = queryFilePath;
		BufferedReader in = new BufferedReader(new FileReader(pathstr + queryFileName));
		String line = "";
		int counter = 0;
		s = "";

		while ((line = in.readLine()) != null) {
			try {
				//s = br.readLine();
				s = line;
				if (s.equalsIgnoreCase("q")) {
					break;
				}

				Query q = new QueryParser(Version.LUCENE_47, "contents",
						sAnalyzer).parse(s);
				IndexSearcher searcher = new IndexSearcher(reader);
				TopScoreDocCollector collector = TopScoreDocCollector.create(100, true);
				searcher.search(q, collector);
				ScoreDoc[] hits = collector.topDocs().scoreDocs;
				counter += 1;

				// 4. display results
				System.out.println("Found " + hits.length + " hits.");
				String queryNum = String.valueOf(counter);
				String path = outFilePathName;
						// "Lucene_feedback/";
						//"Lucene_stoplist/;"
				OutputStreamWriter writer = new OutputStreamWriter(
						new FileOutputStream(path + "results_" + queryNum + ".txt")
						, "UTF-8");
				BufferedWriter bufWriter = new BufferedWriter(writer);

				for (int i = 0; i < hits.length; ++i) {
					//query_id    Q0   DocID   Rank   Lucene_score   system_name
					int docId = hits[i].doc;
					Document d = searcher.doc(docId);

					String str = d.get("path").split("/")[corpusPathLen];
					String outputString = queryNum + "    Q0    " + str.split(".html")[0].split("-")[1] + "    "
							+ (i + 1) + "    " + hits[i].score + "    Lucene\n";
					System.out.println(outputString);
					bufWriter.write(outputString);
					bufWriter.flush();
				}
				bufWriter.close();

				// 5. term stats --> watch out for which "version" of the term
				// must be checked here instead!
				Term termInstance = new Term("contents", s);
				long termFreq = reader.totalTermFreq(termInstance);
				long docCount = reader.docFreq(termInstance);
				System.out.println(s + " Term Frequency " + termFreq
						+ " - Document Frequency " + docCount);

			} catch (Exception e) {
				System.out.println("Error searching " + s + " : "
						+ e.getMessage());
				break;
			}

		}
		in.close();

	}

	/**
	 * Constructor
	 *
	 * @param indexDir
	 *            the name of the folder in which the index should be created
	 * @throws java.io.IOException
	 *             when exception creating index.
	 */
	NewHW4(String indexDir) throws IOException {

		FSDirectory dir = FSDirectory.open(new File(indexDir));

		IndexWriterConfig config = new IndexWriterConfig(Version.LUCENE_47,
				sAnalyzer);

		writer = new IndexWriter(dir, config);
	}

	/**
	 * Indexes a file or directory
	 *
	 * @param fileName
	 *            the name of a text file or a folder we wish to add to the
	 *            index
	 * @throws java.io.IOException
	 *             when exception
	 */
	public void indexFileOrDirectory(String fileName) throws IOException {
		// ===================================================
		// gets the list of files in a folder (if user has submitted
		// the name of a folder) or gets a single file name (is user
		// has submitted only the file name)
		// ===================================================
		addFiles(new File(fileName));

		int originalNumDocs = writer.numDocs();
		for (File f : queue) {
			FileReader fr = null;
			try {
				Document doc = new Document();

				// ===================================================
				// add contents of file
				// ===================================================
				fr = new FileReader(f);
				doc.add(new TextField("contents", fr));
				doc.add(new StringField("path", f.getPath(), Field.Store.YES));
				doc.add(new StringField("filename", f.getName(),
						Field.Store.YES));

				writer.addDocument(doc);
				System.out.println("Added: " + f);
			} catch (Exception e) {
				System.out.println("Could not add: " + f);
			} finally {
				fr.close();
			}
		}

		int newNumDocs = writer.numDocs();
		System.out.println("");
		System.out.println("************************");
		System.out
		.println((newNumDocs - originalNumDocs) + " documents added.");
		System.out.println("************************");

		queue.clear();
	}

	private void addFiles(File file) {

		if (!file.exists()) {
			System.out.println(file + " does not exist.");
		}
		if (file.isDirectory()) {
			for (File f : file.listFiles()) {
				addFiles(f);
			}
		} else {
			String filename = file.getName().toLowerCase();
			// ===================================================
			// Only index text files
			// ===================================================
			if (filename.endsWith(".htm") || filename.endsWith(".html")
					|| filename.endsWith(".xml") || filename.endsWith(".txt")) {
				queue.add(file);
			} else {
				System.out.println("Skipped " + filename);
			}
		}
	}

	/**
	 * Close the index.
	 *
	 * @throws java.io.IOException
	 *             when exception closing
	 */
	public void closeIndex() throws IOException {
		writer.close();
	}
}

///Users/prasadtajane/IR/Prasad_Tajane_CS6200_HW4/index
//What articles exist which deal with TSS (Time Sharing System), an operating system for IBM computers?
//Intermediate languages used in construction of multi-targeted compilers; TCOLL

///Users/prasadtajane/PycharmProjects/untitled/final/lib/Lucene/ParsedDocumentsstopped
///Users/prasadtajane/PycharmProjects/untitled/final/lib/Lucene/ParsedDocumentsstemmed
///Users/prasadtajane/PycharmProjects/untitled/final/cacm
///Users/prasadtajane/Documents/workspace/IRHW4/src/cacm