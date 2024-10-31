import mongoose from 'mongoose';
import dotenv from 'dotenv';
dotenv.config();


const MONGO_URI = process.env.MONGO_URI;


export default async function connectToMongoDB() {
  try {
    await mongoose.connect(MONGO_URI);
    console.log('Successfully connected to MongoDB');
  } catch (error) {
    console.error('Error connecting to MongoDB:', error);
    throw error;
  }
}
