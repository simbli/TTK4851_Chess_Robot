package AIsocket;

import java.net.*;
import java.io.*;
import java.util.Arrays;

public class TCPServer {

    public static int[] getNextMove() {


        ServerSocket serverSocket = null;

        try {
            serverSocket = new ServerSocket(5005);
        }
        catch (IOException e)
        {
            System.err.println("Could not listen on port: 5005.");
            System.exit(1);
        }

        Socket clientSocket = null;
        System.out.println ("Waiting for connection.....");

        try {
            clientSocket = serverSocket.accept();
        }
        catch (IOException e)
        {
            System.err.println("Accept failed.");
            System.exit(1);
        }

        System.out.println ("Connection successful");
        System.out.println ("Waiting for input.....");
        String inputLine;
        String outPut = "";

        try{
            PrintWriter out = new PrintWriter(clientSocket.getOutputStream(),
                    true);
            BufferedReader in = new BufferedReader(
                    new InputStreamReader( clientSocket.getInputStream()));


            while ((inputLine = in.readLine()) != null)
            {
                System.out.println ("Server: " + inputLine);
                out.println(inputLine);
                outPut = inputLine;

            }


            out.close();
            in.close();
            clientSocket.close();
            serverSocket.close();

        } catch (IOException e) {
            e.printStackTrace();
        }


        return convertCoordinates(outPut);


    }

    private static int[] convertCoordinates(String move){
        int[] ar = new int[4];
        System.out.println("MOVE "+ move);
        for (int i = 0; i < move.length(); i++) {
            ar[i] = getInt(move.charAt(i));
        }
        return ar;
    }

    private static int getInt(char c){
        if (Character.isLetter(c)) return c-'a';
        else return c-'1';
    }


    public static void main(String[] args) {
        int i = 0;
        while (i < 10){
            System.out.println("i: "+i);
            System.out.println(Arrays.toString(TCPServer.getNextMove()));
            i++;

        }


    }


} 