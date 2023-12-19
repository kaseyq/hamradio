Control ham radio setup with multiple accessory controls.


The following options are available:
-m	Mock usage, do not use hardware interfaces
-v	Verbose log output
-a	Action name. Followed by the action name and arguments

	Actions:

	Frequency <float megahertz>
		-a Frequency 14.09570

	Tune
		-a Tune

	RotateTo <float degrees>
		-a RotateTo 30

	Power <int power>
		-a Power 50

	Examples:

	20 meters WSPR band:
	$ python3 ./ -a Frequency 14.09570

	Tune and Rotate to 30 degrees
	python3 ./ -a Tune -a RotateTo 30

	Set frequency to 14.09 mhz, then tune, then rotate to 30 degrees
	python3 ./ -m -a Frequency 14.09 -a Tune -a RotateTo 30
