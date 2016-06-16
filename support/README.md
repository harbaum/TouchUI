# Support files for TouchUI

<dl>
  <dt>`touchui-init`</dt>
  <dd>This init script is supposed to be placed
    under `/etc/init.d`. Use `update-rc.d touchui defaults` to
    create the required links. `touchui-init` will try to run a
    file named `/root/touchui/touchui`.</dd>

  <dt>`touchui`</dt>
  <dd>This shell script is supposed to be placed under
    `/root/touchui/touchui` and will be called by
    `touchui-init`.  It will launch
    `/root/touchui/launcher.py` and thus expects the whole
    `touchui` directory to be placed under `/root`.</dd>
</dl>