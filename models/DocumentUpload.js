import mongoose from 'mongoose';

const Schema = mongoose.Schema

// Create a new schema for uploaded documents
const DocumentUploadSchema = new Schema({
  title: String,
  description: String,
  fileName: String,
  uploadDate: {
    type: Date,
    default: Date.now,
  },
  embedding: [Number],
  // Represents the vector embedding
  // 1536 numbers in array (this is if you use OpenAI ada embeddings)
  // You can add other fields as needed
})

// Create a model from the schema
const UploadedDocument = mongoose.model(
  'UploadedDocument',
  DocumentUploadSchema
)

export default UploadedDocument;