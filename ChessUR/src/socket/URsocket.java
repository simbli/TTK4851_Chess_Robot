package socket;

import java.io.DataOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.net.Socket;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Paths;

public class URsocket {
/*
    Declaration of variables
    */
    static String serverName;
    static int port;
    static Socket client;
    static DataOutputStream out;
    static OutputStream outToServer;

    /*
    Constructor to recieve address and port
    */
    public URsocket(String serverName, int port) {
        this.serverName = serverName;
        this.port = port;
    }

    /*
    Method to connect to the UR
    */
    public void connectUR() {
        try {
            /*
            Establish socket connection to the UR
             */
            System.out.println("Connecting to " + serverName + " on port " + port);
            client = new Socket(serverName, port);
            client.setSoTimeout(5000);
            System.out.println("Connected to " + client.getRemoteSocketAddress());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void sendScriptToUR(String scriptToWrite) {
        /*
            Display what we are sending to the server
         */
        System.out.println(scriptToWrite);

        try {
            /*
            Create stream to read from file and send data to UR
             */
            outToServer = client.getOutputStream();
            out = new DataOutputStream(outToServer);
            /*
            Write script to server
             */
            out.write(scriptToWrite.getBytes());
            out.write('\n'); // Always newline after a script
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    /*
    Method to read from script file
     */
    static String readFile(String path) throws IOException {
        byte[] encoded = Files.readAllBytes(Paths.get(path));
        return new String(encoded, Charset.defaultCharset());
    }
}
