from libqtile import qtile
from libqtile.config import Group, Key, Drag, Click
from libqtile.lazy import lazy
import logging


def set_modkey(config_dict, key):

    config_dict['mod'] = key


def parse_cmd(mod_key, cmd):

    mod_dict = {'M': mod_key, 'C': 'control', 'S': 'shift'}

    cmd = cmd.split('-')
    if len(cmd) == 1:
        logging.warning(f"A keybinding must include at least one mod key. Failed to parse '{cmd}'")
        return None, None

    main_key = cmd[-1]
    try:
        modkeys = [mod_dict[m] for m in cmd[:-1]]
    except KeyError as e:
        logging.warning("Invalid mod key in keybinding. Failed to parse '{cmd}'")
        return None, None

    return modkeys, main_key


def gen_keybinding(mod_key, key_config):

    commands_dict = {
        'layout.left': lazy.layout.left,
        'layout.right': lazy.layout.right,
        'layout.down': lazy.layout.down,
        'layout.up': lazy.layout.up,
        'layout.next': lazy.layout.next,
        'layout.shuffle_left': lazy.layout.shuffle_left,
        'layout.shuffle_right': lazy.layout.shuffle_right,
        'layout.shuffle_down': lazy.layout.shuffle_down,
        'layout.shuffle_up': lazy.layout.shuffle_up,
        'layout.grow_left': lazy.layout.grow_left,
        'layout.grow_right': lazy.layout.grow_right,
        'layout.grow_down': lazy.layout.grow_down,
        'layout.grow_up': lazy.layout.grow_up,
        'layout.normalize': lazy.layout.normalize,
        'layout.toggle_split': lazy.layout.toggle_split,
        'spawn': lazy.spawn,
        'next_layout': lazy.next_layout,
        'window.kill': lazy.window.kill,
        'window.toggle_fullscreen': lazy.window.toggle_fullscreen,
        'window.toggle_floating': lazy.window.toggle_floating,
        'reload_config': lazy.reload_config,
        'shutdown': lazy.shutdown,
        'spawncmd': lazy.spawncmd
    }

    mod_keys, main_key = parse_cmd(mod_key, key_config['keys'])
    callback = commands_dict[key_config['cmd']] if isinstance(key_config['cmd'], str) else key_config['cmd']
    params = key_config['params'] if 'params' in key_config else []
    named_params = key_config['named_params'] if 'named_params' in key_config else dict()
    keybinding = Key(mod_keys, main_key, callback(*params, **named_params), desc=key_config['desc'])

    return keybinding


def set_keybindings(config_dict, keys_config):

    # TODO: find a way to get these values independently of the call order
    mod = config_dict['mod']
    terminal = config_dict['terminal']

    keys = [gen_keybinding(mod, key_config) for key_config in keys_config['ungrouped']]

    for i in [Group(i) for i in "123456789"]:

        switch_config = dict(
            keys=keys_config['tags']['switch']['keys']+i.name,
            cmd=lazy.group[i.name].toscreen,
            desc=keys_config['tags']['switch']['desc'].format(i.name)
        )
        switch_move_config = dict(
            keys=keys_config['tags']['switch_move']['keys']+i.name,
            cmd=lazy.window.togroup,
            desc=keys_config['tags']['switch_move']['desc'].format(i.name),
            params=[i.name],
            named_params=dict(switch_group=True)
        )

        keys.extend([
            gen_keybinding(mod, switch_config),
            gen_keybinding(mod, switch_move_config)
        ])

    config_dict['keys'] = keys


def set_mousebindings(config_dict, mouse):

    # TODO: find a way to get these values independently of the call order
    mod = config_dict['mod']

    mouse = [
        Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
        Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
        Click([mod], "Button2", lazy.window.bring_to_front()),
    ]
