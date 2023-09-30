# SceneSettings

Save, load and compare scene parameters  
  
**[Download latest](https://github.com/Pullusb/SceneSettings/archive/master.zip)**  
  
**[Latest 2.7 version](https://github.com/Pullusb/SceneSettings/releases/tag/v0.0.1)**

---
### Description

**Settings filepath/filebrowser**  
Save the scene parameters (and the lights parameter) to a json file.
(If the field is left empty the json will be created in the blend's folder.)

**Compare**  
Print the parameters differences between saved json and current scene in the console.

**stamp changes**  
If ticked, place the text of 'compare' in the *stamp output note* (usefull when you save a series of render while tweaking settings)

### where ?

The panel is located in properties > scene

![scene Settings panel](https://github.com/Pullusb/images_repo/raw/master/blender_SceneSettings_panel.png)


---

### Changelog

0.3.0

- added: selective laod properties with compare button
- fixed: possible errors when setting properties

0.2.0

- update for Blender 3+
- added: New multi scene apply with select popup
    - copy settings loaded file (same as existing `Load file`)
    - copy settings from active scene to the others

0.1.0

- update to 2.9
- code cleanup