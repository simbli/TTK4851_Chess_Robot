package socket;

import java.io.DataInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.ByteBuffer;
import java.util.logging.Level;
import java.util.logging.Logger;
import static socket.URsocket.client;

public class Coordinates implements Runnable {

    /*
    Declaration of variables
     */
    int size;
    InputStream fromServer;
    DataInputStream in;

    int statusUR;

    public int getStatusUR() {
        return statusUR;
    }

    @Override
    public void run() {
        final int MAX = 10000;

        byte[] b = new byte[MAX];
        byte buf_net[] = new byte[MAX];
        byte buf_new[] = new byte[MAX];     //  excess?
        int index = 0;

        do {
            /*
            Here we create and read from stream
             */
            try {
                fromServer = client.getInputStream();
                size = fromServer.read(b);
            } catch (IOException ex) {
                Logger.getLogger(Coordinates.class.getName()).log(Level.SEVERE, null, ex);
            }

            /*
            Here we check if stream is empty
             */
            if (size > 0) {
                /*
                Here we do something that seem to work
                 */
                for (int i = 0; i < size; i++) {
                    buf_net[index++] = b[i];
                }
                while (index >= size) {
                    for (int i = 0; i < 560; i++) { //  excess?
                        buf_new[i] = buf_net[i];    //  excess?
                    }
                    for (int i = size; i < MAX; i++) {
                        buf_net[i - size] = buf_net[i];
                    }

                    index = index - size;

                    /*
                    Here we wrap a byte array into a buffer
                     */
                    ByteBuffer bb = ByteBuffer.wrap(b);
                    int sizenew = bb.getInt(0);

                    if (sizenew == size) {
                        /*
                        Get coordinates. Sent from UR as Double
                        Print both types of coordinates
                        +41 / +8
                         */
                        double x1norm = bb.getDouble(47);
                        double y1norm = bb.getDouble(88);
                        double z1norm = bb.getDouble(129);
                        double rxnorm = bb.getDouble(170);
                        double rynorm = bb.getDouble(211);
                        double rznorm = bb.getDouble(252);
                        double x1p = bb.getDouble(290);
                        double y1p = bb.getDouble(298);
                        double z1p = bb.getDouble(306);
                        double rxp = bb.getDouble(314);
                        double ryp = bb.getDouble(322);
                        double rzp = bb.getDouble(330);
//
//                        System.out.println("movej(");
//                        System.out.println("[" + x1norm + "," + y1norm + "," + z1norm + "," + rxnorm + "," + rynorm + "," + rznorm + "]");
//                        System.out.println("");
//                        System.out.println("movej(p[");
//                        System.out.println("[" + x1p + "," + y1p + "," + z1p + "," + rxp + "," + ryp + "," + rzp + "]");
//                        System.out.println("");

                        /*
                        State of the robot, will create a GUI for it at a
                        later time. I have no idea how to create a GUI or make
                        it look pretty. Work in progress
                         */
                        if (b[18] == 0) {
                            System.out.println("UR: disconnected");
                        }
                        if (b[19] == 0) {
                            System.out.println("UR: disabled");
                        }
                        if (b[20] == 0) {
                            System.out.println("Power: off");
                        }
                        if (b[21] == 1) {
                            System.out.println("EMERGENCY STOP ACTIVATED!!");
                            break;
                        }
                        if (b[22] == 1) {
                            System.out.println("Security stop: on");
                        }
                        if (b[23] == 1) {
                            System.out.println("Program: running");
                        }
                        if (b[23] != 1) {
                            System.out.println("Program: stopped");
                        }
                        if (b[24] == 1) {
                            System.out.println("Program: paused");
                        }
                    }
                }
            }
            statusUR = b[23];

        } while (true);

    }
}
