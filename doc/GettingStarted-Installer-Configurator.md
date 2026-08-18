# Getting Started - Menuconfig Configurator / Installer

The all _“new”_ Happy Hare v4 Installer and Configurator is a dynamic, _menuconfig_ 
rules based configuration management system that has been designed to streamline the
initial installation and ongoing management of Happy Hare configurations. It employs a
structured, deterministic workflow, exposing only the configuration parameters and 
capabilities relevant to your particular MMU system and the features it supports 
and you have enabled.

Where possible, the installer applies recommended defaults and sensible settings across
hardware definitions, GPIO assignments, and various Happy Hare capabilities. Configuration
options not applicable to your MMU or configuration are suppressed and omitted from the
generated configuration files stored in the `config/mmu/base/` directory. 

This rules driven approach simplifies setup, reduces configuration errors / 
frustration, and provides a clear foundation for upgrading, managing, and 
enabling Happy Hare capabilities.

## Design Goal
The intention is for users to manage the majority of configurable settings using the 
interactive menuconfig installer (`./install.sh -i`), without needing to edit Happy Hare
configuration files directly. The rules‑driven interface ensures configuration
choices always remain consistent with the selected MMU hardware and supported features.

## Direct Modification of Configuration Files
Direct modification of Happy Hare configuration files remains possible when required, 
with installer options to control merge and overwrite behavior to accommodate your preferred 
configuration workflow. 

All all `menuconfig` configuration selections are mastered and stored in the
`config/mmu/.mmu-config` settings file to enable them to be back backed up along with other
configuration by popular GitHub printer backup mechanisms.

## Navigation
<p align="center">
  <img src="GettingStarted-Installer-Configurator/GettingStarted-Installer-Configurator.png" alt="Menuconfig installer and configurator" align=right width="60%">
</p>

Navigation is intuitive and the same as any other `menuconfig` based interface.


| Key | Purpose |
| --- | ------- |
| **↑**   | move up |
| **↓**   | move down |
| **↵ or space**   | select a menu or option |
| **Esc** | go back to the previous menu |
| **R**   | reset a setting to its default value (if available) |
| **Q**   | quit and selectively save configuration changes |


The top-down flow guides you through the process in a logical, step by step manner. 
Depending on the MMU and selections you make, additional sub-menus and settings
will appear, enabling you to configure relevant settings.

Review any highlighted **Config Warnings / Errors** for configuration issues you need to correct.

## Managing Configuration Changes
When the `menuconfig` installer is launched after your initial setup and configuration, 
you will be prompted to choose how it should apply and reconcile configuration changes with 
locally applied settings. <br>

The installer supports three distinct modes for applying configuration changes:
_**R**efresh_, _**R**eplace_, and _**M**erge_.

<div width="100%">
<p align="center">
  <img src="GettingStarted-Installer-Configurator/GettingStarted-Menuconfig-Update-Options.png" alt="Menuconfig configuration update options" align=center width="60%">
</p>
</div>


1. **Refresh** (**Option 1 — Default upgrade path**)<br>
The Refresh mode preserves all parameter values that have been manually edited in your existing
Happy Hare `.cfg` files. It will only add new or missing configuration sections and options 
required by the current Happy Hare release. `menuconfig` values may appear outdated because
this mode does not update or overwrite existing parameters.

2. **Replace** (**Option 2 — Recommended**)<br>
This is the recommended mode **_when all configuration changes are managed through menuconfig_**. <br>
The **Replace** mode **OVERWRITES** any local changes you have made directly to your Happy Hare
`.cfg` files, resetting and regenerating a new configuration based solely on the selections
made in `menuconfig`.  

3. **Merge** (**Option 3 — Advanced**)<br>
Applies simple parameter updates from `menuconfig` while preserving other manual edits made to
your Happy Hare `.cfg` files. Useful when most settings are managed through `menuconfig` but
want hardware‑specific settings or tuning to remain untouched.

## Other
* Running `./install.sh` will always automatically check and update Happy Hare to the
  latest release from GitHub. To prevent this, launch with `-z` flag to skip the update check.
* `./install.sh` will never overwrite your existing configuration files. It will always create
  a timestamped backup of your current configuration before applying any changes.
* `./install.sh` `menuconfig` options and selections are saved to the `config/mmu/.mmu_config`
  file.
* `menuconfig` does not have the ability to sync and import changes made directly to your Happy
  Hare `.cfg` files. If you have made changes and want them reflected in `menuconfig`, you will
  need to manually transpose them before you will be able to use the `menuconfig` *Replace*
  option to reset your configuration baseline.  It is for this reason it is recommended to
  manage all configuration changes through `menuconfig` where possible.

---
