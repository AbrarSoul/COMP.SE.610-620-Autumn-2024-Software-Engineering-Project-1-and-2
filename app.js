import express from 'express';
import PdfParse from 'pdf-parse/lib/pdf-parse.js';
import multer from 'multer';
import hface_summarize from './utils/hface.js';
import gemini_summarize from './utils/gemini.js';
import openai from './utils/openai.js';
import processUrlAndSaveDocument from './utils/processUrlAndSaveDocument.js';
import createEmbedding from './utils/createEmbedding.js';
import findSimilarDocuments from './utils/findSimilarDocuments.js';
import connectToMongoDB from './config/MongoDB.js';
import dotenv from 'dotenv';
dotenv.config();




const app = express();
const upload = multer();

// Serve static files from the frontend 'dist' directory
// const frontendPath = path.join(__dirname, '../frontend/dist/index.html');

app.use(express.static('public'));
app.use(express.json());

// PDF upload and processing endpoint
app.post('/upload_pdf', upload.single('file'), async (req, res) => {

  try {
    if (!req.file) {
      return res.status(400).json({ message: 'No file uploaded. Please upload a PDF file.' });
    }

    const fileBuffer = req.file.buffer;
    const fileName = req.file.originalname;

    // Parse the PDF text
    const pdfText = await PdfParse(fileBuffer).then(data => data.text);
    
    // Process the document and save it
    const result = await processUrlAndSaveDocument(fileName, pdfText);

    // Respond with success message
    res.status(200).json({ message: 'PDF uploaded and processed successfully!', data: result });
  } catch (error) {
    console.error('Error processing PDF:', error.message);
    res.status(500).json({ message: 'Error processing the PDF file. Kindly try again.' });
  }
});

app.post('/query', async (req, res) => {
  try {
    const { query } = req.body;
    const embedding = await createEmbedding(query);

    const similarDocuments = await findSimilarDocuments(embedding);
    if (similarDocuments.length === 0) {
      res.status(404).json({ response: 'No similar documents found.' });
      return;
    }
    const highestScoreDoc = similarDocuments.reduce((highest, current) => {
      return highest.score > current.score ? highest : current;
    });
    const prompt = `Based on this context: ${highestScoreDoc.description} \n\n Query: ${query} \n\n Answer:`;
    const answer = await openai(prompt);
    res.status(200).json({ response: answer });
  } catch (error) {
    console.error('Error processing query:', error.message);
    res.status(500).json({ error: 'Error processing the query' });
  }
});



// Start the server
const PORT = 5000;
app.listen(PORT, async () => {
  await connectToMongoDB();
  console.log(`Server is running on  http://localhost:${PORT}`);
});
