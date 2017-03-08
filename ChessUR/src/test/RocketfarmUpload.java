/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package test;

import java.net.*;
import java.io.*;
import java.nio.ByteBuffer;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Paths;

/**
 *
 * @author Børge
 */
public class RocketfarmUpload {
    
    static double x1, y1, z1, rx, ry, rz, a, v;
    static String script
            = "def test():\n"
            + " socket_open(\"127.0.0.1\",63351,\"stream\")\n"
            + "end";
    static String scriptMovement;

    public static void main(String[] args) {
//        String filePath = "F:/Dropbox lagring/Dropbox/Prosjekt 14/Bachelor/borgeg/";
//        String scriptFile = "handshake_v3.script"; // ball_pull_v2  handshake_v2

        String filePath = "F:/GitHub/EiT_chess_robot/URscript/newGripper/";
//       String scriptFile = "palletTest.script"; 
//        String scriptFile = "pickUpTest.script";
//        String scriptFile = "xyMove.script";
         String scriptFile = "xyMoveGripper45deg.script";
//         String scriptFile = "hoverplan.script";
         
        
//        Scanner input = new Scanner(System.in);
//        String choice;

        String serverName = "192.168.0.3";
        int port = 30002;
//        int port = 63350;

        // acceleration and velocity
        a = 0.4;
        v = 0.1;
        //  Safe positions
        x1 = 0.2;
        y1 = 0.4;
        z1 = 0.7;
        rx = 3.1415;
        ry = 0.0;
        rz = 0.0;

        scriptMovement
                = "def scriptmovement():\n"
                + " textmsg(\"Starting script from String\")\n"
                + " movej(p[" + x1 + ", " + y1 + "," + z1 + "," + rx + "," + ry + "," + rz + "]," + v + "," + a + ")\n"
                + " movej(p[" + x1 + ", " + y1 + "," + (z1) + "," + rx + "," + ry + "," + rz + "]," + v + "," + a + ")\n"
                + "end";

        String scriptMove2
                = "def scriptMove2():\n"
                + " movej([-0.5605182705025187, -2.350330184112267, -1.316631037266588, -2.2775736604458237, 2.3528323423665642, -1.2291967454894914], a=1.3962634015954636, v=0.1471975511965976)\n"
                + "end";
        try {
            // Open socket
            System.out.println("Connecting to " + serverName + " on port " + port);
            Socket client = new Socket(serverName, port);
            client.setSoTimeout(5000);
            System.out.println("Just connected to " + client.getRemoteSocketAddress());

            OutputStream outToServer = client.getOutputStream();
            DataOutputStream out = new DataOutputStream(outToServer);

            InputStream fromServer = client.getInputStream();
            DataInputStream in = new DataInputStream(fromServer);

            String scriptToWrite;

            // Choose inline or file
            if (false) {
                scriptToWrite = scriptMovement;
                System.out.println("Writing urscript to robot: ");

            } else {
                scriptToWrite = readFile(filePath + scriptFile);
                System.out.println("Writing urscript to robot: " + scriptFile);

            }
//             Write script to socket
            System.out.println(scriptToWrite);

            out.write(scriptToWrite.getBytes());
            out.write('\n'); // Always newline after a script

            final int MAX = 1100;

            byte[] b = new byte[MAX];
            byte buf_net[] = new byte[MAX];
            byte buf_new[] = new byte[MAX];
            int index = 0;

            do {
                int size = fromServer.read(b);
                if (size > 0) {
                    for (int i = 0; i < size; i++) {

                        buf_net[index++] = b[i];

                    }
                    while (index >= size) {
                        //System.out.println("index " + index);
                        for (int i = 0; i < 560; i++) {
                            buf_new[i] = buf_net[i];
                        }
                        for (int i = size; i < MAX; i++) {
                            buf_net[i - size] = buf_net[i];
                        }

                        index = index - size;
//                for (int i = 0; i < b.length; i++) {
//                    System.out.print("[" + b[i] + "] ");
//                }

                        //  System.out.println("size "+size);
                        ByteBuffer bb = ByteBuffer.wrap(b);
                        //String tt = new String(b);
                        //int ii = Integer.parseInt(tt);
                        int sizenew = bb.getInt(0);
                        System.out.println("Pakke size: " + sizenew + " Size: " + size);
                        if (sizenew == size) {

//                    double x1norm = bb.getDouble(47);
//                    double y1norm = bb.getDouble(88);
//                    double z1norm = bb.getDouble(129);
//                    double rxnorm = bb.getDouble(170);
//                    double rynorm = bb.getDouble(211);
//                    double rznorm = bb.getDouble(252);
//                    System.out.println("movej(");
//                    System.out.println("[" + x1norm + "," + y1norm + "," + z1norm + "," + rxnorm + "," + rynorm + "," + rznorm + "]");
//                    System.out.println("X: " + x1norm);
//                    System.out.println("Y: " + y1norm);
//                    System.out.println("Z: " + z1norm);
//                    System.out.println("Rx: " + rznorm);
//                    System.out.println("Ry: " + rynorm);
//                    System.out.println("Rz: " + rznorm);
//                    System.out.println("");
//                    System.out.println("movej(p[");
//                    System.out.println("pX: " + bb.getDouble(290));
//                    System.out.println("pY: " + bb.getDouble(298));
//                    System.out.println("pZ: " + bb.getDouble(306));
//                    System.out.println("rx?: " + bb.getDouble(314));
//                    System.out.println("ry?: " + bb.getDouble(322));
//                    System.out.println("rz?: " + bb.getDouble(330));
//                    System.out.println("");
//                            if (b[18] == 0) {
//                                System.out.println("UR: disconnected");
//                            }
//                            if (b[19] == 0) {
//                                System.out.println("UR: disabled");
//                            }
//                            if (b[20] == 0) {
//                                System.out.println("Power: off");
//                            }
//
//                            if (b[21] == 1) {
//                                System.out.println("EMERGENCY STOP ACTIVATED!!");
//                                System.out.println("EMERGENCY STOP ACTIVATED!!");
//                                break;
//                            }
//                            if (b[22] == 1) {
//                                System.out.println("Security stop: on");
//                            }
//                            if (b[23] == 1) {
//                                System.out.println("Program: running");
//                            }
//                            if (b[24] == 1) {
//                                System.out.println("Program: paused");
//                            }
//                            for (int i = 0; i < b.length; i++) {
//                        System.out.print("[" + b[i] + "] ");
//                            }
//
//                            for (int i = 0; i < b.length; i++) {
//                                System.out.println(i + " " + bb.getDouble(i));
//
//                            }
                        }

//                System.out.println("length getInt(0) " + bb.getInt(0));
//                System.out.println("b[9] " + b[9]);
//                if (b[4] == 16) {
//                    System.out.println("");
//                    System.out.print("X: ");
//                    for (int i = 399; i < 407; i++) {
//                        double c = b[i];
//                        System.out.print(c);
//                    }
//                    System.out.println("");
//                    System.out.print("Y: ");
//                    for (int i = 407; i < 415; i++) {
//                        double c = b[i];
//                        System.out.print(c);
//                    }
//                    System.out.println("");
//                    System.out.print("Z: ");
//                    for (int i = 415; i < 423; i++) {
//                        double c = b[i];
//                        System.out.print(c);
//                    }
//                }
//                if (sizenew == size) {
//
//                    for (int i = 4; i < 13; i++) {
//                        System.out.println("Timestamp " + bb.getInt(i));
//                    }
//                    System.out.println(bb.getInt(80));
//                    for (int i = 86; i <= 94; i++) {
//                        System.out.println("Joint Data " + i + " " + bb.getDouble(i));
//                    }
//                    for (int i = 95; i <= 103; i++) {
//                        System.out.println("Target joint " + i + " " + bb.getDouble(i));
//                        
//                    }
//                    Thread.sleep(3000);
                        //System.out.println("joint 0 info " + bb.getLong(39));
//                    long tid =      bb.get(39);
//                    tid = tid * 256 + bb.get(40);
//                    tid = tid * 256 + bb.get(41);
//                    tid = tid * 256 + bb.get(42);
//                    tid = tid * 256 + bb.get(43);
//                    tid = tid * 256 + bb.get(44);
//                    tid = tid * 256 + bb.get(45);
//                    tid = tid * 256 + bb.get(46);
//                    System.out.println(" time " + tid);
//                  
//                    System.out.println("q target 2 " + bb.getLong(28));
//                    System.out.println("q target 3 " + bb.getLong(36));
//                    System.out.println("q target 4 " + bb.getLong(44));
//                    System.out.println("q target 5 " + bb.getLong(52));
//                } else {
//                    //System.out.println("error");
//                }
                        System.out.println("");
                        //System.out.println("****");
                        // System.out.println(fromServer.read());
//               System.out.println("***");
//                
//                System.out.println(in.readInt());
//                for (int i = 0; i < 95; i++) {
//                    System.out.println(in.readDouble());
//                }
//                System.out.println("***");
                    }
                }
                // in2 =  in. .readChar() ;
                //System.out.print(in);
                Thread.sleep(2);
            } while (true);
//            System.out.println("Closing socket");
//            client.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    static String readFile(String path) throws IOException {
        byte[] encoded = Files.readAllBytes(Paths.get(path));
        return new String(encoded, Charset.defaultCharset());
    }
}


//            /*
//            Choose if we want to send a string or file to server
//             */
//            if (choice) {
//                scriptToWrite = scriptFromHandEye;
//                System.out.println("Sending string to robot");
//
//            } else {
//                scriptToWrite = readFile(filePath + movePushRehab);
//                System.out.println("Sending " + movePushRehab + " to robot");
//
//            }
