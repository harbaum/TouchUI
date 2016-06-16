# Support files for TouchUI

<dl>
  <dt><tt>touchui-init</tt></dt>
  <dd>This init script is supposed to be placed
    under <tt>/etc/init.d/touchui</tt>. Use <tt>update-rc.d touchui defaults</tt> to
    create the required links. <tt>touchui-init</tt> will try to run a
    file named <tt>/root/touchui/touchui</tt>.</dd>

  <dt><tt>touchui</tt></dt>
  <dd>This shell script is supposed to be placed under
    <tt>/root/touchui/touchui</tt> and will be called by
    <tt>touchui-init</tt>.  It will launch
    <tt>/root/touchui/launcher.py</tt> and thus expects the whole
    <tt>touchui</tt> directory to be placed under <tt>/root</tt>.</dd>
</dl>