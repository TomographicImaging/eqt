# Version 1.0.2
- Upgrade python to 3.8 in `test.yml` (#171)
- Rename `/scripts` directory to `/recipe` (#161)
- Update `CONTRIBUTING.md` with detailed installation and contribution instructions (#161)
- Limit Python version to <3.12 in conda recipe (#161)
- Change SessionDirectorySelectionDialog `.open()` call to `.exec()` (#163, #165)

# Version 1.0.1
- Add NoBorderScrollArea, example and tests (#155)
- Edit next and prev in UIMultiStepWidget (#151)
- Remove question mark from form dialog (#150)

# Version 1.0.0
- Update "pre-commit-config.yaml" (#136)
- Change order of widget states (#129)
- Adds the class `AdvancedDialogForm` & tests/example;
deprecates `getWidgetStates` to be `getSavedWidgetStates` (#124)
- Edits 'contributing.md' and 'README.md (#131, #133)
- Adds unit test for `addWidget` and `addSpanningWidget`; adds `getIndexFromVerticalLayout`
to `FormDialog` (#123)
- Initialises `widget_states` in init (#132)
- Adds methods to insert widgets in the forms & tests/example; removes `_addWidget`;
adds `getWidgetRow`and updates states dictionary and related methods; adds
`getNameAndRole*`; changes `num_widgets` to be a property (#109)
- Reinstates changelog (#99)
- Adds `title` to `FormDockWidget` & update tests/examples (#102)
- Stops `pre-commit` committing corrections to user PRs (#112)
- Updates `pre-commit` dependencies (#111, #104, #96, #88, #84, #82, #81)
- Fixes failing unit tests (#106)
- Adds `removeWidget` & `getNumWidgets` form methods (#93, #70)
  + Adds `addSpanningWidget` method to `FormDockWidget` (#93)
  + update examples/tests
- Creates `eqt_env.yml` conda environment configuration with all prerequisites (#91)
- Fixes `find_packages` build bloat & development installation bug (#89)
- Adds user-defined function for `FormDialog` "Cancel" button (#85)
- Update installation instructions (#83, #76)
- Fixes linter errors (#81)
- Fixes CI release tags

# Version 0.7.1
- add code linting (#79)
  + add `pre-commit` config
  + automated lint
    * fix `git-blame` attribution
  + manual fixes
- misc code tidy (#77)
  + esp. reduce duplication in `test/test__formUI_status_test.py`
- misc metadata updates
  + migrate `unittest` => `pytest` (#77)
    * fix & update some tests
  + add CI tests & update workflows (#77 <- #11, #54)
    * purge conda packaging (will do in upstream `conda-forge` repo instead) (#76, #56)
  + migrate `setup.py` => `pyproject.toml` (#77)
    * use SCM versioning
    * drop unused `sphinx` dependency
  + update README/CONTRIBUTING (#79)
  + rename repo from https://github.com/paskino/qt-elements to https://github.com/TomographicImaging/eqt (#77)
  + exclude `/examples/` from `*.whl` distribution (#79)
  + add `qdarkstyle` dependency (#77)
  + minify licen[cs]e (#77)
  + purge changelog (see https://github.com/paskino/qt-elements/releases or https://github.com/TomographicImaging/eqt/blob/main/CONTRIBUTING.md#changelog instead) (#77)
  + enforce annotated tags for releases (#77)

# Version v0.7.0
- Adds `MainWindowWithProgressDialogs` a base class for a main window, with a menu bar, and ability to create ProgressTimerDialogs.
- Renames `SessionMainWindow` to `MainWindowWithSessionManagement`
- Removed addToMenu method from `MainWindowWithProgressDialogs` (and therefore `MainWindowWithSessionManagement` which inherits from it) as it didn't do anything, and the user can add their own method and call it if needed.
- Check if session folder loaded from QSettings exists before writing to it.

# Version v0.6.0
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

# Version v0.5.0
- Add getWidgets method to FormWidget, FormDockWidget and FormDialog
- Add setWidgetVisibility method to FormWidget, FormDockWidget and FormDialog

# Version v0.4.0
- Add `ReOrderableListWidget` and `ReOrderableListDockWidget`
- Add example of using the `ReOrderableListWidget`
- Add `getWidget` method to `FormWidget`, `FormDockWidget` and `FormDialog`

# Version v0.3.0
- Add ProgressTimerDialog and example.
- Delete ErrorObserver, as this is relevant to VTK, not Qt, so it has been moved to the CILViewer repo.

# Version v0.2.2
* By default, automatically number the tab titles in a `StackedWidget`

# Version v0.2.1
- Adds methods to add titles and separators to the FormWidget
- Adds UIMultiStepWidget
- Adds version string from git describe
- Added unit tests and a way to disable interactive tests if run on conda build

# version 0.1.1

# Version v0.1.0
* Fixes FormDockWidget by setting a FormWidget as the DockWidget's widget
* Allows a widget to be added to a FormWidget, which spans the width of the form
* Adds a factory for creating a StackedWidget
* Adds UISliderWidget

# Version v0.0.7
* bump version number (#5)

# Version v0.0.6
sync version number

# Version v0.0.5
mainly just a github action

# Version v0.0.4
* Create `python-publish.yml` (#3)
