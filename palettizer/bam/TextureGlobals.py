### FORMAT
F_unspecified = 0
F_rgba = 1
F_rgbm = 2
F_rgba12 = 3
F_rgba8 = 4
F_rgba4 = 5
F_rgba5 = 6
F_rgb = 7
F_rgb12 = 8
F_rgb8 = 9
F_rgb5 = 10
F_rgb332 = 11
F_red = 12
F_green = 13
F_blue = 14
F_alpha = 15
F_luminance = 16
F_luminance_alpha = 17
F_luminance_alphamask = 18
### FORMAT

### FILTER TYPE
FT_unspecified = 0
FT_nearest = 1
FT_linear = 2
FT_nearest_mipmap_nearest = 3
FT_linear_mipmap_nearest = 4
FT_nearest_mipmap_linear = 5
FT_linear_mipmap_linear = 6
### FILTER TYPE

### QUALITY LEVEL
QL_unspecified = 0
QL_default = 1
QL_fastest = 2
QL_normal = 3
QL_best = 4
### QUALITY LEVEL

### WRAP MODE
WM_unspecified = 0
WM_clamp = 1
WM_repeat = 2
WM_mirror = 3
WM_mirror_once = 4
WM_border_color = 5
### WRAP MODE

### OMIT REASON
OR_none = 0
OR_working = 1
OR_omitted = 2
OR_size = 3
OR_solitary = 4
OR_coverage = 5
OR_unknown = 6
OR_unused = 7
OR_default_omit = 8
### OMIT REASON

### ALPHA BITS
AB_one = 0x01
AB_mid = 0x02
AB_zero = 0x04
AB_all = 0x07
### ALPHA BITS

### ALPHA MODE
AM_unspecified = 0
VM_unspecified = 1
VM_hidden = 2
VM_normal = 3
### ALPHA MODE

format_strings = {
    F_unspecified: 'unspecified',
    F_rgba: 'rgba',
    F_rgbm: 'rgbm',
    F_rgba12: 'rgba12',
    F_rgba8: 'rgba8',
    F_rgba4: 'rgba4',
    F_rgba5: 'rgba5',
    F_rgb: 'rgb',
    F_rgb12: 'rgb12',
    F_rgb8: 'rgb8',
    F_rgb5: 'rgb5',
    F_rgb332: 'rgb332',
    F_red: 'red',
    F_green: 'green',
    F_blue: 'blue',
    F_alpha: 'alpha',
    F_luminance: 'luminance',
    F_luminance_alpha: 'luminance_alpha',
    F_luminance_alphamask: 'luminance_alphamask'
}

filter_strings = {
    FT_unspecified: 'unspecified',
    FT_nearest: 'nearest',
    FT_linear: 'linear',
    FT_nearest_mipmap_nearest: 'nearest_mipmap_nearest',
    FT_linear_mipmap_nearest: 'linear_mipmap_nearest',
    FT_nearest_mipmap_linear: 'nearest_mipmap_linear',
    FT_linear_mipmap_linear: 'linear_mipmap_linear',
}

quality_strings = {
    QL_unspecified: 'unspecified',
    QL_default: 'default',
    QL_fastest: 'fastest',
    QL_normal: 'normal',
    QL_best: 'best'
}

wrap_mode_strings = {
    WM_unspecified: 'unspecified',
    WM_clamp: 'clamp',
    WM_repeat: 'repeat',
    WM_mirror: 'mirror',
    WM_mirror_once: 'mirror_once',
    WM_border_color: 'border_color'
}

omit_reason_strings = {
    OR_none: 'none',
    OR_working: 'working',
    OR_omitted: 'omitted',
    OR_size: 'size',
    OR_solitary: 'solitary',
    OR_coverage: 'coverage',
    OR_unknown: 'unknown',
    OR_unused: 'unused',
    OR_default_omit: 'default_omit'
}

alpha_mode_strings = {
    AM_unspecified: 'am_unspecified',
    VM_unspecified: 'vm_unspecified',
    VM_hidden: 'hidden',
    VM_normal: 'normal'
}

def get_format_string(format_type):
    return format_strings.get(format_type, 'unknown')

def get_filter_string(filter_type):
    return filter_strings.get(filter_type, 'unknown')

def get_quality_string(quality):
    return quality_strings.get(quality, 'unknown')

def get_wrap_mode_string(wrap_mode):
    return wrap_mode_strings.get(wrap_mode, 'unknown')

def get_omit_reason_string(omit_reason):
    return omit_reason_strings.get(omit_reason, 'unknown')

def get_alpha_mode_string(alpha_mode):
    return alpha_mode_strings.get(alpha_mode, 'unknown')