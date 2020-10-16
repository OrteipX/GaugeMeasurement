# Gauge Measurement Device

The gauge measurement device is a project which consists of a Mitutoyo Gauge working alongside to a step motor that is going to collect dimension for the analyzed part.

## Before usage
Use the package manager pip to 
install matplotlib.
```
pip install matplotlib
```

## Usage
Connect the device through the USB cable, get the port's name, and change in the main.py.

### Example:
```
    ser_arduino = SerialInterface(port = "COM9")
    ser_arduino.connect()
    ser_gauge = SerialInterface(port = "COM10", baudrate = 9600)
    ser_gauge.connect()
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update the tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
