# FragClean User Guide — ZBrush 2022.0.5 / 2025.0.1

FragClean finds and deletes small loose pieces that are not connected to the main body of a SubTool,
as a check before Boolean operations on 3D-print parts.
The plugin comes in an English and a Chinese version with the same features.

## Before you start
- **Save your ZTL before cleaning.** Cleaning runs many steps (duplicate, split, delete, merge, import).
  Reopening the saved ZTL is the safest way back if something goes wrong.
- **Lost after cleaning: Layers and Morph Targets.**
- **Kept after cleaning: UVs, Polygroups, the SubTool name, its position and its folder.**
- **SubTools with subdivision levels cannot be processed.** The plugin shows a reminder.
  Remove the levels first: Geometry > Del Lower / Del Higher until only one level is left.

## Installation (once per computer)
1. Double-click `install.bat` and choose **2 = English** (1 is the Chinese version).
   It looks for ZBrush in the usual places, copies the plugin into `ZStartup\ZPlugs64\` and creates the temp folder
   `C:\Users\Public\Documents\ZBFragClean\`.
   If it cannot find ZBrush, drag your ZBrush folder (the one with ZBrush.exe) into the window and press Enter.
   If ZBrush is under C:\Program Files and the copy fails, right-click install.bat > Run as administrator.
2. Start ZBrush, press **Ctrl+Shift+L** (ZScript > Load) and pick `ZStartup\ZPlugs64\FragClean.txt`.
   This creates `FragClean.zsc`, which ZBrush then loads automatically on every start.
   (ZBrush does not compile .txt files in the plugin folder by itself, so this step is required.)
3. The buttons are in **ZPlugin > FragClean**.

> To switch languages, run install.bat again, pick the other language, restart ZBrush and repeat step 2.

## Buttons
| Button | What it does | Changes the model |
|---|---|---|
| Detect Current | Counts the loose pieces of the selected SubTool | No |
| Detect All | Checks every visible SubTool and shows a summary | No |
| Clean Current | Deletes the loose pieces of the selected SubTool | Yes |
| Clean All | Cleans every visible SubTool (asks first) | Yes |
| Close Holes | Runs Close Holes before cleaning, as in the manual workflow. On by default | — |
| Keep % | Pieces with at least this percent of the largest piece's faces are kept too. Default 10. 100 = keep only the largest piece | — |

## First run after each ZBrush start
ZBrush asks "This is not an undoable operation" (once each for split, delete and merge):
- **Choose "Always OK"** each time. ZBrush stops asking until it is restarted.
- If "Mesh does not contain multiple parts" appears, click it to close it (only possible at the start).
- Do not choose Cancel, or the plugin stops.

After that the plugin runs without any prompts.

## Subdivision levels
- **Detect Current / Clean Current**: a reminder says the SubTool has subdivision levels; nothing is changed.
- **Detect All / Clean All**: a reminder lists the SubTools with subdivision levels. Choose Continue to skip them
  and process the rest, or Cancel. If every visible SubTool has levels, you only get the reminder.

## How it works
Manual workflow: Solo > Close Holes > Auto Groups > Ctrl+Shift-click the body > Del Hidden.
The plugin instead:
1. (optional) runs Close Holes on the SubTool,
2. duplicates it and runs Split To Parts on the copy,
3. counts the faces of every piece; the largest is the body, pieces above Keep % stay too,
4. deletes the other pieces, merges the kept ones, exports them as OBJ, imports that back into the
   original SubTool and removes the temporary SubTools.

## Notes
- Detection also counts pieces that are separate on purpose (for example two eyes in one SubTool). Check the report.
- Ctrl+Z undoes the import step; to go back completely, reopen the ZTL you saved before cleaning.
