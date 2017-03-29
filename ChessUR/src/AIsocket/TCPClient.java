package AIsocket;


import java.io.*;
import java.net.*;

public class TCPClient {
    public static void sendConfirmation(){
        try{
            String sentence;
            String modifiedSentence;
            BufferedReader inFromUser = new BufferedReader( new InputStreamReader(System.in));
            Socket clientSocket = new Socket("localhost", 5006);
            DataOutputStream outToServer = new DataOutputStream(clientSocket.getOutputStream());
            BufferedReader inFromServer = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
            sentence = "1";
            outToServer.writeBytes(sentence + '\n');
            modifiedSentence = inFromServer.readLine();
            System.out.println("FROM SERVER: " + modifiedSentence);
            clientSocket.close();

        }catch (Exception e){
            e.printStackTrace();
        }

    }

    public static void main(String[] args) {
        sendConfirmation();
    }

}

