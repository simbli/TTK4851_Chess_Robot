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
//        scriptToWrite = scriptUR.lineUpPieces();

        // Status UR:   crd.getStatusUR()
        int i = 0;
        while (true) {
            //Get's script to be sendt
            scriptToWrite = scriptUR.moveChessPiece(TCPServer.getNextMove());

            //Try to connect to the UR, and send URScript to UR.
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
