package chessur;

import AIsocket.TCPServer;
import chessur.LibraryURscript;
import socket.Coordinates;
import socket.URsocket;

/**
 *
 * @author Børge
 */
public class ChessUR {

    /*
    Here we can set the ip-adress and port to the UR5
     */
    static String serverUR = "192.168.0.3";
    static int portUR = 30002;

    /*
    Here we can set the ip-address and port for the PC
    (currently not in use, will implement at a later point)
     */
    static String serverPC = "192.168.0.2";
    static int portPC = 29999;

    /*
    Here we can choose which file and where to find it
    Wont work properly until this is changed to correct folder
     */
    static String filePath = "F:/GitHub/EiT_chess_robot/URscript/";
    static String movePushRehab = ".script";

    /*
    Here we can set the acceleration and velocity for the UR
    Use values between 0.1 and 1.0
     */
    static String a = "0.1";
    static String v = "0.1";

    /*
    Here we can choose if we want to send the file or following script to robot
    true sends string script, false sends file
     */
//    static boolean choice = true;       //  currently not in use
    public static void main(String[] args) {
        /*
        Create new object and send the ip and port to class URsocket
         */
        URsocket client = new URsocket(serverUR, portUR);
        Coordinates crd = new Coordinates();
        Thread coordinateThread = new Thread((Runnable) crd);

        /*
        Create a new object from our Libary of URScripts.
         */
        LibraryURscript scriptUR = new LibraryURscript(serverPC, portPC);

        String scriptToWrite;

        // Finn ut av dette........
        while (crd.getStatusUR() == 1) {
            System.out.println("Status UR: Running script");
        }
        int i = 0;
        while (true) {
            //Get's script to be sendt
            scriptToWrite = scriptUR.moveChessPiece(TCPServer.getNextMove());
            /*
            Try to connect to the UR, then it will send the chosen URScript to UR.
            It will also start to listen on port 30002. The UR will send joint
            positions and coordinations back to Java.
             */
            client.connectUR();
            client.sendScriptToUR(scriptToWrite);
            System.out.println("-----------------------------------------------------");
            if (i == 0) {
                coordinateThread.start();
            }
            i++;
        }
    }

}
