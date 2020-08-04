import ShefRobot.Motor;

public class Movement {

  // Motors
  private Motor leftMotor;
  private Motor rightMotor;

  /**
   * Movement constructor
   *
   * @param leftMotor The left motor
   * @param rightMotor The right motor
   */
  public Movement(Motor leftMotor, Motor rightMotor) {
    this.leftMotor = leftMotor;
    this.rightMotor = rightMotor;
  }

  /**
   * Set the speed of both left and right motor
   *
   * @param speed The desired speed of the motors
   *
   */
  public void setSpeed(int speed) {
    leftMotor.setSpeed(speed);
    rightMotor.setSpeed(speed);
  }

  /**
   * Set the speed of both left and right motor individually
   *
   * @param lSpeed The desired speed of left motor
   * @param rSpeed The desired speed for right motor
   */
  public void setSpeed(int lSpeed, int rSpeed) {
    leftMotor.setSpeed(lSpeed);
    rightMotor.setSpeed(rSpeed);
  }

  /**
   * Move forward
   */
  public void forward() {
    leftMotor.forward();
    rightMotor.forward();
  }
}
