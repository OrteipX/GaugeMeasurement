/*
  ___       _       _     __  __
 / _ \ _ __| |_ ___(_)_ __\ \/ /
| | | | '__| __/ _ \ | '_ \\  /
| |_| | |  | ||  __/ | |_) /  \
 \___/|_|   \__\___|_| .__/_/\_\
                     |_|

Developer: Ramon Garcia
Date: Oct 22, 2019

Project: Arduino project to control step motor to work with different angles.
Board: Black Board Uno R3
Version: 1.0
*/

#include <Servo.h>
#include <string.h>

Servo servo;
const char COMMAND_01[] = {"ResetServo"};
const char COMMAND_02[] = {"RotateClockwise"};
const char COMMAND_03[] = {"RotateCounterClockwise"};
const char COMMAND_04[] = {"GetAngle"};
const unsigned short BAUDRATE = 57600;
const unsigned short INITIAL_ANGLE = 0;
const unsigned short FINAL_ANGLE = 175;
const unsigned short SERVO_PIN = 9;
const unsigned short MAX_INPUT  = 128;
const unsigned short SERVO_SPEED = 1;
short angle = 0;

void resetServo(int currentAngle);
short getAngle();
void rotateServo(short angle);

void setup()
{
    // serial attach
    Serial.begin(BAUDRATE);
    while (!Serial);

    // servo initialization
    servo.attach(SERVO_PIN);
    servo.write(INITIAL_ANGLE);
}

void loop()
{
    char serialData[MAX_INPUT] = { '\0' };

    while (!Serial.available());
    int size = Serial.readBytesUntil('\n', serialData, MAX_INPUT);

    // reset servo to initial position
    if (strcmp(serialData, COMMAND_01) == 0)
    {
        int currentAngle = getAngle();
        resetServo(currentAngle);

        Serial.print("...Servo Reset...");
    }
    // rotate servo clockwise
    else if (strcmp(serialData, COMMAND_02) == 0)
    {
        short angle = getAngle();

        if (angle > INITIAL_ANGLE)
            rotateServo(--angle);
    }
    // rotate servo counter clockwise
    else if (strcmp(serialData, COMMAND_03) == 0)
    {
        short angle = getAngle();

        if (angle < FINAL_ANGLE)
            rotateServo(++angle);
    }
    // get servo angle
    else if (strcmp(serialData, COMMAND_04) == 0)
    {
        Serial.println(getAngle());
    }
}

short getAngle()
{
    return servo.read();
}

void rotateServo(short angle)
{
    servo.write(angle);
}

void resetServo(int currentAngle)
{
    if (currentAngle > INITIAL_ANGLE)
    {
        for (int i = currentAngle; i > INITIAL_ANGLE; i--)
        {
            servo.write(i);
            delay(SERVO_SPEED / 5);
        }
    }
    else if (currentAngle < INITIAL_ANGLE)
    {
        for (int i = currentAngle; i < INITIAL_ANGLE; i++)
        {
            servo.write(i);
            delay(SERVO_SPEED / 5);
        }
    }
}
