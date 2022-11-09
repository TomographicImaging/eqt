## v0.3.0
* Add ProgressTimerDialog and example.
* Delete ErrorObserver, as this is relevant to VTK, not Qt, so it has been moved to the CILViewer repo.
* Add getWidget method to FormWidget, FormDockWidget and FormDialog

## v0.2.2
* By default, automatically number the tab titles in a StackedWidget

## v0.2.1
* Adds methods to add titles and separators to the FormWidget
* Adds UIMultiStepWidget
* Adds version string from git describe
* Added unit tests and a way to disable interactive tests if run on conda build

## v0.2.0
* Adds methods to add titles and separators to the FormWidget
* Adds version string from git describe
* Added unit tests and a way to disable interactive tests if run on conda build
* Adds UIMultiStepWidget

## v0.1.0
* Fixes FormDockWidget by setting a FormWidget as the DockWidget's widget
* Allows a widget to be added to a FormWidget, which spans the width of the form
* Adds a factory for creating a StackedWidget
* Adds UISliderWidget

