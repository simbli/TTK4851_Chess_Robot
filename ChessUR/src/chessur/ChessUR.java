package chessur;

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
    static boolean choice = true;       //  currently not in use

    /*
    Positions for UR
    These are tested and it is safe for the UR to move into these positions
     */
    static double x1 = 0.1;
    static double y1 = 0.4;
    static double z1 = 0.7;
    static double rx = 3.1415;
    static double ry = 0.0;
    static double rz = 0.0;

    /*
    Example of two different ways to move the robot. These are the same waypoints
    using two different ways to determine where and how UR will move
     */
    static String scriptMovement
            = "def scriptmovement():\n"
            + " textmsg(\"Starting script from String\")\n"
            + " movej(p[" + x1 + ", " + y1 + "," + z1 + "," + rx + "," + ry + "," + rz + "]," + v + "," + a + ")\n"
            + "end";
    static String moveHome
            = "= def moveHome():\n"
            + " movej([4.19949825862993,-1.5307928265838344,0.7768978331470714,-0.816820601535465,-1.570841791732095,-0.512890719912271]," + a + "," + v + ")\n"
            + "end";
    static char in;

    public static void main(String[] args) {
        /*
        Create new object and send the ip and port to class URsocket
         */
        URsocket client = new URsocket(serverUR, portUR);
        Thread coordinateThread = new Thread((Runnable) new Coordinates());

        /*
        Create a new object from our Libary of URScripts.
        */
        LibraryURscript scriptUR = new LibraryURscript(serverPC,portPC);
     


        String scriptToWrite;

        scriptToWrite = scriptUR.pickUpTest();
//        scriptToWrite = scriptUR.HandEyeCoordination(a, v);
//        scriptToWrite = scriptUR.test(a, v);
//        scriptToWrite = scriptUR.BallPull(a, v);

        /*
        Try to connect to the UR, then it will send the chosen URScript to UR.
        It will also start to listen on port 30002. The UR will send joint
        positions and coordinations back to Java.
        */
        client.connectUR();
        client.sendScriptToUR(scriptToWrite);
        coordinateThread.start();

    }

}
