import { GoogleGenerativeAI } from "@google/generative-ai";
import dotenv from "dotenv";
dotenv.config();

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

export default async function gemini_summarize(text) {
    try {
        const result = await model.generateContent(`Summarize the following text:\n\n${text}`);
        return result.response.text();
    } catch (error) {
        console.error('Error generating content:', error);
        return null;
    }
}

