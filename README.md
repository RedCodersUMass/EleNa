# EleNa : Elevation Based Navigation System

## Team Name
### Redcoders

## Team Members
```
Vijaya Gajanan Buddhavarapu
Supriya Shreekant Jahagirdar
Mrinal Tak
Sirisha Annamraju
Devyani Varma
```

# Demo of the project
```
https://www.youtube.com/watch?v=ubCXJt6fU9o
```

# Getting the setup done

### Installing the dependencies
with pip:
```
pip install -r requirements.txt
```

# How to run the app

### Running the application
- Execute ```launch.sh``` to get the flask app started.
- Open the browser and go to `http://127.0.0.1:5000/view`.


# Adding Input

## Mode of Input

### Select Map
This option lets you select origin and destination points on MAP by clicking the map.

- Choose the `Select Map` button from right side `Mode of Input panel`
- Select any one point on Map(This would be origin)
- Select other point on Map(This would be destination)

### Enter Fields Manually
This option lets you enter origin and destination manually by entering in fields in text box

- Choose the `Enter Fields Manually` button from right side `Mode of Input panel`
- Type origin address in `Origin` text box on left side panel `Input` (For eg: Umass police department)
- Type destination address in `Destination` text box on left side panel `Input`(For eg: Umass amherst)


### Path Limit
You can enter path limit - % of shortest distance one wants to minimize or maximize

- Type the path limit percentage (without %) in `Path Limit` text box on left side panel `Input` (For eg: 50)

### Min/Max Elevation
There are two elevation strategy:
- ```Minimize Elevation``` This selects the elevation strategy to minimize.
- ```Maximize Elevation``` This selects the elevation strategy to maximize.

### Choice of Algorithms
We have two algorithms to choose from
- ```Dijkstra``` This selects the algorithm to Dijkstra.
- ```A*``` This selects the algorithm to A*.

# Steps to add Input

### Mode of Input - Selecting points on Map
- Choose the `Select Map` button from right side Mode of Input panel
- Select any one point on Map(This would be origin)
- Select other point on Map(This would be destination)
- Choose `Elevation option` (Minimize Elevation/Maximize Elevation) from left side Min/Max Elevation panel
- Choose `Algorithm option` (A* Algorithm/Dijkstra Algorithm) from left side Algorithm panel
- Click on `Submit Values` button to submit the request to the system

### Mode of Input - Entering Fields Manually in Text Box
- Choose the `Enter Fields Manually` button from right side Mode of Input panel
- Type origin address in `Origin text box` on left side panel Input(For eg: Umass police department)
- Type destination address in `Destination text box` on left side panel Input(For eg: Umass amherst)
- Choose `Elevation option` (Minimize Elevation/Maximize Elevation) from left side Min/Max Elevation panel
- Choose `Algorithm option` (A* Algorithm/Dijkstra Algorithm) from left side Algorithm panel
- Click on `Submit Values` button to submit the request to the system

### Reset Fields
This button resets the UI to default settings.

# Documentation

### Evaulation and desgin report
- ```Evaluation and Design Document```

### White Box testing
- ```UI Testing Report```

### Automated testing using unittest framework
- Go to test directory and run the files `MVCTestSuite.py` and `AlgorithmTestSuite.py`

### Console Logs
One can view console logs on console. It contains metrics of shortest route and elevation route along with request
and response.
