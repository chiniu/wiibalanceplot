wiiblanceplot
=============

What is this
------------
Use wii blance board to track barycentre and draw on display.
Combine below two 

* GUI [scalesgui.py](http://abstrakraft.org/cwiid/ticket/63)

* BT communication use [wiiboard-simple](https://code.google.com/p/wiiboard-simple/)

Requirements
-----------
* python-pygame
* python-bluez
* bluez-utils
* Bluetooth

Usage
-----
 
    ./blanceplot.py

Filiter for AD convert
-------
* [Sample code](http://blog.csdn.net/lxc1014/article/details/17138991)

	     public void onSensorChanged(SensorEvent event)
	     {
	          // alpha is calculated as t / (t + dT)
	          // with t, the low-pass filter's time-constant
	          // and dT, the event delivery rate
	
	          final float alpha = 0.8;
	
	          gravity[0] = alpha * gravity[0] + (1 - alpha) * event.values[0];
	          gravity[1] = alpha * gravity[1] + (1 - alpha) * event.values[1];
	          gravity[2] = alpha * gravity[2] + (1 - alpha) * event.values[2];
	
	          linear_acceleration[0] = event.values[0] - gravity[0];
	          linear_acceleration[1] = event.values[1] - gravity[1];
	          linear_acceleration[2] = event.values[2] - gravity[2];
	     }

* [Methodology](http://chamberplus.blogspot.tw/2010/04/ad.html)

Sample Rate
-----------
According to log, 100 saples in 1000 ms