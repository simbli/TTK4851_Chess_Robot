package chessur;

import AIsocket.TCPClient;
import AIsocket.TCPServer;
import chessur.LibraryURscript;
import socket.Coordinates;
import socket.URsocket;

/**
 *
 * @author Børge
 */
public class ChessUR {

    //Set the ip-adress and port to the UR3
    static String serverUR = "192.168.0.3";
    static int portUR = 30002;

    public static void main(String[] args) throws InterruptedException {

        //Create new object and send the ip and port to class URsocket
        URsocket client = new URsocket(serverUR, portUR);

        //Create new object for "running program" variable from the UR stream
        Coordinates crd = new Coordinates();
        Thread coordinateThread = new Thread((Runnable) crd);

        //Create a new object from our Libary of URScripts.
        LibraryURscript scriptUR = new LibraryURscript();
        String scriptToWrite;
//        scriptToWrite = scriptUR.lineUpPieces();

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
            int rofl = 0;
            while (crd.getStatusUR() == 0) {
                System.out.println("first");
            }
            Thread.sleep(1000);
            while (crd.getStatusUR() == 1) {
                System.out.println("second");
            }
            Thread.sleep(1000);

            System.out.println("loops done!!!");
            TCPClient.sendConfirmation();
        }

    }

}
