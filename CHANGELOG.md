
## v0.7.0
- Adds `MainWindowWithProgressDialogs` a base class for a main window, with a menu bar, and ability to create ProgressTimerDialogs.
- Renames `SessionMainWindow` to `MainWindowWithSessionManagement`
- Removed addToMenu method from `MainWindowWithProgressDialogs` (and therefore `MainWindowWithSessionManagement` which inherits from it) as it didn't do anything, and the user can add their own method and call it if needed.
- Check if session folder loaded from QSettings exists before writing to it.

## v0.6.0
- Use pip install in the conda recipe, instead of setup.py install
- Adds the following new methods to UIFormWidget, FormWidget, FormDialog and FormDockWidget:
   - `saveAllWidgetStates` - Saves the state of all widgets in the form. This can be used to restore the state of the widgets using the restoreAllSavedWidgetStates method.

   - `restoreAllSavedWidgetStates` - Restores the state of all widgets in the form to the state saved by the saveAllWidgetStates method. If the saveAllWidgetStates method has not been called, this method will do nothing.

   - `getAllWidgetStates` - Returns a dictionary of the state of all widgets in the form.

   - `getWidgetState` - Returns the state of the widget.

   - `applyWidgetState` - Applies the given state to the widget with the given name.

   - `applyWidgetStates`  - Applies the given state to the widgets in the form given by the keys of the state dictionary.

- Adds an example of a FormDialog: `dialog_save_state_example.py` where all of the widgets are saved and restored if you press "Ok", whereas the previous values of the dialog are restored if you press "Cancel".
- Adds unit tests to cover: `saveAllWidgetStates`, `restoreAllSavedWidgetStates`, `getAllWidgetStates`, `getWidgetState`, `applyWidgetState`, `applyWidgetStates`
- setup.py:
  - Always normalise the version from git describe to pep440
- Adds `SessionsMainWindow.py` - which is a base class for our apps which create a session folder where any files generated in the app are saved, and provides the ability to permanently save and reload sessions.
- Adds `SessionsMainWindow_example.py` - an example of using the SessionsMainWindow - you can run this example, change the state of widgets in the form, save the session, reload the session and see the state of the widgets be restored.
- Adds `SessionsDialogs.py` - the dialogs used by the SessionsMainWindow.py
- Adds `io.py` - contains method for zipping a directory, used by SessionsMainWindow.py
- Adds unit tests to cover `SessionsDialogs.py`, `io.py`, and a large proportion of `SessionsMainWindow.py`

## v0.5.0
* Add getWidgets method to FormWidget, FormDockWidget and FormDialog
* Add setWidgetVisibility method to FormWidget, FormDockWidget and FormDialog 

## v0.4.0
* Add ReOrderableListWidget and ReOrderableListDockWidget
* Add example of using the ReOrderableListWidget
* Add getWidget method to FormWidget, FormDockWidget and FormDialog

## v0.3.0
* Add ProgressTimerDialog and example.
* Delete ErrorObserver, as this is relevant to VTK, not Qt, so it has been moved to the CILViewer repo.

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

