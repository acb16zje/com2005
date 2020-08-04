import ShefRobot.TouchSensor;
import ShefRobot.UltrasonicSensor;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.math.RoundingMode;
import java.text.DecimalFormat;
import javax.swing.JFrame;

public class Controller {

  // Reference input
  private float distance = 10;

  // Last error signal
  private float lastError = 0;

  // Proportional gain, Kp
  private float kP = 70;

  // Delta time between sensors checking
  private float dT = 0.099f;

  // Integral gain
  private float kI = 220.791f * dT;
  private float integral = 0;

  // Derivative gain
  private float kD = 10.435f / dT;

  // Control / Feedback elements
  private Movement movement;
  private UltrasonicSensor leftSensor;
  private UltrasonicSensor rightSensor;

  // Constants
  private final int INIT_SPEED = 300;
  private final float STRAIGHT_MULT = 2f;
  private final float TURN_MULT = 1.7f;

  private boolean right = false;
  private boolean left = false;
  private boolean forward = false;

  /**
   * Controller constructor
   *
   * @param movement Movement object instance
   * @param lSensor Left ultrasonic sensor instance
   * @param rSensor Right ultrasonic sensor instance
   */
  public Controller(Movement movement, UltrasonicSensor lSensor,
      UltrasonicSensor rSensor) {
    this.movement = movement;
    this.leftSensor = lSensor;
    this.rightSensor = rSensor;
  }

  /**
   * Start the negative feedback control loop
   */
  public void startLoop() {
    // Move slowly initially
    movement.setSpeed(INIT_SPEED);
    movement.forward();

    while (true) {
      float leftDistance = leftSensor.getDistance();
      float rightDistance = rightSensor.getDistance();

      // Do nothing if Infinity is detected
      if (Float.isInfinite(leftDistance) || Float.isNaN(leftDistance) ||
          Float.isInfinite(rightDistance) || Float.isNaN(rightDistance)) {
        continue;
      }

      float error = round(leftDistance - rightDistance) * 100;

      // Control signal, u
      float u = controlSignal(error);
      System.out.println(u);

      int speed = Math.abs(Math.round(u)) + INIT_SPEED;

      if (u == 0 || forward) {
        // Move forward
        forward = false;
        movement.setSpeed((int) (INIT_SPEED * STRAIGHT_MULT));

      } else if (u > 0 || left) {
        // Turn left
        if (speed > INIT_SPEED * TURN_MULT) {
          speed = (int) (INIT_SPEED * TURN_MULT);
        }
        left = false;
        movement.setSpeed(INIT_SPEED, speed);

      } else if (u < 0 || right) {
        // Turn right
        if (speed > INIT_SPEED * TURN_MULT) {
          speed = (int) (INIT_SPEED * TURN_MULT);
        }
        right = false;
        movement.setSpeed(speed, INIT_SPEED);
      }

      movement.forward();
    }

  }

  /**
   * Calculate the control signal
   *
   * @return The control signal `u` to be sent to the motors
   */
  private float controlSignal(float error) {
    // Integral term
    integral = 2 / 3 * (integral + error);

    // Derivative term
    float derivative = error - lastError;
    lastError = error;

    return (kP * error) + (kI * integral) + (kD * derivative);
  }

  /**
   * Round the actual distance to 4 decimal places
   *
   * @param actualDistance The distance returned by the ultrasonic sensor
   * @return The rounded actual distance to 4 decimal places
   */
  private float round(float actualDistance) {
    DecimalFormat df = new DecimalFormat("#.####");
    df.setRoundingMode(RoundingMode.CEILING);

    return Float.parseFloat(df.format(actualDistance));
  }
}
