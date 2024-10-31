import OpenAI from 'openai';
import dotenv from 'dotenv';
dotenv.config();

const openai = new OpenAI({
  apiKey: process.env.OPENAI_KEY,
});

export default async function createEmbedding(text) {
  const embeddingResponse = await openai.embeddings.create({
    model: 'text-embedding-ada-002',
    input: text,
  })
  const embedding = embeddingResponse.data[0].embedding
  return embedding
}
