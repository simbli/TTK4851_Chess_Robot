/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package chessur;

/**
 *
 * @author Børge
 * 
 * This class contains all the different URScript we use for the UR
 */
public class LibraryURscript {

    static String payloadUR = "0.4"; // in kilograms
    static String serverPC;
    static int portPC;

    public LibraryURscript(String serverPC, int portPC) {
        this.serverPC = serverPC;
        this.portPC = portPC;
    }

    public String threadSensorData() {
        /*
        This method will read data from the torque sensor and send it back
        to a socket server in Java. This script need to be combined with other
        scripts and run it will then run in a seperate thread.
        Add the following line to the script you want to run sensordata to.
        + "join threadId_SensorDataThread\n"

        The thread will recieve the serveraddress and serverport from URmain.java
         */
        String threadSensorData
                = "	thread SensorDataThread(): \n"
                + "		socket_close(\"stream\") #Close the stream \"stream\"\n"
                + "		sleep(0.1)\n"
                + "		socket_open(\"127.0.0.1\",63351,\"stream\")\n"
                + "		sleep(3)\n"
                + "		socket_close(\"pc_connect\") #Close the stream \"pc_connect\"\n"
                + "             global var_1 =   False  \n" // new
                + "             while (var_1 ==  False  ):\n"// new
                + "		  global var_1 = socket_open(\"" + serverPC + "\"," + portPC + ",\"pc_connect\")\n" // new
                + "             end\n"// new
                + "		socket_send_string(\"StartOfInput\", \"pc_connect\")\n"
                + "		socket_send_string(\";\", \"pc_connect\")\n"
                + "		while True:\n" // new
                + "			global sensor_data = socket_read_ascii_float(6,\"stream\")\n"
                + "			varmsg(\"sensor_data\",sensor_data)\n"
                + "			if (sensor_data[0]  >=6): #IfSensorDataArrayIsFilledThenRun\n"
                + "				global Fx = sensor_data[1]#Set input sensor data to appropiate variables\n"
                + "				global Fy = sensor_data[2]\n"
                + "				global Fz = sensor_data[3]\n"
                + "				global Mx = sensor_data[4]\n"
                + "				global My = sensor_data[5]\n"
                + "				global Mz = sensor_data[6]\n"
                + "			else: #IfItIsNotThenSetThemAllToZer0\n"
                + "				global Fx = 0.0 # set the variables to zer0\n"
                + "				global Fy = 0.0\n"
                + "				global Fz = 0.0\n"
                + "				global Mx = 0.0\n"
                + "				global My = 0.0\n"
                + "				global Mz = 0.0\n"
                + "			end #EndIf\n"
                + "			socket_send_string(\";\", \"pc_connect\")#New Line in java, to seperate the informationblocks\n"
                + "			socket_send_string(\"Fx: \", \"pc_connect\")#SendVariables\n"
                + "			socket_send_string(Fx, \"pc_connect\")#SendVariables\n"
                + "			socket_send_string(\";\", \"pc_connect\")#NewLineInJava\n"
                + "			socket_send_string(\"Fy: \", \"pc_connect\")\n"
                + "			socket_send_string(Fy, \"pc_connect\")\n"
                + "			socket_send_string(\";\", \"pc_connect\")\n"
                + "			socket_send_string(\"Fz: \", \"pc_connect\")\n"
                + "			socket_send_string(Fz, \"pc_connect\")\n"
                + "			socket_send_string(\";\", \"pc_connect\")\n"
                + "			sleep(0.5)\n"
                + "               global var_1 =   False\n"
                + "		end #EndWhile\n"
                + "	end #EndThread\n"
                + " threadId_SensorDataThread = run SensorDataThread() #RunThread\n";
        return threadSensorData;
    }

    public String initialization() {
        String initalization
                = "  modbus_add_signal(\"0.0.0.0\", 255, 0, 3, \"Modbus_1\")\n"
                + "  modbus_set_signal_update_frequency(\"Modbus_1\", 10)\n"
                + "  set_analog_inputrange(0, 0)\n"
                + "  set_analog_inputrange(1, 0)\n"
                + "  set_analog_inputrange(2, 0)\n"
                + "  set_analog_inputrange(3, 0)\n"
                + "  set_analog_outputdomain(0, 0)\n"
                + "  set_analog_outputdomain(1, 0)\n"
                + "  set_tool_voltage(0)\n"
                + "  set_runstate_outputs([])\n"
                + "  modbus_set_runstate_dependent_choice(\"Modbus_1\",0)\n"
                + "  set_payload(" + payloadUR + ")\n"
                + "  set_gravity([0.0, 0.0, 9.82])\n"
                + "  Base=p[0.0,0.0,0.0,0.0,0.0,0.0]\n"
                + "  Fx=0.0\n"
                + "  Fy=0.0\n"
                + "  Fz=0.0\n"
                + "  Mx=0.0\n"
                + "  My=0.0\n"
                + "  Mz=0.0\n";
        return initalization + threadSensorData();
    }

    public String ballrehab(String inA, String inV) {
        /*
    This method will simulate that of a ball being pulled out of the hand.
    The UR will try to pull a ball from the user, where the FT-150 force sensor
    will detect how much force the user is pulling with. The UR will then
    increase or decrease the velocity it will try to pull away with. If the
    force sensor does not detect any force (nobody is holding the ball) then it
    will push the ball towards the user until it detect force again.
         */
        String scriptName = "def ballrehab_v2():\n";
        String script
                = "  def push_z_axis():\n"
                + "    thread Thread_while_47():\n"
                + "      while (True):\n"
                + "        global position_increm = get_forward_kin()\n"
                + "        position_increm[0] = position_increm[0]-x_increment\n"
                + "        movel(position_increm,1.2,0.00001)\n"
                + "      end\n"
                + "    end\n"
                + "    if (norm(Fz) <Fz_max):\n"
                + "      global thread_handler_47=run Thread_while_47()\n"
                + "      while (norm(Fz) <Fz_max):\n"
                + "        sync()\n"
                + "      end\n"
                + "      kill thread_handler_47\n"
                + "    end\n"
                + "  end\n"
                + "  def rq_set_zero():\n"
                + "    	if(socket_open(\"127.0.0.1\",63350,\"acc\")):\n"
                + "    		socket_send_string(\"SET ZRO\",\"acc\")\n"
                + "    		sleep(0.1)\n"
                + "    		socket_close(\"acc\")\n"
                + "    	end\n"
                + "    end\n"
                + "  global Fx = 0.0\n"
                + "  global Fy = 0.0\n"
                + "  global Fz = 0.0\n"
                + "  global Mx = 0.0\n"
                + "  global My = 0.0\n"
                + "  global Mz = 0.0\n"
                + "  global Fx_max = 12\n"
                + "  global Fz_max = 12\n"
                + "  global Fz_tolerance = 5\n"
                + "  global x_increment = 0.002\n"
                + "  global z_increment = 0.004\n"
                + "  global y_increment = 0.004\n"
                + "  thread Thread_1():\n"
                + "    while True:\n"
                + "      while(1):\n"
                + "      	listofstuff = socket_read_ascii_float(6,\"stream\")\n"
                + "      	if(listofstuff[0] != 0):\n"
                + "      		Fx = listofstuff[1]\n"
                + "      		Fy = listofstuff[2]\n"
                + "      		Fz = listofstuff[3]\n"
                + "      		Mx = listofstuff[4]\n"
                + "      		My = listofstuff[5]\n"
                + "      		Mz = listofstuff[6]\n"
                + "      	end\n"
                + "#      	textmsg(Fz)\n"
                + "      end\n"
                + "    end\n"
                + "  end\n"
                + "  threadId_Thread_1 = run Thread_1()\n"
                + "    movej([3.2653818126748063, -0.5004661537747839, 1.2609107063460065, -3.216423783749357, -1.5145955848326498, 2.38019390734757], a=1.0, v=0.5)\n"
                + "  sleep(0.3)\n"
                + "  rq_set_zero()\n"
                + "  push_z_axis()\n"
                + "  sleep(0.5)\n"
                + "  global x_distance = 0\n"
                + "    while (norm(x_distance) < 5):\n"
                + "         position_increm = get_forward_kin()\n"
                + "#        global x_distance = x_distance+x_increment\n"
                + "    if (norm(Fz) > 10) and (norm(Fz) <= 20):\n"
                + "        speedl([(-0.001),0.0,0.0,0.0,0.0,0.0], 0.5, 0.008)\n"
                + "        textmsg(\"norm(Fz) > 10) and (norm(Fz) < 20\")\n"
                + "        textmsg(\"Force after contact Fz = \", Fz)\n"
                + "        global x_distance = x_distance+0.001\n"
                + "        textmsg(\"x_distance\", x_distance)\n"
                + "    elif (norm(Fz) > 20) and (norm(Fz) <= 35):\n"
                + "        textmsg(\"norm(Fz) > 20) and (norm(Fz) < 35\")\n"
                + "        textmsg(\"Force after contact Fz = \", Fz)\n"
                + "        global x_distance = x_distance+0.003\n"
                + "        textmsg(\"x_distance\", x_distance)\n"
                + "        speedl([(-0.003),0.0,0.0,0.0,0.0,0.0], 0.5, 0.008)\n"
                + "    elif (norm(Fz) > 35) and (norm(Fz) <= 40):\n"
                + "        textmsg(\"norm(Fz) > 20) and (norm(Fz) < 40\")\n"
                + "        textmsg(\"Force after contact Fz = \", Fz)\n"
                + "        global x_distance = x_distance+0.006\n"
                + "        textmsg(\"x_distance\", x_distance)\n"
                + "        speedl([(-0.006),0.0,0.0,0.0,0.0,0.0], 0.5, 0.008)\n"
                + "    elif (norm(Fz) > 40):\n"
                + "        textmsg(\"norm(Fz) > 40\")\n"
                + "        textmsg(\"Force after contact Fz = \", Fz)\n"
                + "        global x_distance = x_distance+0.009\n"
                + "        textmsg(\"x_distance\", x_distance)\n"
                + "        speedl([(-0.009),0.0,0.0,0.0,0.0,0.0], 0.5, 0.008)\n"
                + "    else:\n"
                + "        textmsg(\"DROPPED\")\n"
                + "        textmsg(\"Force after contact Fz = \", Fz)\n"
                + "        global x_distance = x_distance-0.002\n"
                + "        textmsg(\"x_distance\", x_distance)\n"
                + "        # 'DROPPED'\n"
                + "        speedl([(0.002),0.0,0.0,0.0,0.0,0.0], 0.5, 0.008)\n"
                + "    end\n"
                + "        textmsg(\"x_distance FINISHED?\", x_distance)\n"
                + "    end\n"
                + "    movej([3.360639076715726, -0.750901013913703, 1.8627477276646113, -3.7658198596698145, -1.665923337465497, 2.5039267622723], a=0.1, v=0.2)\n"
                + "    movej([3.560639076715726, -0.950901013913703, 2.2627477276646113, -3.7658198596698145, -1.665923337465497, 2.5039267622723], a=0.2, v=0.5)\n"
                + "join threadId_SensorDataThread\n"
                + "end";
        return scriptName + initialization() + script;
    }

    public String handshake(String inA, String inV) {
        /*
    This method will simulate the feeling of a handshake. The UR will wait
    until it detect force against the FT-150 force sensor. Then it will go through
    a couple of predetermined positions to simulate a handshake
         */
        String scriptName = "def handshake_v2():\n";
        String script
                = "  def push_z_axis():\n"
                + "    thread Thread_while_37():\n"
                + "      while (True):\n"
                + "        global position_increm = get_forward_kin()\n"
                + "        position_increm[2] = position_increm[2]-.005\n"
                + "        movel(position_increm,2.2,0.0001,0,0.0001)\n"
                + "      end\n"
                + "    end\n"
                + "    if (norm(Fx)<Fmax):\n"
                + "      global thread_handler_37=run Thread_while_37()\n"
                + "      while (norm(Fx)<Fmax):\n"
                + "        sync()\n"
                + "      end\n"
                + "      kill thread_handler_37\n"
                + "    end\n"
                + "  end\n"
                + "  \n"
                + "  def rq_set_zero():\n"
                + "    	if(socket_open(\"127.0.0.1\",63350,\"acc\")): \n"
                + "    		socket_send_string(\"SET ZRO\",\"acc\")\n"
                + "    		sleep(0.1)\n"
                + "    		socket_close(\"acc\")\n"
                + "    	end\n"
                + "    end\n"
                + "\n"
                + "  sleep(1.0)\n"
                + "  rq_set_zero()\n"
                + "  global Fx = 0.0\n"
                + "  global Fy = 0.0\n"
                + "  global Fz = 0.0\n"
                + "  global Mx = 0.0\n"
                + "  global My = 0.0\n"
                + "  global Mz = 0.0\n"
                + "  global Fmax = 10\n" //change this if you want to apply more force
                + "  thread Thread_1():\n"
                + "    while True:\n"
                + "      while(1):\n"
                + "      	listofstuff = socket_read_ascii_float(6,\"stream\")\n"
                + "      	if(listofstuff[0] != 0):\n"
                + "      		Fx = listofstuff[1]\n"
                + "      		Fy = listofstuff[2]\n"
                + "      		Fz = listofstuff[3]\n"
                + "      		Mx = listofstuff[4]\n"
                + "      		My = listofstuff[5]\n"
                + "      		Mz = listofstuff[6]\n"
                + "      	end\n"
                + "      end\n"
                + "    end\n"
                + "  end\n"
                + "  threadId_Thread_1 = run Thread_1()\n"
                + "  while (True):\n"
                + "    movej([3.200080809962689, -1.994541626691599, 2.663925097733759, -2.7613141184321828, -1.6226326173531431, 1.6340247019898373], a=1.3962634015954636, v=1.0471975511965976)\n"
                + "    sleep(0.5)\n"
                + "    movej([3.1886013797851094, -1.059109353239251, 2.0996290640173756, -4.214171099406416, -1.6178153424361694, 1.6320974468773706], a=1.3962634015954636, v=1.0471975511965976)\n"
                + "    sleep(0.5)\n"
                + "    push_z_axis()\n"
                + "    textmsg(\"Force after contact = \", Fz)\n"
                + "    textmsg(\"Force 1 sec later = \", Fz)\n"
                + "    sleep(0.3)\n"
                + "    movel(pose_trans(Base, p[0.46371057826150597,0.12275824616358655,0.3278104951907625,0.058349744030833324,1.445227432811873,0.04622116985412137]), a=1.2, v=0.25)\n"
                + "    movel(pose_trans(Base, p[0.5055859434607656,0.12467656626114328,0.25855195309048457,0.05609212946852178,1.7284970742543104,0.028514585372903946]), a=1.2, v=0.25)\n"
                + "    movel(pose_trans(Base, p[0.46371057826150597,0.12275824616358655,0.3278104951907625,0.058349744030833324,1.445227432811873,0.04622116985412137]), a=1.2, v=0.25)\n"
                + "    movel(pose_trans(Base, p[0.5055859434607656,0.12467656626114328,0.25855195309048457,0.05609212946852178,1.7284970742543104,0.028514585372903946]), a=1.2, v=0.25)\n"
                + "    movel(pose_trans(Base, p[0.46371057826150597,0.12275824616358655,0.3278104951907625,0.058349744030833324,1.445227432811873,0.04622116985412137]), a=1.2, v=0.25)\n"
                + "    movel(pose_trans(Base, p[0.5055859434607656,0.12467656626114328,0.25855195309048457,0.05609212946852178,1.7284970742543104,0.028514585372903946]), a=1.2, v=0.25)\n"
                + "    sleep(1.0)\n"
                + "    sleep(0.5)\n"
                + "  end\n"
                + "join threadId_SensorDataThread\n"
                + "end";
        return scriptName + initialization() + script;
    }

    public String handeye(String inA, String inV) { //Not testet YET!
        /*
    This method will have the user try to move his hand to the UR, it will then
    detect force through the FT-150 force sensor when the user touch the tip of
    the UR. It will then move to a different predetermied position and the user
    will have to touch the tip of the UR once more. This is to train hand eye
    coordination of the user.
         */
        String scriptName = "def handeye():\n";
        String script
                = "  def push_z_axis():\n"
                + "    thread Thread_while_51():\n"
                + "      while (True):\n"
                + "        global position_increm = get_forward_kin()\n"
                + "        varmsg(\"position_increm\",position_increm)\n"
                + "        position_increm[2] = position_increm[2]-.005\n"
                + "        movel(position_increm,2.2,0.0001,0,0.0001)\n"
                + "      end\n"
                + "    end\n"
                + "    if (norm(Fz)<Fmax):\n"
                + "      global thread_handler_51=run Thread_while_51()\n"
                + "      while (norm(Fz)<Fmax):\n"
                + "        sync()\n"
                + "      end\n"
                + "      kill thread_handler_51\n"
                + "    end\n"
                + "  end\n"
                + "  def rq_set_zero():\n"
                + "    	if(socket_open(\"127.0.0.1\",63350,\"acc\")): \n"
                + "    		socket_send_string(\"SET ZRO\",\"acc\")\n"
                + "    		sleep(0.1)\n"
                + "    		socket_close(\"acc\")\n"
                + "    	end\n"
                + "    end\n"
                + "  global Fx = 0.0\n"
                + "  global Fy = 0.0\n"
                + "  global Fz = 0.0\n"
                + "  global Mx = 0.0\n"
                + "  global My = 0.0\n"
                + "  global Mz = 0.0\n"
                + "  global Fmax = 8\n"
                + "  thread Thread_1():\n"
                + "    while True:\n"
                + "      while(1):\n"
                + "      	listofstuff = socket_read_ascii_float(6,\"stream\")\n"
                + "      	if(listofstuff[0] != 0):\n"
                + "      		Fx = listofstuff[1]\n"
                + "      		Fy = listofstuff[2]\n"
                + "      		Fz = listofstuff[3]\n"
                + "      		Mx = listofstuff[4]\n"
                + "      		My = listofstuff[5]\n"
                + "      		Mz = listofstuff[6]\n"
                + "      	end\n"
                + "      end\n"
                + "    end\n"
                + "  end\n"
                + "  threadId_Thread_1 = run Thread_1()\n"
                + "    movej([2.3597812121119945, -2.6554155312661014, 2.0940045125362365, -2.2006856657739915, -1.6548339300696657, 1.5697192686207784]," + inA + "," + inV + ")\n"
                + "    sleep(0.5)\n"
                + "   rq_set_zero()\n"
                + "  while (True):\n"
                + "    movej([2.3597812121119945, -2.6554155312661014, 2.0940045125362365, -2.2006856657739915, -1.6548339300696657, 1.5697192686207784]," + inA + "," + inV + ")\n"
                + "    sleep(0.5)\n"
                + "    push_z_axis()\n"
                + "    sleep(0.5)\n"
                + "    movej([2.971706895489564, -2.075837808367967, 2.2925625958333153, -3.350395146350983, -1.9576173017773657, 1.569395215179323]," + inA + "," + inV + ")\n"
                + "    sleep(0.5)\n"
                + "    push_z_axis()\n"
                + "    sleep(0.5)\n"
                + "    textmsg(\"FORTSOMFAEN 1 \")\n"
                + "    movel(pose_trans(Base, p[0.08553227176327999,-0.3129441826248693,0.3374102646331472,0.6726456817459714,1.3388897101437733,-0.8455655847392162])," + inA + "," + inV + ")\n"
                + "    sleep(0.5)\n"
                + "    push_z_axis()\n"
                + "    sleep(0.5)\n"
                + "    textmsg(\"FORTSOMFAEN 1 \")\n"
                + "    movel(pose_trans(Base, p[0.12579963594747545,-0.23599038250988408,0.7361827434885464,0.6643994012672705,1.4551519891084799,-0.4900663886874872])," + inA + "," + inV + ")\n"
                + "    sleep(0.5)\n"
                + "    push_z_axis()\n"
                + "    sleep(0.5)\n"
                + "    movel(pose_trans(Base, p[0.3663171643410643,0.008555546193374276,0.6897456833543845,0.35771901560902175,1.5716548823160623,-0.1967816952526886])," + inA + "," + inV + ")\n"
                + "    sleep(0.5)\n"
                + "    push_z_axis()\n"
                + "    sleep(0.5)\n"
                + "    movel(pose_trans(Base, p[0.2769653515359639,0.021988040857504797,0.38566288939025917,0.4101252280525745,1.4131672553666632,-0.26604284846445503])," + inA + "," + inV + ")\n"
                + "    sleep(0.5)\n"
                + "    push_z_axis()\n"
                + "    sleep(0.5)\n"
                + "    movel(pose_trans(Base, p[0.196367583520833,0.034782408671321555,0.3425156627555773,0.26793253121640853,1.1149430927142523,-0.26620128539673843])," + inA + "," + inV + ")\n"
                + "    sleep(0.5)\n"
                + "    push_z_axis()\n"
                + "    sleep(0.5)\n"
                + "  end\n"
                + "    join threadId_SensorDataThread\n"
                + "end";
        return scriptName + initialization() + script;

    }

    public String handshakeDynamic(String inA, String inV) {
        /*
    This method will simulate the feeling of a handshake. The UR will wait
    until it detect force against the FT-150 force sensor. Then it will follow
        the motion of the user
         */
        String scriptName = "def handshake_v2():\n";
        String script
                = "  def push_z_axis():\n"
                + "    thread Thread_while_47():\n"
                + "      while (True):\n"
                + "        global position_increm = get_forward_kin()\n"
                + "        position_increm[0] = position_increm[0]-x_increment\n"
                + "        movel(position_increm,1.2,0.00001)\n"
                + "      end\n"
                + "    end\n"
                + "    if (norm(Fy) <Fz_max):\n"
                + "      global thread_handler_47=run Thread_while_47()\n"
                + "      while (norm(Fz) <Fz_max):\n"
                + "        sync()\n"
                + "      end\n"
                + "      kill thread_handler_47\n"
                + "    end\n"
                + "  end\n"
                + "  def rq_set_zero():\n"
                + "    	if(socket_open(\"127.0.0.1\",63350,\"acc\")):\n"
                + "    		socket_send_string(\"SET ZRO\",\"acc\")\n"
                + "    		sleep(0.1)\n"
                + "    		socket_close(\"acc\")\n"
                + "    	end\n"
                + "    end\n"
                + "  global Fx = 0.0\n"
                + "  global Fy = 0.0\n"
                + "  global Fz = 0.0\n"
                + "  global Mx = 0.0\n"
                + "  global My = 0.0\n"
                + "  global Mz = 0.0\n"
                + "  global Fx_max = 12\n"
                + "  global Fz_max = 7\n"
                + "  global Fz_tolerance = 5\n"
                + "  global x_increment = 0.002\n"
                + "  global z_increment = 0.004\n"
                + "  global y_increment = 0.004\n"
                + "  thread Thread_1():\n"
                + "    while True:\n"
                + "      while(1):\n"
                + "      	listofstuff = socket_read_ascii_float(6,\"stream\")\n"
                + "      	if(listofstuff[0] != 0):\n"
                + "      		Fx = listofstuff[1]\n"
                + "      		Fy = listofstuff[2]\n"
                + "      		Fz = listofstuff[3]\n"
                + "      		Mx = listofstuff[4]\n"
                + "      		My = listofstuff[5]\n"
                + "      		Mz = listofstuff[6]\n"
                + "      		sleep(0.2)\n"
                + "      	end\n"
                + "#      	textmsg(Fz)\n"
                + "      end\n"
                + "    end\n"
                + "  end\n"
                + "  threadId_Thread_1 = run Thread_1()\n"
                + "    movej([3.1886013797851094, -1.059109353239251, 2.0996290640173756, -4.214171099406416, -1.6178153424361694, 1.6320974468773706], a=1.3962634015954636, v=1.0471975511965976)\n"
                + "  sleep(0.3)\n"
                + "  rq_set_zero()\n"
                + "  push_z_axis()\n"
                + "  sleep(0.5)\n"
                + "  global x_distance = 0\n"
                + "  global timeout = 0\n"
                + "    while (norm(x_distance) < 10):\n"
                + "         position_increm = get_forward_kin()\n"
                + "#        global x_distance = x_distance+x_increment\n"
                + "    if (Fy > 5): # press ned = positiv verdi\n"
                + "        speedj([0,0.1,0.05,0.1,0,0], 1.3, 0.008) # positiv beveger seg opp\n"
                + "        global x_distance = x_distance-0.1\n"
                + "        global timeout = 0\n"
                + "    elif (Fy < (-5)): # press opp = negativ verdi\n"
                + "        global x_distance = x_distance+0.1\n"
                + "        speedj([0,(-0.1),(-0.05),(-0.1),0,0], 1.3, 0.008) # positiv beveger seg opp\n"
                + "        global timeout = 0\n"
                + "    else:\n"
                + "        # 'DROPPED'\n"
                + "        speedl([(0.001),0.0,0.0,0.0,0.0,0.0], 0.5, 0.008)\n"
                + "        if(timeout >= 100):\n"
                + "        	global x_distance = 10\n"
                + "        end        \n"
                + "        global timeout = timeout+1\n"
                + "    end\n"
                + "    end\n"
                + "    sleep(0.5)\n"
                + "    movej([3.360639076715726, -0.750901013913703, 1.8627477276646113, -3.7658198596698145, -1.665923337465497, 2.5039267622723], a=0.1, v=0.2)\n"
                + "    movej([3.560639076715726, -0.950901013913703, 2.2627477276646113, -3.7658198596698145, -1.665923337465497, 2.5039267622723], a=0.2, v=0.5)\n"
                + "    join threadId_SensorDataThread\n"
                + "end";
        return scriptName + initialization() + script;
    }

}
