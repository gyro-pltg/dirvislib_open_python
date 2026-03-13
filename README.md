Free-to-use and open Python library made for radio frequency propagation analysis.
This library features functions that can help this process in different ways, such as modeling a radio wave's path through earth surface along its slice or estimating what a coverage parameters of a given area look like.
These functions use a calculation method that utilizes both earth curvature and land topography (fed from the manually imported .hgt files)

Please note that so far this library is meant for estimation uses and hobby projects rather than the professional use. As for early March 2026, the abovementioned calculation method doesn't imply complex factors like frenzel zones or terrain signal reflections, and the functions themselves imply that the possibility to receive signal from one point on Earth to other is a binary value determined by presence of obstructions on its path. 

Please also note that as for 13th of March 2026 this package is still in a testing mode stage and doesn't support working with coordinates outside of the positive geographical coordinate value scopes (0-90 N, 0-180 E)
