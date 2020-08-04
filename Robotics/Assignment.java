import ShefRobot.Robot;
import ShefRobot.Motor;
import ShefRobot.Sensor;
import ShefRobot.UltrasonicSensor;

public class Assignment {

  /**
   * The main method
   *
   * @param args The standard command line string array
   */
  public static void main(String[] args) {
    // Basic robot settings
    Robot myRobot = new Robot("192.168.137.13");
    Motor leftMotor = myRobot.getLargeMotor(Motor.Port.A);
    Motor rightMotor = myRobot.getLargeMotor(Motor.Port.D);
    UltrasonicSensor leftSensor = myRobot.getUltrasonicSensor(Sensor.Port.S4);
    UltrasonicSensor rightSensor = myRobot.getUltrasonicSensor(Sensor.Port.S1);

    // Helpers classes
    Movement movement = new Movement(leftMotor, rightMotor);
    Controller control = new Controller(movement, leftSensor, rightSensor);

    // Start the loop
    control.startLoop();

    myRobot.close();
  }
}
