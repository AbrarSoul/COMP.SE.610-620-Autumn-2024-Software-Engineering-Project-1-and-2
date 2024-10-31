import http from 'http';
import { expect } from 'chai';
import { Server } from 'socket.io';
import express from 'express';
import io from 'socket.io-client'; 

const app = express();

describe('PDF Summarizer API', () => {
  let server;
  let sio;
  let clientSocket;

  before((done) => {
    server = http.createServer(app);
    sio = new Server(server, {
      cors: {
        origin: 'http://localhost:5173', 
        methods: ['GET', 'POST'],
      },
    });

    server.listen(5001, () => {
      console.log('Test server running on port 5001');
      clientSocket = io('http://localhost:5001'); 
      clientSocket.on('connect', () => {
        console.log('Client connected');
        done(); 
      });
    });
  });

  after((done) => {
    clientSocket.close();
    sio.close();
    server.close(done);
  });

  describe('Socket.IO Events', () => {
    it('should summarize PDF content with both models', function (done) {
      this.timeout(100000); 

      const mockPdfBuffer = Buffer.from('Mock PDF content for testing.');

      let receivedSummary1 = false;
      let receivedSummary2 = false;

      clientSocket.emit('upload_pdf', mockPdfBuffer);

      clientSocket.on('summary1', (summary1) => {
        console.log('Received summary1:', summary1); 
        expect(summary1).to.exist; 
        receivedSummary1 = true; 
      });

      clientSocket.on('summary2', (summary2) => {
        console.log('Received summary2:', summary2); 
        expect(summary2).to.exist; 
        receivedSummary2 = true; 
      });

      
      const checkCompletion = setInterval(() => {
        if (receivedSummary1 && receivedSummary2) {
          clearInterval(checkCompletion);
          clientSocket.emit('disconnect');
          done();
        }
      }, 100);

      
      setTimeout(() => {
        if (!receivedSummary1 || !receivedSummary2) {
          clearInterval(checkCompletion);
          clientSocket.emit('disconnect');
          done(new Error('Test timed out waiting for summaries.'));
        }
      }, 10000); 
    });

    it('should handle errors when processing PDF', function (done) {
      this.timeout(10000); 

      clientSocket.emit('upload_pdf', null);

      clientSocket.on('error', (error) => {
        console.log('Error received:', error); 
        expect(error).to.equal('Error processing the PDF file');
        done();
      });
    });
  });
});
