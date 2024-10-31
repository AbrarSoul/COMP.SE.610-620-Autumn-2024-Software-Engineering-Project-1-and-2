import UploadedDocument from '../models/DocumentUpload.js';


export default async function findSimilarDocuments(embedding) {
    try {
      // Query similar documents using Mongoose
      const documents = await UploadedDocument.aggregate([
        {
          $search: {
            knnBeta: {
              vector: embedding,
              path: 'embedding', // The path to the embedding field in the collection
              k: 5,  // Return top 5 most similar documents
            },
          },
        },
        {
          $project: {
            description: 1,
            score: { $meta: 'searchScore' },
          },
        },
      ]);
      // console.log('documents---------', documents)
      return documents;
    } catch (err) {
      console.error(err);
      throw err;
    }
  }