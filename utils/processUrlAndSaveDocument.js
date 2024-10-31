import fs from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import UploadedDocument from '../models/DocumentUpload.js';
import createEmbedding from './createEmbedding.js';

// Define __dirname for ES module
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

export default async function processUrlAndSaveDocument(file_name, text) {
  try {
    // Generate embedding for the provided text
    const embedding = await createEmbedding(text);

    // Step 1: Database Operation
    const updatedDoc = await UploadedDocument.findOneAndUpdate(
      { title: file_name },  // Search criteria
      { description: text, embedding: embedding }, // Update fields
      { new: true, upsert: true } // Options: `new` returns the updated document, `upsert` creates if not found
    );

    // Step 2: JSON File Operation
    const jsonPath = join(__dirname, 'pdf_data.json');
    let jsonData = [];

    // Check if file exists and read it
    if (fs.existsSync(jsonPath)) {
      const fileContent = fs.readFileSync(jsonPath, 'utf8');
      jsonData = JSON.parse(fileContent);
    }

    // Find existing document in jsonData
    const existingEntryIndex = jsonData.findIndex(entry => entry.title === file_name);

    // Update the existing entry or add a new one
    const newEntry = { title: file_name, description: text, embedding: embedding };
    if (existingEntryIndex >= 0) {
      jsonData[existingEntryIndex] = newEntry; // Update existing entry
    } else {
      jsonData.push(newEntry); // Add new entry
    }

    // Write updated data back to the JSON file
    try {
      fs.writeFileSync(jsonPath, JSON.stringify(jsonData, null, 2));
      console.log('JSON file updated successfully:', jsonPath);
    } catch (writeError) {
      console.error('Error writing to JSON file:', writeError.message);
    }

    return {
      completed: true,
      message: 'Document uploaded or updated successfully',
      data: updatedDoc,
    };
  } catch (error) {
    console.error('Error processing document:', error.message);
    return { completed: false, message: `Error processing document: ${error.message}` };
  }
};
